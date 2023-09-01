import os
import re
import shutil
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from flask import render_template
import flask
from PIL import Image

from utils.works import get_dir_list, get_file_list

try:
    load_dotenv()
except:
    pass


TITLE = os.getenv("TITLE", "Seongmee Park")
EMAIL = os.getenv("EMAIL", "sw5860@naver.com")
IMAGE_ROOT = "static/images/"
WORK_TITLE = os.getenv("WORK_TITLE", "Together with green")
WORK_DESCRIPTION = os.getenv("WORK_DESCRIPTION", "Acrylic on canvas")
RESIZE = bool(os.getenv("RESIZE", 1))


def reset_resized_dir(dir, dest_dir="resized"):
    resized_dir = os.path.join(dir, dest_dir)
    if os.path.exists(resized_dir):
        shutil.rmtree(resized_dir, ignore_errors=True)
    os.mkdir(resized_dir)

def resize_image(dir, dest_dir, image_name, resize=True):
    resized_image_name = os.path.join(dir, dest_dir, image_name)

    if resize:
        original_image_name = os.path.join(dir, image_name)
        image = Image.open(original_image_name)
        image.thumbnail((750, 3000))
        image.save(resized_image_name)

    return resized_image_name

def resize_images_in_dir(dir, dest_dir="resized", resize=True):
    if resize:
        reset_resized_dir(dir, dest_dir)
    image_names = get_file_list(dir)
    resized_image_names = []

    # concurrency
    pool = ThreadPoolExecutor(max_workers=4)
    futures = [pool.submit(resize_image, dir, dest_dir, image_name, resize) for image_name in image_names]
    for future in futures:
        resized_image_names.append(future.result())
    
    # sync
    # for image_name in image_names:
    #     resized_image_name = resize_image(dir, dest_dir, image_name)
    #     resized_image_names.append(resized_image_name)
    return resized_image_names

def render_static_page(template_name, **kwargs):
    return render_template(
        template_name,
        **kwargs
    )

def write_static_page(template_name, **kwargs):
    html = render_static_page(template_name, **kwargs)
    with open(template_name, "w") as f:
        f.write(html)

def get_size_pattern(file_path):
    filename = os.path.split(file_path)[1]
    size_pattern_1 = r"(\d+)x(\d+)"
    match_1 = re.match(size_pattern_1, filename)
    if match_1:
        return match_1.group(0) + "cm"
    size_pattern_2 = r"(\d+)(호)"
    match_2 = re.match(size_pattern_2, filename)
    if match_2:
        return match_2.group(0)


app = flask.Flask(__name__)

resize = True
dirs = get_dir_list(IMAGE_ROOT)

if __name__ == "__main__":
    with app.app_context():
        # static pages
        templates = ["index.html", "profile.html", "notes.html", "articles.html", "contact.html"]
        for template in templates:
            if template in ["contact.html", "profile.html"]:
                write_static_page(template, title=TITLE, menus=dirs, email=EMAIL)
            else:
                write_static_page(template, title=TITLE, menus=dirs)

        # works pages
        for dir in dirs:
            image_dir = os.path.join(IMAGE_ROOT, dir) # ./static/images/2021
            resized_image_names = resize_images_in_dir(image_dir, resize=resize)
        
            works = []
            for work_image in resized_image_names:
                if dir.isdigit():
                    works.append({
                        "title": WORK_TITLE,
                        "description": WORK_DESCRIPTION,
                        "size": get_size_pattern(work_image) or "unknown",
                        "image_url": work_image,
                    })
                elif dir == "판화":
                    works.append({
                        "title": WORK_TITLE,
                        "description": "Etching & Auqatint",
                        "size": get_size_pattern(work_image) or "unknown",
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
        
