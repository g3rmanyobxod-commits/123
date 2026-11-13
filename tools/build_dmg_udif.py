#!/usr/bin/env python3
"""Сборка .dmg БЕЗ macOS и без hdiutil.

Использование:
  python3 tools/build_dmg_udif.py <папка_приложения.app> <выходной.dmg> [имя_тома]

Контейнер — UDIF (формат Apple .dmg): внутри ISO9660 с Rock Ridge + Joliet + UDF,
содержимое сжато zlib-блоками (как UDZO). В образ кладётся папка приложения целиком
(права файлов сохраняются) и ссылка «Applications» на /Applications.

Проверка: после записи файл разбирается заново (koly → XML → mish → распаковка →
CRC32), ISO читается pycdlib, и дерево сравнивается с исходной папкой по именам,
содержимому и правам.

Ограничения:
  * Файл не открывался на macOS: hdiutil может потребовать дополнительных полей.
    Проверьте на Mac; при ошибке используйте ZIP или tools/build-macos-app.sh на Mac.
  * Нужен pycdlib (pip install pycdlib).
"""
import io
import os
import plistlib
import re
import stat
import struct
import sys
import uuid
import zlib

import pycdlib

CHUNK_SECTORS = 2048            # 1 МиБ несжатых данных на блок
ZLIB_TYPE = 0x80000005          # UDZO: zlib-блок
RAW_TYPE = 0x00000001           # несжатый блок
TERM_TYPE = 0xFFFFFFFF          # завершающая запись таблицы


def crc32(b: bytes) -> int:
    return zlib.crc32(b) & 0xFFFFFFFF


def walk_tree(src_dir):
    """Список (относительный путь, 'dir'|'file', mode, данные) в порядке обхода."""
    entries = []

    def rec(path, rel):
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                raise SystemExit('симлинки внутри приложения не поддерживаются: ' + full)
            child_rel = rel + [name]
            if stat.S_ISDIR(st.st_mode):
                entries.append(('/'.join(child_rel), 'dir', stat.S_IMODE(st.st_mode), None))
                rec(full, child_rel)
            else:
                with open(full, 'rb') as fh:
                    data = fh.read()
                entries.append(('/'.join(child_rel), 'file', stat.S_IMODE(st.st_mode), data))

    rec(src_dir, [])
    return entries


def build_iso(app_dir, app_name, volume):
    """ISO9660 (уровень 3) с Rock Ridge, Joliet и UDF. Имена ISO — генерируемые, настоящие — в RR/Joliet/UDF."""
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, rock_ridge='1.09', joliet=3, udf='2.60', vol_ident=volume[:32])

    # корень: папка приложения и ссылка Applications
    # режим корня приложения явно 0755: по умолчанию pycdlib ставит 0555 (владелец не может писать)
    iso.add_directory('/D0000', rr_name=app_name, joliet_path='/' + app_name, udf_path='/' + app_name,
                      file_mode=stat.S_IFDIR | 0o755)
    iso_dirs = {app_name: '/D0000'}
    counter = {'d': 1, 'f': 0}

    for rel, kind, mode, data in walk_tree(app_dir):
        parts = rel.split('/')
        parent_rel = '/'.join(parts[:-1])
        name = parts[-1]
        parent_iso = iso_dirs[app_name if not parent_rel else app_name + '/' + parent_rel]
        joliet = '/' + app_name + '/' + rel
        if kind == 'dir':
            iso_path = '%s/D%04d' % (parent_iso, counter['d'])
            counter['d'] += 1
            iso.add_directory(iso_path, rr_name=name, joliet_path=joliet, udf_path=joliet,
                              file_mode=stat.S_IFDIR | mode)
            iso_dirs[app_name + '/' + rel] = iso_path
        else:
            counter['f'] += 1
            iso_path = '%s/F%04d.;1' % (parent_iso, counter['f'])
            iso.add_fp(io.BytesIO(data), len(data), iso_path, rr_name=name,
                       joliet_path=joliet, udf_path=joliet, file_mode=stat.S_IFREG | mode)

    iso.add_symlink(symlink_path='/APPLICATIONS.;1', rr_symlink_name='Applications',
                    rr_path='/Applications', joliet_path='/Applications',
                    udf_symlink_path='/Applications', udf_target='/Applications')
    out = io.BytesIO()
    iso.write_fp(out)
    iso.close()
    data = out.getvalue()
    assert len(data) % 2048 == 0
    return data


