#!/bin/sh
# Stage the library plate, counter and poses plus this episode's two codex-p poses (art/*.png) into hf/assets/art/ (not in Git).
# Series: swap PLATE and the pose list per episode; episode poses (art/*.png, codex-p) are cut out and staged too.
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
PLATE=${PLATE:-cafe}
mkdir -p hf/assets/art
for f in art/*.png; do
  [ -e "$f" ] || continue
  n=$(basename "$f" .png)
  $K/scripts/cutout.sh "$f" "art/$n.webp" >/dev/null
  cp "art/$n.webp" hf/assets/art/
done
cp $K/library/backgrounds/$PLATE.webp hf/assets/art/plate.webp
cp $K/library/backgrounds/cafe-counter.webp hf/assets/art/counter.webp
for p in presenter point friend-order friend-oops friend-nod friend-yay friend-hello; do
  cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp
done
echo staged hf/assets/art
