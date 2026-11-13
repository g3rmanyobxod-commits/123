#!/usr/bin/env python3
"""AppIcon.icns для macOS из той же иконки, что у Android (tools/make_icons.py).

Плашка уменьшается до сетки macOS (824 px на холсте 1024 px) — так иконка
выглядит как остальные приложения. Знак и цвета те же.

Использование: python3 tools/make_macos_icon.py <путь_к_AppIcon.icns>
Нужен Pillow (pip install pillow).
"""
import importlib.util
import io
import os
import struct
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CANVAS = 1024
TILE = 824  # стандартная сетка macOS: плашка 824 px в холсте 1024 px

# тип чанка → размер пикселей (PNG-вариант ICNS)
CHUNKS = [
    ('icp4', 16), ('icp5', 32), ('icp6', 64), ('ic07', 128), ('ic08', 256),
    ('ic09', 512), ('ic10', 1024), ('ic11', 32), ('ic12', 64), ('ic13', 256), ('ic14', 512),
]


def load_render():
    spec = importlib.util.spec_from_file_location('make_icons', os.path.join(HERE, 'make_icons.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.render


def master_canvas():
    render = load_render()
    tile = render(TILE)
    canvas = Image.new('RGBA', (CANVAS, CANVAS), (0, 0, 0, 0))
    offset = (CANVAS - TILE) // 2
    canvas.paste(tile, (offset, offset), tile)
    return canvas


def build_icns(out_path):
    master = master_canvas()
    body = b''
    for kind, px in CHUNKS:
        buf = io.BytesIO()
        master.resize((px, px), Image.LANCZOS).save(buf, format='PNG')
        data = buf.getvalue()
        body += kind.encode('ascii') + struct.pack('>I', len(data) + 8) + data
    with open(out_path, 'wb') as fh:
        fh.write(b'icns' + struct.pack('>I', len(body) + 8) + body)
    return out_path


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print('icns:', build_icns(sys.argv[1]))
