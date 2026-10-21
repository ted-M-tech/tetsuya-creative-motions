#!/bin/sh
# Render a Rive project to a PNG sequence (one headless screenshot per frame, 4 in parallel) and an MP4.
# usage: design/mimi-2d/scripts/render_rive.sh <rive-dir> <frames> <out-dir>
set -e
proj=$1; n=$2; out=$3
rm -rf "$out"; mkdir -p "$out"
rive "$proj" --verify >/dev/null
export proj out   # passed by environment: xargs -I limits the command to 255 bytes, too short for absolute paths
seq 0 $((n - 1)) | xargs -P 4 -n 1 sh -c 'rive "$proj" --screenshot="$out/f$(printf %03d "$1").png" --advance="$1" >/dev/null 2>&1' _
ffmpeg -v error -y -framerate 60 -i "$out/f%03d.png" -c:v libx264 -pix_fmt yuv420p -crf 16 "$out.mp4"
echo "$out.mp4 $(ls "$out" | wc -l | tr -d ' ') frames"
