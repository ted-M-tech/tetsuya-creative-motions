#!/bin/sh
# Cut the simulator mock-exam take into one track on the film's clock: hf/assets/app/app.mp4 starts at 2.8 s.
# Source (not in Git): renders/app/mock.mov (app-capture/MockWalkthrough.swift; kept in Drive 016/IELTS_assets).
# It is resampled to 60 fps first (the simulator take is variable frame rate): renders/app/mock-60.mp4.
# Measured on it: mock overview 37.7 | Q1 43.7, recording 48.3, stopped 52.4 | Q2 55.2 | Q3 67.0 | Q4 78.9 | Q5 90.7
# | Q6 102.7 | Q7 (Part 2) 114.7, preparing 119.8 | Q8 130.7 | Q9 142.4 | finished 154.4 | Band + answers 164.7 | Q1 feedback 175.0
# Film: overview 2.8-3.6 | Q1 3.6-4.4 | recording 4.4-5.1 | Q2 5.1, Q4 5.35, Q7 5.6 (0.4), Q8 6.0, Q9 6.25 | finished, tap 6.97, Band 6.5-8.0 | feedback 8.0-9.4
set -e
cd "$(dirname "$0")/.."
[ -f renders/app/mock-60.mp4 ] || ffmpeg -v error -y -i renders/app/mock.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/mock-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS,fps=60[$3];"; }
mkdir -p hf/assets/app
ffmpeg -v error -y -i renders/app/mock-60.mp4 -filter_complex "\
$(seg 38.0 38.8 a)$(seg 43.8 44.6 b)$(seg 48.4 49.1 c)$(seg 55.3 55.55 d)$(seg 78.9 79.15 e)$(seg 114.8 115.2 g)\
$(seg 130.8 131.05 h)$(seg 142.5 142.75 i)$(seg 158.7 160.2 j)$(seg 175.3 176.7 k)\
[a][b][c][d][e][g][h][i][j][k]concat=n=10:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
