#!/bin/sh
# Cut out the episode's drawn props (castle, apartment, outlet, complaint) (white background -> transparent WebP) and stage them with the library plate and poses
# into hf/assets/art/ (not in Git). Series: swap PLATE and the library pose list per episode.
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
PLATE=${PLATE:-street}
mkdir -p hf/assets/art
for f in art/*.png; do
  n=$(basename "$f" .png)
  $K/scripts/cutout.sh "$f" "art/$n.webp" >/dev/null
  cp "art/$n.webp" hf/assets/art/
done
cp $K/library/backgrounds/$PLATE.webp hf/assets/art/plate.webp
for p in sparkle perk droop confident point friend-order friend-oops friend-nod; do cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp; done
echo staged hf/assets/art
