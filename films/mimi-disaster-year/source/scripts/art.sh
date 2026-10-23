#!/bin/sh
# Cut out the drawn art (white background -> transparent WebP) and stage it with the library poses, the reused mouth panels
# (episode 2, mimi-disaster-beach: /iː/ for the "y" glide, /ɪ/ for the bare vowel) and the winter shrine plate into hf/assets/art/ (not in Git).
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short
B=../../mimi-disaster-beach/source/art
mkdir -p hf/assets/art
for n in mimi-earmuffs heard-ear; do $K/scripts/cutout.sh "art/$n.png" "art/$n.webp" >/dev/null; cp "art/$n.webp" hf/assets/art/; done
magick art/shrine-winter.png -resize 1080x1920^ -gravity center -extent 1080x1920 -quality 90 hf/assets/art/shrine-winter.webp   # the plate (no cut-out)
for v in ee ih; do for p in front side; do cp "$B/mouth-$v-$p.webp" hf/assets/art/; done; done
for p in grin scream jump confident friend-hello friend-oops friend-yay; do cp $K/library/poses/$p.webp hf/assets/art/pose-$p.webp; done
echo staged hf/assets/art
