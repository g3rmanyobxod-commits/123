#!/usr/bin/env bash
# Восстановление окружения после снапшота: SDK/JDK/Playwright живут вне воркспейса.
set -euo pipefail
WORK="${WORK:-/var/tmp/work}"

# Автономный тулчейн без Google SDK (если dl.google.com недоступен):
#   aapt2 — npm aaptjs3, android.jar / d8 / apksigner / ecj — npm @drxiaozhi/minapk, Java — PyPI jdk4py.
if [ ! -x "$WORK/and/android-15/aapt2" ] && [ ! -f "$WORK/and/tools/android.jar" ]; then
  echo "▸ автономный тулчейн (npm + PyPI)"
  mkdir -p "$WORK/and/tools" "$WORK/jdk" /tmp/dl && cd /tmp/dl
  npm pack aaptjs3@2.0.2 >/dev/null 2>&1
  npm pack @drxiaozhi/minapk@0.5.1 >/dev/null 2>&1
  tar xzf aaptjs3-2.0.2.tgz && cp package/bin/x64/linux/aapt2 "$WORK/and/aapt2" && rm -rf package
  mkdir -p mp && tar xzf drxiaozhi-minapk-0.5.1.tgz -C mp
  cp mp/package/tools/android.jar mp/package/tools/d8.jar mp/package/tools/apksigner.jar mp/package/tools/ecj-3.45.0.jar "$WORK/and/tools/"
  chmod +x "$WORK/and/aapt2"
  python3 -m pip download -q --no-deps jdk4py==25.0.2.1 --only-binary=:all: -d jdk4 2>/dev/null || pip download -q --no-deps jdk4py==25.0.2.1 --only-binary=:all: -d jdk4
  python3 -c "import zipfile,glob; zipfile.ZipFile(glob.glob('jdk4/*.whl')[0]).extractall('jdkx')"
  cp -r jdkx/jdk4py/java-runtime "$WORK/jdk/" && chmod +x "$WORK/jdk/java-runtime/bin/"*
  rm -rf /tmp/dl/mp /tmp/dl/jdk4 /tmp/dl/jdkx /tmp/dl/*.tgz
  cd - >/dev/null
  echo "✓ автономный тулчейн: $WORK/and/tools, $WORK/jdk"
fi

if [ ! -x "$WORK/and/android-15/aapt2" ] && [ ! -f "$WORK/and/tools/android.jar" ]; then
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
