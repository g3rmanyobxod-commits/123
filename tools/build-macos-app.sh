#!/usr/bin/env bash
# Сборка macOS-приложения smpl для Apple Silicon (arm64) из десктопного макета examples/desktop-preview.html.
#   release/macos/smpl-macos-arm64.zip — всегда (нужен только zip);
#   release/macos/smpl-macos-arm64.dmg — на macOS через hdiutil; без macOS через tools/build_dmg_udif.py (нужен pycdlib).
# Состав .app: нативный Mach-O лаунчер (tools/macos/launcher, исходник smpl.zig), иконка AppIcon.icns
# из той же иконки, что у Android (tools/make_macos_icon.py), страница Resources/index.html.
# Лаунчер открывает интерфейс в браузере по умолчанию. VPN-ядра для macOS в проекте нет.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/examples/desktop-preview.html"
LAUNCHER="$ROOT/tools/macos/launcher/smpl-arm64"
OUT="$ROOT/release/macos"
NAME="smpl-macos-arm64"
APP_NAME="smpl"
VOLUME="smpl"
WORK="$(mktemp -d)"
APP="$WORK/$APP_NAME.app"
trap 'rm -rf "$WORK"' EXIT

for f in "$SRC" "$LAUNCHER"; do
  [ -f "$f" ] || { echo "нет файла $f"; exit 1; }
done

mkdir -p "$OUT" "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$SRC" "$APP/Contents/Resources/index.html"
cp "$LAUNCHER" "$APP/Contents/MacOS/$APP_NAME"
chmod 755 "$APP/Contents/MacOS/$APP_NAME"
python3 "$ROOT/tools/make_macos_icon.py" "$APP/Contents/Resources/AppIcon.icns"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>$APP_NAME</string>
  <key>CFBundleDisplayName</key><string>$APP_NAME</string>
  <key>CFBundleIdentifier</key><string>com.globevpn.desktop</string>
  <key>CFBundleExecutable</key><string>$APP_NAME</string>
  <key>CFBundleIconFile</key><string>AppIcon</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleShortVersionString</key><string>1.0.0</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>LSMinimumSystemVersion</key><string>11.0</string>
  <key>LSArchitecturePriority</key><array><string>arm64</string></array>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST
printf 'APPL????' > "$APP/Contents/PkgInfo"

IS_MAC=0
if [ "$(uname -s)" = "Darwin" ]; then
  IS_MAC=1
fi

if [ "$IS_MAC" = 1 ] && command -v codesign >/dev/null 2>&1; then
  # ad-hoc подпись всего бандла: без неё приложение не проходит проверку на Apple Silicon
  codesign --force --deep --sign - "$APP" >/dev/null 2>&1 || echo "предупреждение: codesign не удался"
fi

rm -f "$OUT/$NAME.zip"
(cd "$WORK" && zip -qry "$OUT/$NAME.zip" "$APP_NAME.app")
echo "ZIP: $OUT/$NAME.zip"

if [ "$IS_MAC" = 1 ] && command -v hdiutil >/dev/null 2>&1; then
  STAGE="$WORK/stage"
  mkdir -p "$STAGE"
  cp -R "$APP" "$STAGE/"
  ln -s /Applications "$STAGE/Applications"
  rm -f "$OUT/$NAME.dmg"
  hdiutil create -volname "$VOLUME" -srcfolder "$STAGE" -ov -format UDZO -imagekey zlib-level=9 "$OUT/$NAME.dmg"
  echo "DMG: $OUT/$NAME.dmg"
elif python3 -c "import pycdlib" >/dev/null 2>&1; then
  # без macOS: UDIF-контейнер (zlib) с ISO9660 + Rock Ridge + Joliet + UDF; см. tools/build_dmg_udif.py
  python3 "$ROOT/tools/build_dmg_udif.py" "$APP" "$OUT/$NAME.dmg" "$VOLUME"
else
  echo "DMG не собран: нужен macOS (hdiutil) или pip install pycdlib (без macOS)."
fi
