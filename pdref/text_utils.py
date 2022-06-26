from datetime import datetime
import re


def slugify(text):
    # From Django
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[-\s]+", "-", slug).strip("-_")

    return slug

def make_frontmatter(title = '', author = '', date = datetime.now().strftime("%Y-%m-%d"), slug = '', keys = '', top_level = "false"):
    if slug:
        slug = f"slug: {slug}\n"
    
    yaml_array = [
        "---","\n", 
        f"title: '{title}'","\n", 
        f"author: '{author}'","\n", 
        f"date: '{date}'","\n", 
        slug,
        "toc: true","\n",
        f"top_level: {top_level}","\n",
        "categories:","\n", 
        "  - ","\n", 
        "tags:","\n", 
        "  - ","\n", 
        "---"
    ]

    if keys:
        yaml_array.insert(-1, "keys:\n")
        for key in keys:
            yaml_array.insert(-1, f"  - {key}\n")

    return yaml_array

def debug_image_text(img):
    strings = [
        "\n",
        "---", "\n",
        f"color count = {img.color_count()}  ", "\n",
        f"width = {img.w}; height = {img.h}  ", "\n",
        f"colorspace = {img.colorspace}  ", "\n",
        f"monochrome = {img.is_monochrome}  ", "\n",
        f"unicolor = {img.is_unicolor}  ", "\n",
        f"resolution xy = {img.xres}; {img.yres}  ", "\n",
        f"size = {img.size}  ", "\n",
        "\n"
        ]

    return strings