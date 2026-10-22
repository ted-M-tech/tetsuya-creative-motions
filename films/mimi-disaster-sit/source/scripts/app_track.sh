#!/bin/sh
# Cut the simulator take onto the film's clock: hf/assets/app/app.mp4 runs 11.0-15.1.
# Source (not in Git): renders/app/sit.mov (capture.sh + SitWalkthrough.swift + PATCH=sit-lesson.patch) -> renders/app/sit-60.mp4
#   39.0-40.9 "Please sit down." with the score (11.0-12.9; お手本 tapped at 11.6)
#   46.15-46.75 the record button pressed (12.9-13.5; tap at 13.0)
#   52.9-54.5 the sound to fix: sit /sɪt/ (13.5-15.1). Stop before 54.6: the offline fixture then shows a scoring error.
set -e
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i renders/app/sit.mov -vf fps=60 -an -c:v libx264 -crf 16 renders/app/sit-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS[$3];"; }
mkdir -p hf/assets/app
ffmpeg -v error -y -i renders/app/sit-60.mp4 -filter_complex "\
$(seg 39.0 40.9 a)$(seg 46.15 46.75 b)$(seg 52.9 54.5 c)[a][b][c]concat=n=3:v=1:a=0,fps=60,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
