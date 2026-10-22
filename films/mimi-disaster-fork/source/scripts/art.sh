#!/bin/sh
# Cut out the drawn cast (white background -> transparent WebP), convert the plate, and stage them with the library poses
# into hf/assets/art/ (not in Git). The plate is the one PNG whose name is not a character pose.
set -e
PLATE=${PLATE:-restaurant}
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
mkdir -p hf/assets/art
for f in art/*.png; do
  n=$(basename "$f" .png)
  if [ "$n" = "$PLATE" ]; then magick "$f" -resize 1080x1920^ -gravity center -extent 1080x1920 -quality 92 "art/$n.webp"
  elif [ "${n#mouth-}" != "$n" ]; then   # mouth illustration: side cross-section (top 55%) and front lips (bottom 45%) as two panels
    magick "$f" -resize 600x -gravity north -crop 100%x55%+0+0 +repage -quality 90 "art/$n-side.webp"
    magick "$f" -resize 600x -gravity south -crop 100%x45%+0+0 +repage -quality 90 "art/$n-front.webp"
    cp "art/$n-side.webp" "art/$n-front.webp" hf/assets/art/; continue
  elif false; then magick "$f" -resize 1080x1920^ -gravity center -extent 1080x1920 -quality 92 "art/$n.webp"
  else $K/scripts/cutout.sh "$f" "art/$n.webp" >/dev/null; fi
  cp "art/$n.webp" hf/assets/art/
done
for p in confident point perk speak-open jump; do cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp; done
for p in friend-hello friend-shrink; do cp $K/library/poses/$p.webp hf/assets/art/$p.webp; done   # library poses of the Friend
echo staged hf/assets/art
