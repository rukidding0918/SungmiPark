import os
import shutil

from dotenv import load_dotenv
from flask import render_template
import flask
from PIL import Image

from utils.menus import menu
from utils.thumbnails import thumbnail
from utils.works import get_dir_list, get_file_list

load_dotenv()
TITLE = os.getenv("TITLE", "SUNGMI PARK")
IMAGE_ROOT = "./static/images/"


def reset_resized_dir(dir, dest_dir="resized"):
    resized_dir = os.path.join(dir, dest_dir)
    if os.path.exists(resized_dir):
        shutil.rmtree(resized_dir, ignore_errors=True)
    os.mkdir(resized_dir)

def resize_image(dir, dest_dir, image_name):
    full_path = os.path.join(dir, image_name)
    image = Image.open(full_path)
    image.thumbnail((750, 3000))
    resized_image_name = os.path.join(dir, dest_dir, image_name)
    image.save(resized_image_name)
    return resized_image_name

def resize_images_in_dir(dir, dest_dir="resized"):
    reset_resized_dir(dir, dest_dir)
    image_names = get_file_list(dir)
    resized_image_names = []
    for image_name in image_names:
        resized_image_name = resize_image(dir, dest_dir, image_name)
        resized_image_names.append(resized_image_name)
    return resized_image_names


app = flask.Flask(__name__)

if __name__ == "__main__":
    dirs = get_dir_list(IMAGE_ROOT)

    with app.app_context():
        # home
        index_html = render_template(
            'index.html',
            title = TITLE,
            menus = dirs,
        )
        with open("index.html", "w") as f:
            f.write(index_html)
        
        # works
        for dir in dirs:
            image_dir = os.path.join(IMAGE_ROOT, dir) # ./static/images/2021
            resized_image_names = resize_images_in_dir(image_dir)
        
            works = []
            for work_image in resized_image_names:
                works.append({
                    "title": os.getenv("WORK_TITLE", "title"),
                    "description": os.getenv("WORK_DESCRIPTION", "description"),
                    "size": os.getenv("WORK_SIZE", "100호"),
                    "image_url": work_image,
                })
                work_html = render_template(
                    'works.html',
                    title = TITLE,
                    menus = dirs,
                    year = dir,
                    works = works,
                )
            with open(f"{dir}.html", "w") as f:
                f.write(work_html)
        
        # profile
        profile_html = render_template(
            'profile.html',
            title = TITLE,
            menus = dirs,
        )
        with open("profile.html", "w") as f:
            f.write(profile_html)