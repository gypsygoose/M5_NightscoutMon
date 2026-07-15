#!/bin/bash
# Builds a SPIFFS image from /data (the smooth-font .vlw files) and flashes
# it to the M5Stack Core2's spiffs partition.
#
# Arduino IDE 2.x dropped the old "ESP32 Sketch Data Upload" menu plugin, so
# this replaces it. Only needs to be run once (or whenever files in /data
# change) - it's independent of the normal sketch upload.
#
# Usage: tools/upload_data.sh /dev/cu.usbserial-XXXX
set -euo pipefail

PORT="${1:?Usage: $0 <serial-port>  (e.g. /dev/cu.usbserial-0001)}"

ESP32_CORE_DIR="$HOME/Library/Arduino15/packages/esp32"
MKSPIFFS="$(find "$ESP32_CORE_DIR/tools/mkspiffs" -type f -name mkspiffs | head -1)"
ESPTOOL="$(find "$ESP32_CORE_DIR/tools/esptool_py" -type f -name esptool | head -1)"
DATA_DIR="$(cd "$(dirname "$0")/.." && pwd)/data"

if [[ -z "$MKSPIFFS" || -z "$ESPTOOL" ]]; then
  echo "Could not find mkspiffs/esptool under $ESP32_CORE_DIR - install the esp32 board package via Arduino IDE first." >&2
  exit 1
fi

# Must match the "spiffs" row of the board's partition table
# (default_16MB.csv for M5Stack-Core2 as of esp32 core 2.0.17):
#   spiffs, data, spiffs, 0xc90000, 0x360000
SPIFFS_OFFSET=0xc90000
SPIFFS_SIZE=0x360000
PAGE_SIZE=256
BLOCK_SIZE=4096

TMP_IMG="$(mktemp -t spiffs.XXXXXX.bin)"
trap 'rm -f "$TMP_IMG"' EXIT

echo "Building SPIFFS image from $DATA_DIR ..."
"$MKSPIFFS" -c "$DATA_DIR" -p "$PAGE_SIZE" -b "$BLOCK_SIZE" -s "$SPIFFS_SIZE" "$TMP_IMG"

echo "Flashing to $PORT at offset $SPIFFS_OFFSET ..."
# 921600 fails "serial noise or corruption" on some USB-serial adapters;
# 115200 is slower but reliable. Override with: BAUD=921600 tools/upload_data.sh ...
"$ESPTOOL" --chip esp32 --port "$PORT" --baud "${BAUD:-115200}" write_flash "$SPIFFS_OFFSET" "$TMP_IMG"

echo "Done."
