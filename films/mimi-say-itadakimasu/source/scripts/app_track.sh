#!/bin/sh
# Cut the simulator take onto the film's clock: hf/assets/app/compose.mp4 (6.646 s, film 4.3-10.946).
# Source (not in Git): renders/app/compose.mov (app-capture/ComposeWalkthrough.swift + compose-result.patch, Lanclo 1088ae0b),
# kept in Drive 077/Say3_Itadakimasu_assets/. Resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on compose-60.mp4 (4 fps tile sheets): フレーズを追加 with caret 37.25; typing 39.2-41.6 (食べる前の 39.5, いただきます 41.25);
# フレーズを作成 tapped ~46.6 (表現を考えています… 46.75); フレーズを確認 with "Let's eat!" and its example 49.0;
# 保存 tapped ~56.7; マイノートに保存したよ。 57.25.
# Film clock: seg1 caret 4.3-4.6 | seg2 typing x1.3 4.6-6.446 | seg3 create + thinking 6.446-7.446 (tap 6.746) |
#             seg4 result 7.446-9.446 (appears 7.546) | seg5 save + saved 9.446-10.946 (tap 9.746, saved 10.296). Waits are skipped.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app renders/app/seg
T=renders/app/compose-60.mp4
[ -f $T ] || ffmpeg -v error -y -i renders/app/compose.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 $T
seg() { ffmpeg -v error -y -ss "$2" -t "$3" -i $T -an -vf "setpts=PTS/$4,fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "renders/app/seg/$1.mp4"; }
seg 1 37.3 0.3 1
seg 2 39.2 2.4 1.3
seg 3 46.3 1.0 1
seg 4 48.9 2.0 1
seg 5 56.4 1.5 1
printf "file 'seg/%s.mp4'\n" 1 2 3 4 5 > renders/app/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i renders/app/segs.txt -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 -t 6.646 hf/assets/app/compose.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/compose.mp4
