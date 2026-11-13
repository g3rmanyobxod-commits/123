#!/usr/bin/env python3
"""Сборка GlobeVPN-macos-arm64.dmg БЕЗ macOS и без hdiutil.

Контейнер — UDIF (формат Apple .dmg): внутри ISO9660 с Rock Ridge + Joliet + UDF,
содержимое сжато zlib-блоками (как UDZO). Содержимое то же, что у ZIP из
tools/build-macos-app.sh: GlobeVPN.app (исполняемый файл 755) и ссылка на /Applications.

Ограничения:
  * Файл проверяется собственным разбором (koly / mish / CRC32 / распаковка / чтение ISO),
    но НЕ открывался на macOS: hdiutil мог бы потребовать дополнительных полей.
    Проверьте на Mac: двойной клик по .dmg; при ошибке используйте ZIP.
  * Нужен пакет pycdlib (pip install pycdlib).

Использование: python3 tools/build_dmg_udif.py [путь_к_dmg]
"""
import base64
import io
import os
import plistlib
import shutil
import struct
import sys
import tempfile
import uuid
import zlib

import pycdlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'examples', 'desktop-preview.html')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'release', 'macos', 'GlobeVPN-macos-arm64.dmg')
VOLUME = 'GlobeVPN'
CHUNK_SECTORS = 2048            # 1 МиБ несжатых данных на блок
ZLIB_TYPE = 0x80000005          # UDZO: zlib-блок
RAW_TYPE = 0x00000001           # несжатый блок
TERM_TYPE = 0xFFFFFFFF          # завершающая запись таблицы


PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>GlobeVPN</string>
  <key>CFBundleDisplayName</key><string>GlobeVPN</string>
  <key>CFBundleIdentifier</key><string>com.globevpn.desktop</string>
  <key>CFBundleExecutable</key><string>GlobeVPN</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleShortVersionString</key><string>1.0.0</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>LSMinimumSystemVersion</key><string>11.0</string>
  <key>LSArchitecturePriority</key><array><string>arm64</string></array>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
