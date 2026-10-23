#!/bin/sh
# Stage the poses this episode uses into hf/assets/art/ (not in Git): Mimi + Friend library poses, plus art/pose-angry-filled.webp
# (the library angry.webp with its see-through white body filled, owner 2026-10-23: 「62透過されている？」; the kit library is unchanged).
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
mkdir -p hf/assets/art
for p in flat confident point jump friend-dreamy friend-tease friend-shock friend-yay; do
  cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp
done
cp art/pose-angry-filled.webp hf/assets/art/pose-angry-filled.webp
echo staged hf/assets/art
