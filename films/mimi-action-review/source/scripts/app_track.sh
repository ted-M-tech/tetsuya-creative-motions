#!/bin/sh
# Cut the simulator review take into one track on the film's clock: hf/assets/app/app.mp4 starts at 1.4 s (screen opens).
# Source (not in Git): renders/app/review.mov (app-capture/ReviewWalkthrough.swift, kept in Drive 012/AB2_assets).
# Source is first resampled to 60 fps (the simulator take is variable frame rate): renders/app/review-60.mp4.
# Measured on it: Bless front 16.5-20.5, meaning 21.0-28.5 (rated 28.5), Please leave front 29.0-30.5, meaning 31.0-38.5,
# Please front 39.0-40.5, meaning 41.0-48.5, Thank you front 49.0-50.0, meaning 50.5-57.5.
# still 16.6 (1.4-3.1) | Bless front 16.6-18.6 at 2x | flip 20.6-21.4 | meaning 21.4-22.6 | rated + next 28.4-29.6
# | flip 30.6-31.6 | Please 38.4-39.6 at 1.5x | meaning 40.8-41.6 | Thank you 48.4-49.6 at 1.5x | meaning 50.4-51.2, holds
set -e
cd "$(dirname "$0")/.."
[ -f renders/app/review-60.mp4 ] || ffmpeg -v error -y -i renders/app/review.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/review-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60,tpad=stop_mode=clone:stop_duration=$4[$5];"; }
ffmpeg -v error -y -i renders/app/review-60.mp4 -filter_complex "\
$(seg 16.6 16.62 1 1.68 a)$(seg 16.6 18.6 2 0 b)$(seg 20.6 21.4 1 0 c)$(seg 21.4 22.6 1 0 d)$(seg 28.4 29.6 1 0 e)$(seg 30.6 31.6 1 0 f)$(seg 38.4 39.6 1.5 0 g)$(seg 40.8 41.6 1 0 h)$(seg 48.4 49.6 1.5 0 i)$(seg 50.4 51.2 1 1.1 j)\
[a][b][c][d][e][f][g][h][i][j]concat=n=10:v=1:a=0,trim=0:11.2,setpts=PTS-STARTPTS,scale=1206:2622,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
# the in-app settings walk, as in ① (Drive 011/AB1_assets/iphone-settings_action-button.mov)
ffmpeg -v error -y -i renders/app/settings.mov -vf "setpts=PTS/2,fps=60,tpad=stop_mode=clone:stop_duration=0.35,format=yuv420p" -an -c:v libx264 -crf 16 hf/assets/app/settings.mp4
