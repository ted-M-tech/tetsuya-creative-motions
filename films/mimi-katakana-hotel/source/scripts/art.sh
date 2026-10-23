#!/bin/sh
# Stage the library plate and poses into hf/assets/art/ (not in Git). No new poses in this episode (all from the library).
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
PLATE=${PLATE:-lobby}
mkdir -p hf/assets/art
cp $K/library/backgrounds/$PLATE.webp hf/assets/art/plate.webp
for p in perk tilt point confident grin friend-hello friend-oops friend-yay friend-puzzled friend-amazed; do cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp; done
echo staged hf/assets/art
