#!/bin/sh
# Drawn pose or prop (white background) -> transparent, trimmed, lossless WebP: white flood fill from the corners.
# usage: kits/mimi-short/scripts/cutout.sh drawn.png out.webp
#        lip-sync pair: cut both with the closed image's crop: CROP=WxH+X+Y kits/mimi-short/scripts/cutout.sh open.png open.webp
#        soft glow around a prop: FUZZ=30 (default 6)
set -e
src=$1; out=$2
tmp="$(mktemp -d)/full.png"
magick "$src" -alpha set -fuzz ${FUZZ:-6}% -fill none \
  -draw "color 2,2 floodfill" -draw "color %[fx:w-3],2 floodfill" \
  -draw "color 2,%[fx:h-3] floodfill" -draw "color %[fx:w-3],%[fx:h-3] floodfill" "$tmp"
crop=${CROP:-$(magick "$tmp" -format "%@" info:)}
mkdir -p "$(dirname "$out")"
magick "$tmp" -crop "$crop" +repage -bordercolor none -border 24 -define webp:lossless=true "$out"
echo "$out crop=$crop"
