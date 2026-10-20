#!/bin/sh
# Cut drawn poses (white background) out to transparent PNGs in art/cut/: flood-fill white from the four corners, trim.
# usage: scripts/cutout.sh hide reach droop ...
set -e
cd "$(dirname "$0")/.."
mkdir -p art/cut
for p in "$@"; do
  magick "art/$p.png" -alpha set -fuzz 6% -fill none \
    -draw "color 2,2 floodfill" -draw "color %[fx:w-3],2 floodfill" \
    -draw "color 2,%[fx:h-3] floodfill" -draw "color %[fx:w-3],%[fx:h-3] floodfill" \
    -trim +repage -bordercolor none -border 24 "art/cut/$p.png"
  echo "art/cut/$p.png $(identify -format '%wx%h' art/cut/$p.png)"
done
