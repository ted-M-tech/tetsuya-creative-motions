#!/bin/sh
# Stage the plate and poses into hf/assets/art/ (not in Git).
# Episode 2 art (codex-p, prompts/01-codex-mimi-waiter.txt): Mimi in a waiter role outfit (art/mimi-waiter-*.png, cut out here)
# and the restaurant plate with an empty table (art/restaurant-empty.png, a plate: no cutout). Library poses for the rest.
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
mkdir -p hf/assets/art
for n in empty sorry serve; do
  [ -e art/mimi-waiter-$n.webp ] || $K/scripts/cutout.sh art/mimi-waiter-$n.png art/mimi-waiter-$n.webp >/dev/null
  cp art/mimi-waiter-$n.webp hf/assets/art/pose-waiter-$n.webp
done
[ -e art/restaurant-empty.webp ] || magick art/restaurant-empty.png -resize 1080x1920^ -gravity center -extent 1080x1920 -quality 92 art/restaurant-empty.webp
cp art/restaurant-empty.webp hf/assets/art/plate.webp
for p in presenter point friend-hello friend-order friend-yay; do
  cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp
done
echo staged hf/assets/art
