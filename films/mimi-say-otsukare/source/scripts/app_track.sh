#!/bin/sh
# Cut the simulator take onto the film's clock: hf/assets/app/compose.mp4 (6.69 s, film 4.3-10.99).
# Source (not in Git): renders/app/compose.mov (app-capture/ComposeWalkthrough.swift + compose-result.patch, Lanclo 5f5571ad),
# kept in Drive 064/Say2_Otsukaresama_assets/. Resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on compose-60.mp4: composer with caret 38.5; typing 40.0-42.0 (仕事終わ 40.1, お疲れ 41.3); フレーズを作成 tapped 46.7
# (生成を中止 46.8); 意味を選択 with the two real candidates 52.2 (settled 52.8); "Good work today!" picked ~60.45; the editable draft
# 60.65 (the walkthrough's save came 0.05 s later, so that frame is held 0.8 s); 保存 ~60.7; the list (saved phrase) 61.25.
# Film clock: seg1 caret 4.3-4.6 | seg2 typing x1.3 4.6-6.29 | seg3 create + loading 6.29-7.09 (tap 6.59) |
#             seg4 candidates 7.09-8.39 (in 7.29) | seg5 candidates + pick 8.39-9.09 (tap 8.89) | seg6 the draft, held 9.09-9.89 |
#             seg7 save + list 9.89-10.99 (tap 9.94, list 10.49). Waits are skipped.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app renders/app/seg
T=renders/app/compose-60.mp4
[ -f $T ] || ffmpeg -v error -y -i renders/app/compose.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 $T
seg() { ffmpeg -v error -y -ss "$2" -t "$3" -i $T -an -vf "setpts=PTS/$4,fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "renders/app/seg/$1.mp4"; }
seg 1 38.6 0.3 1
seg 2 39.8 2.2 1.3
seg 3 46.4 0.8 1
seg 4 52.0 1.3 1
seg 5 59.95 0.7 1
ffmpeg -v error -y -ss 60.65 -i $T -frames:v 1 renders/app/seg/draft.png
ffmpeg -v error -y -loop 1 -t 0.8 -i renders/app/seg/draft.png -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 renders/app/seg/6.mp4
seg 7 60.65 1.1 1
printf "file 'seg/%s.mp4'\n" 1 2 3 4 5 6 7 > renders/app/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i renders/app/segs.txt -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 -t 6.69 hf/assets/app/compose.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/compose.mp4
