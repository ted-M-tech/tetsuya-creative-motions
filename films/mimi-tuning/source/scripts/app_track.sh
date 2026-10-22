#!/bin/sh
# Cut the simulator take into one track on the film's clock: hf/assets/app/app.mp4 starts at 4.1 s and runs 7.4 s.
# Source (not in Git): renders/app/tuning.mov (app-capture/TuningWalkthrough.swift + british-preview.patch; kept in Drive Tuning_assets/).
# First resampled to 60 fps (the simulator take is variable frame rate): renders/app/tuning-60.mp4. Measured on it:
#   AIボイス 32.5-38.8, 声の調整 tapped 38.8 (sheet 38.85-39.5) | 落ち着いて 43.65, ゆっくり 46.80, 穏やか 49.90 | request field tapped ~57.0
#   | typing「イギリス英語っぽく」60-77: the software keyboard pops up and down between characters, so the film steps through one
#   keyboard-free frame per character: 60.5 62.5 64.5 66.4 68.3 70.2 72.3 74.6 76.8 (試聴音声を作る visible; never tapped)
#   | relaunch with --qa-voice-generated: すべてのボイス with the 落ち着いて preview selected 106.5-111.5
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/tuning-60.mp4 ] || ffmpeg -v error -y -i renders/app/tuning.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/tuning-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60[$4];"; }
still() { echo "[0:v]trim=$1:$(echo "$1+0.02" | bc),setpts=PTS-STARTPTS,fps=60,tpad=stop_mode=clone:stop_duration=$2,trim=0:$2[$3];"; }
ffmpeg -v error -y -i renders/app/tuning-60.mp4 -filter_complex "\
$(seg 38.25 38.85 1 a)$(seg 38.85 39.5 2 b)$(seg 43.3 50.3 5 c)$(seg 56.7 57.9 2 d)\
$(still 60.5 0.24 t1)$(still 62.5 0.24 t2)$(still 64.5 0.24 t3)$(still 66.4 0.24 t4)$(still 68.3 0.24 t5)$(still 70.2 0.24 t6)$(still 72.3 0.24 t7)$(still 74.6 0.24 t8)$(still 76.8 0.94 t9)\
$(seg 107.5 109.115 1 r)\
[a][b][c][d][t1][t2][t3][t4][t5][t6][t7][t8][t9][r]concat=n=14:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