def checksum_field(value: int) -> bytes:
    """Поле контрольной суммы UDIF: тип 2 (CRC32), размер 32, значение в первых 4 байтах."""
    return struct.pack('>II', 2, 32) + struct.pack('>I', value) + b'\0' * 124


def build_udif(iso: bytes, volume: str) -> bytes:
    total_sectors = len(iso) // 512
    blocks = []
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
    # сумма данных — CRC32 сырого data fork (сжатые блоки как лежат в файле), см. apple-dmg / pydmg
    koly[88:92] = struct.pack('>I', crc32(bytes(data)))
    struct.pack_into('>QQ', koly, 216, xml_off, xml_len)         # XML-таблица
    koly[352:360] = struct.pack('>II', 2, 32)                    # главная контрольная сумма
    koly[360:364] = master
    struct.pack_into('>I', koly, 488, 1)                         # вариант образа
    struct.pack_into('>Q', koly, 492, total_sectors)
    return bytes(data) + xml + bytes(koly)


def unpack_udif(dmg: bytes):
    """Разбор собственным парсером: koly → XML → mish → распаковка → CRC. Возвращает ISO-байты."""
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
            assert sec * 512 == len(out) and off == dlen
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
    assert struct.unpack_from('>I', koly, 88)[0] == crc32(dmg[:dlen]), 'CRC data fork'
    return bytes(out)


def compare_tree(app_dir, app_name, iso):
    """Читает ISO обратно и сравнивает с папкой: имена, содержимое, права."""
    r = pycdlib.PyCdlib()
    r.open_fp(io.BytesIO(iso))
    expected = {'/' + app_name: ('dir', 0o755, None), '/Applications': ('link', None, None)}
    for rel, kind, mode, data in walk_tree(app_dir):
        expected['/%s/%s' % (app_name, rel)] = (kind, mode, data)
    seen = set()

    def rec(rec_obj, path):
        for c in rec_obj.children:
            if c.is_dot() or c.is_dotdot():
                continue
            name = c.rock_ridge.name().decode() if c.rock_ridge else c.file_identifier().decode()
            full = path + '/' + name
            seen.add(full)
            if full not in expected:
                raise AssertionError('лишний файл в образе: ' + full)
            kind, mode, data = expected[full]
            if c.is_symlink():
                assert kind == 'link', full
                continue
            if c.is_dir():
                assert kind == 'dir', full
                if mode is not None:
                    assert c.rock_ridge.get_file_mode() & 0o7777 == mode, 'права ' + full
                rec(c, full)
            else:
                assert kind == 'file', full
                assert c.rock_ridge.get_file_mode() & 0o7777 == mode, 'права ' + full
                buf = io.BytesIO()
                r.get_file_from_iso_fp(buf, rr_path=full)
                assert buf.getvalue() == data, 'содержимое ' + full

    rec(r.get_record(rr_path='/'), '')
    missing = set(expected) - seen
    assert not missing, 'нет в образе: %s' % sorted(missing)[:5]
    r.close()


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    app_dir = os.path.abspath(sys.argv[1])
    out = sys.argv[2]
    volume = sys.argv[3] if len(sys.argv) > 3 else re.sub(r'\.app$', '', os.path.basename(app_dir))
    if not os.path.isdir(app_dir) or not app_dir.endswith('.app'):
        sys.exit('нужна папка приложения *.app: ' + app_dir)
    app_name = os.path.basename(app_dir)

    iso = build_iso(app_dir, app_name, volume)
    dmg = build_udif(iso, volume)
    assert unpack_udif(dmg) == iso, 'разбор не совпал с записью'
    compare_tree(app_dir, app_name, iso)

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    tmp = out + '.tmp'
    with open(tmp, 'wb') as fh:
        fh.write(dmg)
    os.replace(tmp, out)
    print('DMG: %s (%d байт, том «%s», проверка пройдена)' % (out, len(dmg), volume))


if __name__ == '__main__':
    main()
