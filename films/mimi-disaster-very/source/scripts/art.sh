#!/bin/sh
# Cut out the drawn cast (white background -> transparent WebP), split the mouth illustrations into the two card panels,
# and stage them with the library plate and poses into hf/assets/art/ (not in Git).
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
mkdir -p hf/assets/art
for f in art/*.png; do
  n=$(basename "$f" .png)
  if [ "${n#mouth-}" != "$n" ]; then   # mouth illustration: side cross-section (top 55%) and front lips (bottom 45%) as two panels
    magick "$f" -resize 600x -gravity north -crop 100%x55%+0+0 +repage -quality 90 "art/$n-side.webp"
    magick "$f" -resize 600x -gravity south -crop 100%x45%+0+0 +repage -quality 90 "art/$n-front.webp"
    cp "art/$n-side.webp" "art/$n-front.webp" hf/assets/art/; continue
  else $K/scripts/cutout.sh "$f" "art/$n.webp" >/dev/null; fi
  cp "art/$n.webp" hf/assets/art/
done
cp $K/library/backgrounds/street.webp hf/assets/art/street.webp      # the plate: a sunny street (library); the fruit stall is drawn (art/stall.png)
for p in confident point jump friend-amazed friend-yay; do cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp; done
echo staged hf/assets/art
