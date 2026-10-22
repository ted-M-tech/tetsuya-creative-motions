#!/bin/sh
# Cut the simulator take into one track on the film's clock: hf/assets/app/app.mp4 starts at 5.8 s.
# Source (not in Git): renders/app/topics.mov (app-capture/TopicsWalkthrough.swift; kept in Drive 031/Topics_assets).
# Resampled to 60 fps first (the simulator take is variable frame rate): renders/app/topics-60.mp4.
# Measured on it (scene changes): Home 25.9-33.0, Practice menu 33.0-40.7, roleplay scenes 40.9-48.35 (scroll 44.8-45.8),
# photo gallery 53.7-56.8, debate topics 61.8-68.8 (scroll 64.95-65.3), Home 70.7-80.8, today's lesson 80.8- (お手本 tapped ~83.3).
# home 28.0-29.4 | practice 36.0-36.7 | roleplay 41.2-42.6 + scroll 44.8-45.6 | photos 54.3-55.5 | debate 62.6-63.8 + 65.0-65.6
# | lesson 83.0-85.5 (お手本 pressed 84.0 -> film 14.1), then holds (film 13.1-17.8)
set -e
cd "$(dirname "$0")/.."
[ -f renders/app/topics-60.mp4 ] || ffmpeg -v error -y -i renders/app/topics.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/topics-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS,fps=60,tpad=stop_mode=clone:stop_duration=$3[$4];"; }
ffmpeg -v error -y -i renders/app/topics-60.mp4 -filter_complex "\
$(seg 28.0 29.4 0 a)$(seg 36.0 36.7 0 b)$(seg 41.2 42.6 0 c)$(seg 44.8 45.6 0 d)$(seg 54.3 55.5 0 e)$(seg 62.6 63.8 0 f)$(seg 65.0 65.6 0 g)$(seg 83.0 85.5 3 h)\
[a][b][c][d][e][f][g][h]concat=n=8:v=1:a=0,trim=0:12.0,setpts=PTS-STARTPTS,scale=1206:2622,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
