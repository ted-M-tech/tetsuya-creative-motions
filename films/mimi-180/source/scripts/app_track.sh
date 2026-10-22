#!/bin/sh
# Cut the simulator take into one track on the film's clock: hf/assets/app/app.mp4 starts at 9.1 s.
# Source (not in Git): renders/app/really.mov (app-capture/ReallyWalkthrough.swift + really-take.patch; kept in Drive 033/Talked180_assets).
# Resampled to 60 fps first (the simulator take is variable frame rate): renders/app/really-60.mp4.
# Measured on it (scene changes): the new result (score 58, transcript start) 32.2-36.57, transcript in full + grammar 36.57-41.3,
# 個別の改善ポイント (really, really -> absolutely lovely) at the top 41.3-46.07, then the card higher with the model answer 46.07-49.33.
# film 9.1 result 32.6-34.1 | 10.6 transcript 36.9-38.3 | 12.0 correction 41.6-43.7 | 14.1 (hidden behind the gag) 43.7-45.7
# | 16.1 correction card 46.3-49.0
set -e
cd "$(dirname "$0")/.."
[ -f renders/app/really-60.mp4 ] || ffmpeg -v error -y -i renders/app/really.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/really-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS,fps=60[$3];"; }
ffmpeg -v error -y -i renders/app/really-60.mp4 -filter_complex "\
$(seg 32.6 34.1 a)$(seg 36.9 38.3 b)$(seg 41.6 43.7 c)$(seg 43.7 45.7 d)$(seg 46.3 49.0 e)\
[a][b][c][d][e]concat=n=5:v=1:a=0,trim=0:9.7,setpts=PTS-STARTPTS,scale=1206:2622,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
