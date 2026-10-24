#!/bin/sh
# Review sheets: frames every 1.5 s of a cut, plain and with the platform zones drawn
# (red: bottom 420 px caption area and the right action rail x>900 y 820-1520; orange: top 200 px).
# usage: sh films/mimi-cloning/source/scripts/sheets.sh <cut.mp4> <out-prefix>
set -e
in=$1; out=$2; tmp=$(mktemp -d)
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
t=0.2; i=0
while [ "$(echo "$t < $dur" | bc)" = 1 ]; do
  ffmpeg -v error -y -ss $t -i "$in" -frames:v 1 "$tmp/f$(printf %03d $i).png"
  magick "$tmp/f$(printf %03d $i).png" -fill none -stroke 'rgba(255,0,0,0.9)' -strokewidth 6 -draw 'rectangle 0,1500 1080,1920' \
    -draw 'rectangle 900,820 1080,1520' -stroke 'rgba(255,140,0,0.9)' -draw 'rectangle 0,0 1080,200' \
    -stroke none -fill black -pointsize 70 -font /System/Library/Fonts/Helvetica.ttc -annotate +20+1880 "t=$t" "$tmp/z$(printf %03d $i).png"
  t=$(echo "$t + 1.5" | bc); i=$((i+1))
done
magick montage -font /System/Library/Fonts/Helvetica.ttc "$tmp"/f*.png -geometry 270x480+4+4 -tile 9x -background '#333' "$out-contact.png"
magick montage -font /System/Library/Fonts/Helvetica.ttc "$tmp"/z*.png -geometry 270x480+4+4 -tile 9x -background '#333' "$out-zones.png"
rm -rf "$tmp"; echo "$out-contact.png $out-zones.png"
