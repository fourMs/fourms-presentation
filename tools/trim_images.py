#!/usr/bin/env python3
"""Trim the white margins of the graphics taken from the RITMO slide deck (PowerPoint), so that
their content fills the slide. Leaves a small margin. Run once after adding such a graphic:

    .venv/bin/python tools/trim_images.py images/rhythm-the-link.png ...
"""
import sys

from PIL import Image, ImageChops


def trim(path, pad=24):
    im = Image.open(path)
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    box = ImageChops.difference(rgb, bg).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    if not box:
        return
    l, t, r, b = box
    box = (max(l - pad, 0), max(t - pad, 0), min(r + pad, im.width), min(b + pad, im.height))
    im.crop(box).save(path)
    print(path, im.size, "->", (box[2] - box[0], box[3] - box[1]))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        trim(p)
