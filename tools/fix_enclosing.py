#!/usr/bin/env python3
"""Чистит класс-файлы libs/libv2ray.jar, которые роняют R8/D8 (NullPointerException).

Причина: у анонимного класса go/Seq$GoRefQueue$1 (объявлен в инициализаторе) атрибут
EnclosingMethod без имени, а у синтетического конструктора атрибут MethodParameters
с пустым именем параметра. Оба атрибута нужны только для рефлексии, на поведение
кода не влияют. Удаляются EnclosingMethod (класс) и MethodParameters (методы).
Использование: fix_enclosing.py in.jar out.jar
"""
import struct
import sys
import zipfile

DROP_CLASS = {'EnclosingMethod'}
DROP_MEMBER = {'MethodParameters'}


def _utf_table(data):
    n = struct.unpack('>H', data[8:10])[0]
    names = {}
    i, k = 10, 1
    while k < n:
        t = data[i]
        if t == 1:
            ln = struct.unpack('>H', data[i + 1:i + 3])[0]
            names[k] = data[i + 3:i + 3 + ln].decode('utf-8', 'replace')
            i += 3 + ln
        elif t in (3, 4):
            i += 5
        elif t in (5, 6):
            i += 9
            k += 1
        elif t in (7, 8, 16, 19, 20):
            i += 3
        elif t in (9, 10, 11, 12, 17, 18):
            i += 5
        elif t == 15:
            i += 4
        else:
            raise ValueError('bad constant tag %d' % t)
        k += 1
    return names, i


def _filter_attrs(data, pos, names, drop):
    """Читает таблицу атрибутов с pos, возвращает (байты без drop-атрибутов, новая позиция, число удалённых)."""
    cnt = struct.unpack('>H', data[pos:pos + 2])[0]
    r = pos + 2
    kept, removed = [], 0
    for _ in range(cnt):
        nm = struct.unpack('>H', data[r:r + 2])[0]
        ln = struct.unpack('>I', data[r + 2:r + 6])[0]
        if names.get(nm) in drop:
            removed += 1
        else:
            kept.append(data[r:r + 6 + ln])
        r += 6 + ln
    return struct.pack('>H', len(kept)) + b''.join(kept), r, removed


def patch(data):
    names, p = _utf_table(data)
    ifaces = struct.unpack('>H', data[p + 6:p + 8])[0]
    p = p + 8 + 2 * ifaces
    out = bytearray(data[:p])
    total = 0
    for _ in range(2):  # fields, methods
        cnt = struct.unpack('>H', data[p:p + 2])[0]
        out += data[p:p + 2]
        p += 2
        for _ in range(cnt):
            out += data[p:p + 6]  # access, name, descriptor
            attrs, p2, rm = _filter_attrs(data, p + 6, names, DROP_MEMBER)
            out += attrs
            total += rm
            p = p2
    attrs, p, rm = _filter_attrs(data, p, names, DROP_CLASS)
    out += attrs + data[p:]
    return bytes(out), total


def main():
    src, dst = sys.argv[1], sys.argv[2]
    total = 0
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info)
            if info.filename.endswith('.class'):
                data, rm = patch(data)
                total += rm
            zout.writestr(info.filename, data)
    print('fix_enclosing: removed %d attributes -> %s' % (total, dst))


if __name__ == '__main__':
    main()
