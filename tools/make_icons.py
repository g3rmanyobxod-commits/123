#!/usr/bin/env python3
"""Render legacy launcher PNGs (dark rounded tile + cream power glyph)."""
from PIL import Image, ImageDraw
import os

SIZES = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
DARK = (25, 26, 28, 255)
CREAM = (242, 240, 234, 255)
SS = 8  # supersample

BASE = os.path.join(os.path.dirname(__file__), '..', 'app', 'res')


def render(size):
    px = size * SS
    img = Image.new('RGBA', (px, px), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radius = int(px * 0.235)
    d.rounded_rectangle([0, 0, px - 1, px - 1], radius=radius, fill=DARK)

    cx = cy = px / 2
    ring_r = px * 0.235
    w = max(2, int(px * 0.062))
    # ring with a gap at the top
    d.arc([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
          start=302, end=238, fill=CREAM, width=w)
    # vertical bar
    top = cy - ring_r - px * 0.006
    bottom = cy + ring_r * 0.14
    d.line([cx, top, cx, bottom], fill=CREAM, width=w)
    return img.resize((size, size), Image.LANCZOS)


if __name__ == '__main__':
    for bucket, size in SIZES.items():
        out = os.path.join(BASE, 'mipmap-' + bucket, 'ic_launcher.png')
        render(size).save(out)
        render(size).save(os.path.join(BASE, 'mipmap-' + bucket, 'ic_launcher_round.png'))
        print('wrote', out)
