#!/bin/sh
# Render one Rive shot to a PNG sequence (one headless screenshot per frame, 4 in parallel) and an MP4.
# usage: scripts/render_rive.sh <shot> <frames>
set -e
cd "$(dirname "$0")/.."
shot=$1; n=$2
out=renders/rive/$shot
rm -rf "$out"; mkdir -p "$out"
rive "rive/$shot" --verify >/dev/null
seq 0 $((n - 1)) | xargs -P 4 -I{} sh -c 'f=$(printf %03d {}); rive "rive/'"$shot"'" --screenshot="'"$out"'/f$f.png" --advance={} >/dev/null 2>&1'
ffmpeg -v error -y -framerate 60 -i "$out/f%03d.png" -c:v libx264 -pix_fmt yuv420p -crf 16 "$out.mp4"
echo "$out.mp4 $(ls $out | wc -l | tr -d ' ') frames"