"""

LAUNCHER = """#!/bin/bash
# открывает интерфейс в браузере по умолчанию
DIR="$(cd "$(dirname "$0")/../Resources" && pwd)"
exec /usr/bin/open "$DIR/index.html"
""".encode('utf-8')


def build_iso(index_html: bytes) -> bytes:
    """ISO9660 (уровень 3) с Rock Ridge, Joliet и UDF."""
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, rock_ridge='1.09', joliet=3, udf='2.60', vol_ident=VOLUME)

    def d(iso_path, rr, joliet):
        iso.add_directory(iso_path, rr_name=rr, joliet_path='/' + joliet, udf_path='/' + joliet)

    def f(data, iso_path, rr, joliet, mode):
        iso.add_fp(io.BytesIO(data), len(data), iso_path + ';1', rr_name=rr,
                   joliet_path='/' + joliet, file_mode=mode, udf_path='/' + joliet)

    d('/GLOBEVPNAPP', 'GlobeVPN.app', 'GlobeVPN.app')
    d('/GLOBEVPNAPP/CONTENTS', 'Contents', 'GlobeVPN.app/Contents')
    d('/GLOBEVPNAPP/CONTENTS/MACOS', 'MacOS', 'GlobeVPN.app/Contents/MacOS')
    d('/GLOBEVPNAPP/CONTENTS/RESOURCES', 'Resources', 'GlobeVPN.app/Contents/Resources')
    f(PLIST.encode('utf-8'), '/GLOBEVPNAPP/CONTENTS/INFO.PLIST', 'Info.plist',
      'GlobeVPN.app/Contents/Info.plist', 0o100644)
    f(LAUNCHER, '/GLOBEVPNAPP/CONTENTS/MACOS/GLOBEVPN', 'GlobeVPN',
      'GlobeVPN.app/Contents/MacOS/GlobeVPN', 0o100755)
    f(index_html, '/GLOBEVPNAPP/CONTENTS/RESOURCES/INDEX.HTML', 'index.html',
      'GlobeVPN.app/Contents/Resources/index.html', 0o100644)
    iso.add_symlink(symlink_path='/APPLICATIONS.;1', rr_symlink_name='Applications',
                    rr_path='/Applications', joliet_path='/Applications',
                    udf_symlink_path='/Applications', udf_target='/Applications')
    out = io.BytesIO()
    iso.write_fp(out)
    iso.close()
    data = out.getvalue()
    assert len(data) % 2048 == 0
    return data


def crc32(b: bytes) -> int:
    return zlib.crc32(b) & 0xFFFFFFFF


def checksum_field(value: int) -> bytes:
    """Поле контрольной суммы UDIF: тип 2 (CRC32), размер 32, значение в первых 4 байтах."""
    return struct.pack('>II', 2, 32) + struct.pack('>I', value) + b'\0' * 124


def build_udif(iso: bytes) -> bytes:
    total_sectors = len(iso) // 512
    blocks = []      # (data_bytes, first_sector, sector_count, type)
    for start in range(0, total_sectors, CHUNK_SECTORS):
        n = min(CHUNK_SECTORS, total_sectors - start)
        raw = iso[start * 512:(start + n) * 512]
        comp = zlib.compress(raw, 9)
        if len(comp) < len(raw):
            blocks.append((comp, start, n, ZLIB_TYPE))
        else:
            blocks.append((raw, start, n, RAW_TYPE))

    data = bytearray()
    runs = []
    for payload, sector, count, typ in blocks:
        runs.append(struct.pack('>IIQQQQ', typ, 0, sector, count, len(data), len(payload)))
        data += payload
    runs.append(struct.pack('>IIQQQQ', TERM_TYPE, 0, total_sectors, 0, len(data), 0))

    part_crc = crc32(iso)
    mish = struct.pack('>4sIQQQII', b'mish', 1, 0, total_sectors, 0, 0, 1)
    mish += b'\0' * 24 + checksum_field(part_crc)
    mish += struct.pack('>I', len(runs)) + b''.join(runs)

    name = 'disk image (Apple_ISO : 0)'
    xml = plistlib.dumps({
        'resource-fork': {
            'blkx': [{
                'Attributes': '0x0050',
                'CFName': name,
                'Data': mish,
                'ID': '0',
                'Name': name,
            }]
        }
    }, fmt=plistlib.FMT_XML)

    data_len = len(data)
    xml_off = data_len
    xml_len = len(xml)
    master = struct.pack('>I', crc32(struct.pack('>I', part_crc)))

    koly = bytearray(512)
    koly[0:4] = b'koly'
    struct.pack_into('>III', koly, 4, 4, 512, 1)                 # версия, размер заголовка, флаги
    struct.pack_into('>QQQQQ', koly, 16, 0, 0, data_len, xml_off, xml_len)
    struct.pack_into('>II', koly, 56, 1, 1)                      # сегмент 1 из 1
    koly[64:80] = uuid.uuid4().bytes
    koly[80:88] = struct.pack('>II', 2, 32)                      # контрольная сумма данных
    koly[88:92] = struct.pack('>I', part_crc)
    struct.pack_into('>QQ', koly, 216, xml_off, xml_len)         # XML-таблица
    koly[352:360] = struct.pack('>II', 2, 32)                    # главная контрольная сумма
    koly[360:364] = master
    struct.pack_into('>I', koly, 488, 1)                         # вариант образа
    struct.pack_into('>Q', koly, 492, total_sectors)
    return bytes(data) + xml + bytes(koly)


def verify(dmg: bytes, iso_expected: bytes) -> None:
    """Разбор собственным парсером: koly → XML → mish → распаковка → CRC → чтение ISO."""
    koly = dmg[-512:]
    assert koly[0:4] == b'koly', 'нет подписи koly'
    assert struct.unpack_from('>I', koly, 8)[0] == 512
    dlen = struct.unpack_from('>Q', koly, 32)[0]
    xml_off, xml_len = struct.unpack_from('>QQ', koly, 216)
    assert xml_off == dlen and xml_off + xml_len == len(dmg) - 512, 'смещения XML'
    plist = plistlib.loads(dmg[xml_off:xml_off + xml_len])
    blkx = plist['resource-fork']['blkx']
    assert len(blkx) == 1
    mish = blkx[0]['Data']
    assert mish[:4] == b'mish'
    nruns = struct.unpack_from('>I', mish, 200)[0]
    out = bytearray()
    for i in range(nruns):
        typ, _, sec, cnt, off, length = struct.unpack_from('>IIQQQQ', mish, 204 + 40 * i)
        if typ == TERM_TYPE:
            assert sec == len(iso_expected) // 512 and off == dlen
            break
        payload = dmg[off:off + length]
        if typ == ZLIB_TYPE:
            raw = zlib.decompress(payload)
        elif typ == RAW_TYPE:
            raw = payload
        else:
            raise AssertionError('неизвестный тип блока %x' % typ)
        assert len(raw) == cnt * 512
        assert sec * 512 == len(out)
        out += raw
    assert bytes(out) == iso_expected, 'распакованный образ не совпадает с ISO'
    assert struct.unpack_from('>I', koly, 88)[0] == crc32(bytes(out)), 'CRC данных'
    r = pycdlib.PyCdlib()
    r.open_fp(io.BytesIO(bytes(out)))
    rec = r.get_record(rr_path='/GlobeVPN.app/Contents/MacOS/GlobeVPN')
    assert rec.rock_ridge is not None and rec.rock_ridge.get_file_mode() & 0o111, 'у GlobeVPN нет бита исполнения'
    r.close()


def main() -> None:
    if not os.path.isfile(SRC):
        sys.exit('нет файла ' + SRC)
    with open(SRC, 'rb') as fh:
        index_html = fh.read()
    iso = build_iso(index_html)
    dmg = build_udif(iso)
    verify(dmg, iso)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + '.tmp'
    with open(tmp, 'wb') as fh:
        fh.write(dmg)
    os.replace(tmp, OUT)
    print('DMG: %s (%d байт, проверка разбора пройдена)' % (OUT, len(dmg)))


if __name__ == '__main__':
    main()
