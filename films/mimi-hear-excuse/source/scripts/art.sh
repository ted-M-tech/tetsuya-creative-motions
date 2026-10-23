#!/bin/sh
# Stage the library poses this episode uses into hf/assets/art/ (not in Git). No new poses: Mimi + Friend from the library only.
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
mkdir -p hf/assets/art
for p in angry flat confident point jump friend-dreamy friend-tease friend-shock friend-yay; do
  cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp
done
echo staged hf/assets/art
