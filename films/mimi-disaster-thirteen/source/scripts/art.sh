#!/bin/sh
# Cut out the drawn cast and props (white background -> transparent WebP), resize the booth plate, crop its counter front
# (layered in front of Mimi the clerk), and stage them with the library poses into hf/assets/art/ (not in Git).
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
mkdir -p hf/assets/art
for n in mimi-clerk-smile mimi-clerk-tickets friend-buried ticket; do
  $K/scripts/cutout.sh "art/$n.png" "art/$n.webp" >/dev/null
  cp "art/$n.webp" hf/assets/art/
done
magick art/booth.png -resize 1080x1920! -quality 90 art/booth.webp                       # the plate
magick art/booth.webp -crop 1080x265+0+1028 +repage -quality 90 art/booth-counter.webp   # the counter front (sill + red panel)
cp art/booth.webp art/booth-counter.webp hf/assets/art/
for p in scream jump confident friend-order friend-shock friend-yay; do cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp; done
echo staged hf/assets/art
