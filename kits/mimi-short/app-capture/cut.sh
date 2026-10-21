#!/bin/sh
# Cut a simulator recording into clips. simctl records variable frame rate (no frames while the screen is still), so the take is
# first resampled to constant 60 fps, then cut by frame; seeking the raw .mov lands on the wrong moment.
# usage: kits/mimi-short/app-capture/cut.sh <take.mov> <out-dir> name:start:end [name:start:end ...]   (seconds in the take)
set -e
mov=$1; out=$2; shift 2; mkdir -p "$out"
cfr="${mov%.*}-60.mp4"
[ "$cfr" -nt "$mov" ] || ffmpeg -v error -y -i "$mov" -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 "$cfr"
for spec in "$@"; do
  name=${spec%%:*}; rest=${spec#*:}; a=${rest%%:*}; b=${rest#*:}
  ffmpeg -v error -y -i "$cfr" -vf "trim=start_frame=$(echo "$a*60/1" | bc):end_frame=$(echo "$b*60/1" | bc),setpts=PTS-STARTPTS" \
    -c:v libx264 -pix_fmt yuv420p -crf 18 "$out/$name.mp4"
  echo "$out/$name.mp4"
done
