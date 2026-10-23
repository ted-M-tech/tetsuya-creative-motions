#!/bin/sh
# Stage the art into hf/assets/art/ (not in Git). No new poses: the dark living room, the Friend's ask pose and Mimi's
# flashlight come from Pronunciation Disasters 11 (films/mimi-disaster-light/source/art), the rest from the kit library.
set -e
cd "$(dirname "$0")/.."
K=../../../kits/mimi-short/library/poses
L=../../mimi-disaster-light/source/art
mkdir -p hf/assets/art
cp $L/living.webp $L/friend-ask.webp $L/mimi-flashlight.webp hf/assets/art/
for p in friend-yay friend-shrink friend-nod jump point; do cp $K/$p.webp hf/assets/art/$p.webp; done
echo staged hf/assets/art
