#!/bin/sh
# Cut the simulator take into two tracks on the film's clock.
# Source (not in Git): renders/app/roleplay.mov (app-capture/RoleplayWalkthrough.swift; kept in Drive 017/Roleplay_assets),
# first resampled to 60 fps (the simulator take is variable frame rate): renders/app/roleplay-60.mp4.
# Measured on it: catalogue 20.7-24.0, scroll 24.0-24.9 / back 27.3-28.2, café tapped 30.15, café scenes 30.6-33.85 (task tapped),
# Mimi loading 34.3-40.4, partner line 40.5, meaning on 43.2, hint tapped 45.7, record tapped 49.2 (fixture take, "返答を準備しています…"),
# reply + シチュエーション完了 55.7, back to café 59.8, catalogue 61.7, scrolls 64.6-65.6 and 68.0-69.0.
# app.mp4 (film 4.3-10.6): catalogue 29.8-30.6 | café 33.7-34.3 | loading 34.5-35.0 | partner+meaning 42.6-43.8 | hints 45.3-46.5
#                          | record 48.8-49.6 | reply 55.55-56.75
# catalog.mp4 (film 15.3-16.6): the catalogue scrolling to more scenes 64.3-65.9 at 1.25x
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/roleplay-60.mp4 ] || ffmpeg -v error -y -i renders/app/roleplay.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/roleplay-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60[$4];"; }
ffmpeg -v error -y -i renders/app/roleplay-60.mp4 -filter_complex "\
$(seg 29.8 30.6 1 a)$(seg 33.7 34.3 1 b)$(seg 34.5 35.0 1 c)$(seg 42.6 43.8 1 d)$(seg 45.3 46.5 1 e)$(seg 48.8 49.6 1 f)$(seg 55.55 56.75 1 g)\
[a][b][c][d][e][f][g]concat=n=7:v=1:a=0,trim=0:6.3,setpts=PTS-STARTPTS,scale=1206:2622,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffmpeg -v error -y -i renders/app/roleplay-60.mp4 -vf "trim=64.3:65.9,setpts=(PTS-STARTPTS)/1.25,fps=60,tpad=stop_mode=clone:stop_duration=0.3,format=yuv420p" -an -c:v libx264 -crf 16 hf/assets/app/catalog.mp4
for f in app catalog; do echo $f $(ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/$f.mp4); done
