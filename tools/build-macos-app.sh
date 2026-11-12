#!/usr/bin/env bash
# Сборка macOS-приложения GlobeVPN для Apple Silicon (arm64) из десктопного макета examples/desktop-preview.html.
#   release/macos/GlobeVPN-macos-arm64.zip — всегда (нужен только zip);
#   release/macos/GlobeVPN-macos-arm64.dmg — только на macOS (нужен hdiutil).
# Приложение открывает интерфейс в браузере по умолчанию. VPN-ядра для macOS в проекте нет:
# это интерфейс без подключения.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/examples/desktop-preview.html"
OUT="$ROOT/release/macos"
NAME="GlobeVPN-macos-arm64"
WORK="$(mktemp -d)"
APP="$WORK/GlobeVPN.app"
trap 'rm -rf "$WORK"' EXIT

if [ ! -f "$SRC" ]; then
  echo "нет файла $SRC"
  exit 1
fi

mkdir -p "$OUT" "$APP/Contents/MacOS" "$APP/Contents/Resources"
cp "$SRC" "$APP/Contents/Resources/index.html"

cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
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
PLIST

cat > "$APP/Contents/MacOS/GlobeVPN" <<'LAUNCHER'
#!/bin/bash
# открывает интерфейс в браузере по умолчанию
DIR="$(cd "$(dirname "$0")/../Resources" && pwd)"
exec /usr/bin/open "$DIR/index.html"
LAUNCHER
chmod 755 "$APP/Contents/MacOS/GlobeVPN"

IS_MAC=0
if [ "$(uname -s)" = "Darwin" ]; then
  IS_MAC=1
fi

if [ "$IS_MAC" = 1 ] && command -v codesign >/dev/null 2>&1; then
  # ad-hoc подпись: без неё приложение не проходит проверку на Apple Silicon
  codesign --force --sign - "$APP" >/dev/null 2>&1 || echo "предупреждение: codesign не удался"
fi

rm -f "$OUT/$NAME.zip"
(cd "$WORK" && zip -qry "$OUT/$NAME.zip" GlobeVPN.app)
echo "ZIP: $OUT/$NAME.zip"

if [ "$IS_MAC" = 1 ] && command -v hdiutil >/dev/null 2>&1; then
  STAGE="$WORK/stage"
  mkdir -p "$STAGE"
  cp -R "$APP" "$STAGE/"
  ln -s /Applications "$STAGE/Applications"
  rm -f "$OUT/$NAME.dmg"
  hdiutil create -volname "GlobeVPN" -srcfolder "$STAGE" -ov -format UDZO -imagekey zlib-level=9 "$OUT/$NAME.dmg"
  echo "DMG: $OUT/$NAME.dmg"
else
  echo "DMG не собран: нужен macOS (hdiutil). Запустите tools/build-macos-app.sh на Mac."
fi
