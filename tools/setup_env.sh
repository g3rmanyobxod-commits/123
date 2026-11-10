#!/usr/bin/env bash
# Восстановление окружения после снапшота: SDK/JDK/Playwright живут вне воркспейса.
set -euo pipefail
WORK="${WORK:-/var/tmp/work}"

if [ ! -x "$WORK/and/android-15/aapt2" ]; then
  echo "▸ Android build-tools 35 + platform 34"
  mkdir -p "$WORK/and" /tmp/dl
  curl -sL -o /tmp/dl/bt.zip https://dl.google.com/android/repository/build-tools_r35_linux.zip
  (cd "$WORK/and" && unzip -q -o /tmp/dl/bt.zip)
  curl -sL -o /tmp/dl/plat.zip https://dl.google.com/android/repository/platform-34-ext7_r03.zip
  (mkdir -p "$WORK/and/plat" && cd "$WORK/and/plat" && unzip -q -o /tmp/dl/plat.zip)
  rm -f /tmp/dl/*.zip
fi

if [ ! -x "$WORK/jdk17/bin/java" ]; then
  echo "▸ JDK 17"
  curl -sL -o /tmp/dl/jdk.tar.gz "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.13%2B11/OpenJDK17U-jdk_x64_linux_hotspot_17.0.13_11.tar.gz"
  mkdir -p "$WORK/jdk17" && tar xzf /tmp/dl/jdk.tar.gz -C "$WORK/jdk17" --strip-components=1
  rm -f /tmp/dl/jdk.tar.gz
fi

python3 -c "import playwright" 2>/dev/null || { echo "▸ playwright"; pip install -q playwright; }
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()" 2>/dev/null || {
  echo "▸ chromium + системные библиотеки"
  python3 -m playwright install chromium
  sudo python3 -m playwright install-deps chromium
}
echo "✓ окружение готово ($WORK)"
