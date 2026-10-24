#!/bin/sh
# Stage the library plate and poses into hf/assets/art/ (not in Git). No episode-drawn poses in episode 3.
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
for p in grin talk presenter point highfive friend-amazed friend-oops friend-yay friend-hello; do
  cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp
done
echo staged hf/assets/art
