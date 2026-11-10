#!/usr/bin/env bash
# Сборка APK без Gradle: aapt2 → ecj → d8 → (выравнивание) → apksigner.
#
# Два режима инструментов:
#   1) Android SDK (ANDROID_SDK или /var/tmp/work/and с android-15/): aapt2, zipalign, d8, apksigner из build-tools.
#   2) Автономный набор (tools/setup_env.sh → $WORK/and/tools, $WORK/jdk): aapt2 из npm-пакета aaptjs3,
#      android.jar, d8.jar, apksigner.jar и ecj из npm-пакета @drxiaozhi/minapk, Java из jdk4py.
# Режим выбирается автоматически. Для ядра нужен libgojni.so (см. README, раздел «Ядро»).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="${WORK:-/var/tmp/work}"
APP="$ROOT/app"
BUILD="${BUILD_DIR:-$WORK/apkbuild}"
DIST="$ROOT/release"
KS="$ROOT/keystore/globevpn.jks"
KS_PASS="globevpn24"
KS_ALIAS="globevpn"
APK_NAME="GlobeVPN-1.0.0.apk"

if [ -x "${ANDROID_SDK:-$WORK/and}/android-15/aapt2" ]; then
  MODE=sdk
  SDK="${ANDROID_SDK:-$WORK/and}"
  BT="$SDK/android-15"
  PLATFORM="$SDK/plat/android-34/android.jar"
  AAPT2="$BT/aapt2"
  ZIPALIGN="$BT/zipalign"
  JAVA_BIN="$(dirname "$(readlink -f "$(command -v javac)")")"
  JAVA="java"; JAVAC="javac"
  D8="$BT/d8"
  APKSIGNER="$BT/apksigner"
else
  MODE=offline
  TOOLS="$WORK/and/tools"
  PLATFORM="$TOOLS/android.jar"
  AAPT2="$WORK/and/aapt2"
  JAVA="$WORK/jdk/java-runtime/bin/java"
  ECJ="$TOOLS/ecj-3.45.0.jar"
  D8_JAR="$TOOLS/d8.jar"
  APKSIGNER_JAR="$TOOLS/apksigner.jar"
  for f in "$AAPT2" "$JAVA" "$ECJ" "$D8_JAR" "$APKSIGNER_JAR" "$PLATFORM"; do
    [ -e "$f" ] || { echo "нет инструмента: $f — запустите tools/setup_env.sh"; exit 1; }
  done
fi

echo "▸ режим инструментов: $MODE"
rm -rf "$BUILD"
mkdir -p "$BUILD/res" "$BUILD/gen" "$BUILD/classes" "$BUILD/dex" "$DIST" "$ROOT/keystore"

echo "▸ aapt2 compile"
"$AAPT2" compile --dir "$APP/res" -o "$BUILD/res/resources.zip"

echo "▸ aapt2 link"
"$AAPT2" link \
  -o "$BUILD/app-unsigned.apk" \
  -I "$PLATFORM" \
  --manifest "$APP/AndroidManifest.xml" \
  -R "$BUILD/res/resources.zip" \
  -A "$APP/assets" \
  --java "$BUILD/gen" \
  --min-sdk-version 24 \
  --target-sdk-version 34 \
  --version-code 1 \
  --version-name "1.0.0" \
  --auto-add-overlay

echo "▸ компиляция Java"
SOURCES=$(find "$APP/src" "$BUILD/gen" -name '*.java')
if [ "$MODE" = sdk ]; then
  "$JAVAC" -encoding UTF-8 -source 8 -target 8 -bootclasspath "$PLATFORM" \
    -classpath "$PLATFORM:$ROOT/libs/libv2ray.jar" -d "$BUILD/classes" $SOURCES
else
  # shellcheck disable=SC2086
  "$JAVA" -jar "$ECJ" -encoding UTF-8 -source 1.8 -target 1.8 -proc:none -nowarn \
    -bootclasspath "$PLATFORM" -cp "$PLATFORM:$ROOT/libs/libv2ray.jar" \
    -d "$BUILD/classes" $SOURCES
fi

echo "▸ очистка libv2ray.jar (обход падения R8 на go/Seq\$GoRefQueue\$1)"
python3 "$ROOT/tools/fix_enclosing.py" "$ROOT/libs/libv2ray.jar" "$BUILD/libv2ray-fixed.jar"

echo "▸ d8"
CLASSES=$(find "$BUILD/classes" -name '*.class')
if [ "$MODE" = sdk ]; then
  # shellcheck disable=SC2086
  "$D8" --release --min-api 24 --lib "$PLATFORM" --output "$BUILD/dex" "$BUILD/libv2ray-fixed.jar" $CLASSES
else
  # shellcheck disable=SC2086
  "$JAVA" -cp "$D8_JAR" com.android.tools.r8.D8 --release --min-api 24 --lib "$PLATFORM" \
    --output "$BUILD/dex" "$BUILD/libv2ray-fixed.jar" $CLASSES
fi

echo "▸ упаковка"
cp "$BUILD/app-unsigned.apk" "$BUILD/packaged.apk"
(cd "$BUILD/dex" && zip -q "$BUILD/packaged.apk" classes*.dex)

# Нативное ядро: libs/jni/<abi>/libgojni.so, либо из старого APK в корне репозитория.
HAVE_CORE=0
mkdir -p "$BUILD/libs/lib"
for abi in arm64-v8a armeabi-v7a; do
  SO="$ROOT/libs/jni/$abi/libgojni.so"
  if [ ! -f "$SO" ] && [ -f "$ROOT/GlobeVPN.apk" ]; then
    mkdir -p "$BUILD/so/$abi"
    if unzip -oq "$ROOT/GlobeVPN.apk" "lib/$abi/libgojni.so" -d "$BUILD/so" 2>/dev/null; then
      SO="$BUILD/so/lib/$abi/libgojni.so"
    fi
  fi
  if [ -f "$SO" ]; then
    mkdir -p "$BUILD/libs/lib/$abi"
    cp "$SO" "$BUILD/libs/lib/$abi/"
    HAVE_CORE=1
  fi
done
if [ "$HAVE_CORE" = 1 ]; then
  (cd "$BUILD/libs" && zip -qr "$BUILD/packaged.apk" lib)
else
  echo "! libgojni.so не найден: APK соберётся, но ядро VPN работать не будет"
fi

echo "▸ выравнивание"
if [ "$MODE" = sdk ]; then
  "$ZIPALIGN" -f -p 4 "$BUILD/packaged.apk" "$BUILD/aligned.apk"
else
  python3 "$ROOT/tools/zipalign.py" "$BUILD/packaged.apk" "$BUILD/aligned.apk"
fi

echo "▸ подпись"
if [ "$MODE" = sdk ]; then
  "$APKSIGNER" sign --ks "$KS" --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" \
    --ks-key-alias "$KS_ALIAS" --min-sdk-version 24 --out "$DIST/$APK_NAME" "$BUILD/aligned.apk"
  "$APKSIGNER" verify --print-certs "$DIST/$APK_NAME" | head -5
else
  "$JAVA" -jar "$APKSIGNER_JAR" sign --ks "$KS" --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" \
    --ks-key-alias "$KS_ALIAS" --min-sdk-version 24 --out "$DIST/$APK_NAME" "$BUILD/aligned.apk"
  "$JAVA" -jar "$APKSIGNER_JAR" verify --print-certs "$DIST/$APK_NAME" | head -5
fi

ls -lh "$DIST/$APK_NAME"
echo "✓ готово: $DIST/$APK_NAME (ядро: $([ "$HAVE_CORE" = 1 ] && echo есть || echo НЕТ))"
