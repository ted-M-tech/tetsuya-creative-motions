#!/bin/sh
# Cut the simulator daily-lesson take (the one recorded for 「積読」) onto the film's clock: hf/assets/app/app.mp4 starts at 1.4 s.
# Source (not in Git): renders/app/daily-60.mp4 = Drive 009. Unread Books - Daily Lesson/Mimi_06_Unread_Books_assets/daily-60.mp4
# still 44.0 (1.4-3.1) | lesson + score 44.0-46.4 (3.1-5.5) | recording 51.0-53.4 (5.5-7.9) | the sound to fix 58.4-60.4, holds (7.9-12.6)
set -e
cd "$(dirname "$0")/.."
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60,tpad=stop_mode=clone:stop_duration=$4[$5];"; }
ffmpeg -v error -y -i renders/app/daily-60.mp4 -filter_complex "\
$(seg 44.0 44.02 1 1.68 a)$(seg 44.0 46.4 1 0 b)$(seg 51.0 53.4 1 0 c)$(seg 58.4 60.4 1 2.7 d)\
[a][b][c][d]concat=n=4:v=1:a=0,trim=0:11.2,setpts=PTS-STARTPTS,scale=1206:2622,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
# the in-app settings walk, as in ① (Drive 011/AB1_assets/iphone-settings_action-button.mov)
ffmpeg -v error -y -i renders/app/settings.mov -vf "setpts=PTS/2,fps=60,tpad=stop_mode=clone:stop_duration=0.35,format=yuv420p" -an -c:v libx264 -crf 16 hf/assets/app/settings.mp4
