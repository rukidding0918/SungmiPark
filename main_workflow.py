import os

from dotenv import load_dotenv
from flask import render_template
import flask

from utils.menus import menu
from utils.thumbnails import thumbnail
from utils.works import get_dir_list, get_file_list

load_dotenv()
TITLE = os.getenv("TITLE")
IMAGE_ROOT = "./static/images/"

app = flask.Flask(__name__)


if __name__ == "__main__":
    dirs = get_dir_list(IMAGE_ROOT)

    with app.app_context():
        index_html = render_template(
            'index.html',
            title = TITLE,
            menus = dirs,
        )
        with open("index.html", "w") as f:
            f.write(index_html)
        
        for dir in dirs:
            work_images = get_file_list(IMAGE_ROOT + dir)
            works = []
            for work_image in work_images:
                works.append({
                "title": os.getenv("WORK_TITLE"),
                "description": os.getenv("WORK_DESCRIPTION"),
                "size": os.getenv("WORK_SIZE"),
                "image_url": f"/static/images/{dir}/{work_image}",
                })
                work_html = render_template(
                    'works.html',
                    title = TITLE,
                    menus = dirs,
                    works = works,
                )
                with open(f"./src/works/{dir}.html", "w") as f:
                    f.write(work_html)
        profile_html = render_template(
            'profile.html',
            title = TITLE,
            menus = dirs,
        )
        with open("src/profile.html", "w") as f:
            f.write(profile_html)