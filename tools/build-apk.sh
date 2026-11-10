#!/usr/bin/env bash
# Сборка APK без Gradle: aapt2 → javac → d8 → zipalign → apksigner.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# SDK и JDK живут ВНЕ рабочей папки: снапшот воркспейса их обрезает.
SDK="${ANDROID_SDK:-/var/tmp/work/and}"
BT="$SDK/android-15"
PLATFORM="$SDK/plat/android-34/android.jar"
# JDK 17 нужен из-за PKCS12-хранилища ключа (java 11 его не читает)
if [ -z "${JAVA_HOME:-}" ] && [ -x /var/tmp/work/jdk17/bin/javac ]; then
  JAVA_HOME=/var/tmp/work/jdk17
fi
JAVA_HOME="${JAVA_HOME:-$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")}"
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$BT:$PATH"

APP="$ROOT/app"
BUILD="${BUILD_DIR:-/var/tmp/work/apkbuild}"
DIST="$ROOT/release"
KS="$ROOT/keystore/globevpn.jks"
KS_PASS="globevpn24"
KS_ALIAS="globevpn"

rm -rf "$BUILD"
mkdir -p "$BUILD/res" "$BUILD/gen" "$BUILD/classes" "$BUILD/dex" "$DIST" "$ROOT/keystore"

echo "▸ aapt2 compile"
"$BT/aapt2" compile --dir "$APP/res" -o "$BUILD/res/resources.zip"

echo "▸ aapt2 link"
"$BT/aapt2" link \
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

echo "▸ javac"
javac \
  -encoding UTF-8 \
  -source 8 -target 8 \
  -bootclasspath "$PLATFORM" \
  -classpath "$PLATFORM:$ROOT/libs/libv2ray.jar" \
  -d "$BUILD/classes" \
  $(find "$APP/src" "$BUILD/gen" -name '*.java')

echo "▸ d8"
"$BT/d8" --release --min-api 24 --lib "$PLATFORM" \
  --output "$BUILD/dex" \
  "$ROOT/libs/libv2ray.jar" \
  $(find "$BUILD/classes" -name '*.class')

echo "▸ package"
cd "$BUILD"
cp app-unsigned.apk packaged.apk
(cd "$BUILD/dex" && zip -q "$BUILD/packaged.apk" classes.dex*)
mkdir -p "$BUILD/libs/lib"
for abi in arm64-v8a armeabi-v7a; do
  mkdir -p "$BUILD/libs/lib/$abi"
  SO="$ROOT/libs/jni/$abi/libgojni.so"
  if [ ! -f "$SO" ]; then
    # .so не держим в воркспейсе (65 МБ) — берём из прошлой сборки
    mkdir -p "$BUILD/so/$abi"
    unzip -oq "$ROOT/GlobeVPN.apk" "lib/$abi/libgojni.so" -d "$BUILD/so"
    SO="$BUILD/so/lib/$abi/libgojni.so"
  fi
  cp "$SO" "$BUILD/libs/lib/$abi/"
done
(cd "$BUILD/libs" && zip -qr "$BUILD/packaged.apk" lib)
cd "$ROOT"

echo "▸ zipalign"
"$BT/zipalign" -f -p 4 "$BUILD/packaged.apk" "$BUILD/aligned.apk"

if [ ! -f "$KS" ]; then
  echo "▸ keystore"
  keytool -genkeypair -v \
    -keystore "$KS" -storepass "$KS_PASS" -keypass "$KS_PASS" \
    -alias "$KS_ALIAS" -keyalg RSA -keysize 2048 -validity 10950 \
    -dname "CN=Globe VPN, OU=Mobile, O=Globe VPN, L=Helsinki, C=FI" >/dev/null 2>&1
fi

echo "▸ sign"
"$BT/apksigner" sign \
  --ks "$KS" --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" \
  --ks-key-alias "$KS_ALIAS" \
  --min-sdk-version 24 \
  --out "$DIST/GlobeVPN-1.0.0.apk" \
  "$BUILD/aligned.apk"

"$BT/apksigner" verify --print-certs "$DIST/GlobeVPN-1.0.0.apk" | head -5
ls -lh "$DIST/GlobeVPN-1.0.0.apk"
cp "$DIST/GlobeVPN-1.0.0.apk" "$ROOT/GlobeVPN.apk"
echo "✓ готово: $DIST/GlobeVPN-1.0.0.apk + GlobeVPN.apk"
