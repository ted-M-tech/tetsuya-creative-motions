#!/bin/sh
# Cut out the episode's drawn poses (white background -> transparent WebP), convert the drawn pharmacy plate, and stage them
# with the V mouth panel (from films/mimi-disaster-very) and the library poses into hf/assets/art/ (not in Git).
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
mkdir -p hf/assets/art
for f in art/mimi-*.png; do
  n=$(basename "$f" .png)
  $K/scripts/cutout.sh "$f" "art/$n.webp" >/dev/null
  cp "art/$n.webp" hf/assets/art/
done
magick art/pharmacy.png -resize 1080x1920 -quality 88 art/pharmacy.webp
cp art/pharmacy.webp hf/assets/art/plate.webp
cp art/mouth-v-front.webp art/mouth-v-side.webp hf/assets/art/
for p in confident point friend-order friend-shrink friend-yay; do cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp; done
echo staged hf/assets/art
