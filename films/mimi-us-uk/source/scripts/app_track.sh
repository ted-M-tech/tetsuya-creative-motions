#!/bin/sh
# Cut the simulator take into one track on the film's clock: hf/assets/app/app.mp4 starts at 12.0 s and runs 4.0 s.
# Source (not in Git): renders/app/tuning.mov — the take made for films/mimi-tuning (its app-capture/TuningWalkthrough.swift
# + british-preview.patch, Lanclo origin/main 57b4fc93; VoiceTuningEditor.swift unchanged up to 5998d20d), reused here.
# Kept in Drive 030. US vs UK English in My Own Voice/US_UK_assets/. Resampled to 60 fps: renders/app/tuning-60.mp4. Measured on it:
#   声の調整 sheet open, 落ち着いて tapped 43.65 | request field typing「イギリス英語っぽく」60-77, the software keyboard pops up and
#   down between characters, so the film steps through keyboard-free frames: 60.5 62.5 64.5 66.4 68.3 70.2 72.3 74.6 76.8
#   (試聴音声を作る visible; never tapped — it calls the voice provider)
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/tuning-60.mp4 ] || ffmpeg -v error -y -i renders/app/tuning.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/tuning-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60[$4];"; }
still() { echo "[0:v]trim=$1:$(echo "$1+0.02" | bc),setpts=PTS-STARTPTS,fps=60,tpad=stop_mode=clone:stop_duration=$2,trim=0:$2[$3];"; }
ffmpeg -v error -y -i renders/app/tuning-60.mp4 -filter_complex "\
$(seg 43.3 44.3 1 c)\
$(still 60.5 0.2 t1)$(still 62.5 0.2 t2)$(still 64.5 0.2 t3)$(still 66.4 0.2 t4)$(still 68.3 0.2 t5)$(still 70.2 0.2 t6)$(still 72.3 0.2 t7)$(still 74.6 0.2 t8)$(still 76.8 1.4 t9)\
[c][t1][t2][t3][t4][t5][t6][t7][t8][t9]concat=n=10:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
