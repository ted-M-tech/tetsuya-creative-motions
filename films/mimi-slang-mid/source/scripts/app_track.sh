#!/bin/sh
# Cut the simulator take into the film's app clips (hf/assets/app/*.mp4) on the film clock (app beat 8.4-12.8 s).
# Source (not in Git): renders/app/slang.mov (app-capture/SlangWalkthrough.swift, no patch, Lanclo origin/main ff11569c),
# kept in Drive 071/Slang4_Mid_assets/. The take is resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on slang-60.mp4 (scene changes): deck list 16.6-20.6 (スラング・カジュアル tapped ~20.5), units 20.65-24.5
# (ユニット2 tapped ~24.4), unit 2 top 24.55-28.0, the swipes through unit 2 28.1-55.9 (this take kept the scroll frames),
# the "mid" card low on screen 55.9-66.8, dragged to the top 66.8-67.7, save tapped ~71.9 (tag menu 72.0-75.2),
# bookmark filled 75.25-79.0, swipe to the "extra" card 79.0.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/slang-60.mp4 ] || ffmpeg -v error -y -i renders/app/slang.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/slang-60.mp4
V="fps=60,scale=1206:2622,format=yuv420p"
clip() { ffmpeg -v error -y -ss "$2" -i renders/app/slang-60.mp4 -t "$3" -an -vf "$V" -c:v libx264 -crf 16 "hf/assets/app/$1.mp4"; }
clip list 19.55 1.0       # 単語帳: the deck list (counts masked in the edit), スラング・カジュアル tapped at the end
clip units 23.55 0.9      # スラング・カジュアル: the units (counts masked in the edit), ユニット2 tapped at the end
clip unit 24.6 0.4        # ユニット2 微妙・イヤのリアクション: meh …
# the real scroll, sped up: 28.1-55.9 into 0.4 s (meh … basic → mid), then the drag that brings "mid" to the top, 66.8-67.7 into 0.2 s
ffmpeg -v error -y -i renders/app/slang-60.mp4 -an -filter_complex \
  "[0:v]trim=28.1:55.9,setpts=(PTS-STARTPTS)/69.5[a];[0:v]trim=66.8:67.7,setpts=(PTS-STARTPTS)/4.5[b];[a][b]concat=n=2:v=1,$V,trim=0:0.6[o]" \
  -map "[o]" -c:v libx264 -crf 16 hf/assets/app/scroll.mp4
clip card 71.55 0.5       # the "mid" card at the top, save tapped at ~71.9
clip saved 75.3 1.0       # the bookmark filled (tag menu skipped)
for f in hf/assets/app/*.mp4; do printf '%s %s\n' "$f" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")"; done
