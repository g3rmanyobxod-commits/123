#!/usr/bin/env python3
"""Выравнивание APK (аналог zipalign -p 4) без Android SDK.

Несжатые записи сдвигаются так, чтобы их данные начинались с кратного 4 смещения
(поле extra с id 0xd935, как у zipalign). Нужно для установки и для resources.arsc/.so.
"""
import struct
import sys
import zipfile

src, dst = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, 'w') as zout:
    for info in zin.infolist():
        data = zin.read(info)
        ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        ni.compress_type = info.compress_type
        ni.external_attr = info.external_attr
        if info.compress_type == zipfile.ZIP_STORED:
            start = zout.fp.tell()
            base = start + 30 + len(info.filename.encode('utf-8'))
            extra_len = 4 + ((4 - ((base + 4) % 4)) % 4)
            ni.extra = struct.pack('<HH', 0xD935, extra_len - 4) + b'\0' * (extra_len - 4)
        zout.writestr(ni, data)
print('aligned: %s' % dst)
