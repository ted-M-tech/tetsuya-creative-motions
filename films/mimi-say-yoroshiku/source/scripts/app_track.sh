#!/bin/sh
# Cut the simulator take onto the film's clock: hf/assets/app/compose.mp4 (6.35 s, film 5.0-11.35).
# Source (not in Git): renders/app/compose.mov (app-capture/ComposeWalkthrough.swift + compose-result.patch, Lanclo 5f5571ad),
# kept in Drive 063/Say1_Yoroshiku_assets/. Resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on compose-60.mp4: composer open with caret 36.75; typing 38.25-40.5; フレーズを作成 tapped ~45.45 (生成を中止 45.5);
# the result 47.75; 保存 tapped ~54.45; the list (with the saved phrase) 55.0.
# Film clock: seg1 empty 5.0-5.4 | seg2 typing x1.3 5.4-7.4 | seg3 create + loading 7.4-8.4 (tap 7.65) |
#             seg4 result 8.4-10.15 (appears 8.45) | seg5 save + list 10.15-11.35 (tap 10.35, list 10.9). Waits are skipped.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app renders/app/seg
T=renders/app/compose-60.mp4
[ -f $T ] || ffmpeg -v error -y -i renders/app/compose.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 $T
seg() { ffmpeg -v error -y -ss "$2" -t "$3" -i $T -an -vf "setpts=PTS/$4,fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "renders/app/seg/$1.mp4"; }
seg 1 36.6 0.4 1
seg 2 38.1 2.6 1.3
seg 3 45.2 1.0 1
seg 4 47.7 1.75 1
seg 5 54.25 1.2 1
printf "file 'seg/%s.mp4'\n" 1 2 3 4 5 > renders/app/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i renders/app/segs.txt -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 -t 6.35 hf/assets/app/compose.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/compose.mp4
