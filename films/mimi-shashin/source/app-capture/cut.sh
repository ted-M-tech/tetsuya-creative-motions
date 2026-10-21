#!/bin/sh
# Cut the app recording into the clips the edit uses. simctl records variable frame rate (no frames while the screen
# is still), so first resample the whole take to constant 60 fps, then cut by frame.
set -e
src="$(cd "$(dirname "$0")/.." && pwd)"; mov="$src/renders/app/describe.mov"; out="$src/hf/assets/app"; mkdir -p "$out"
cfr="$src/renders/app/describe-60.mp4"
[ "$cfr" -nt "$mov" ] || ffmpeg -v error -y -i "$mov" -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 "$cfr"
cut() { ffmpeg -v error -y -i "$cfr" -vf "trim=start_frame=$(echo "$2*60/1" | bc):end_frame=$(echo "$3*60/1" | bc),setpts=PTS-STARTPTS" -c:v libx264 -pix_fmt yuv420p -crf 18 "$out/$1.mp4"; }
cut menu 22.0 24.2      # practice tab, taps 写真描写
cut photos 24.2 26.2    # the photo list
cut cafe 29.9 32.9      # the cafe photo, taps record
cut result 38.4 40.9    # score and what she said, the mistake in red
cut fix 43.4 45.4       # People is sitting -> People are sitting
cut better 47.8 50.4    # a more natural sentence, with the model voice button
ls "$out"
