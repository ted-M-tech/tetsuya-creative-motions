#!/bin/sh
# Cut the simulator take into two tracks on the film's clock.
# Source (not in Git): renders/app/airport.mov (app-capture/RoleplayAirportWalkthrough.swift + airport-lines.patch; kept in Drive
# 032/FrozenAbroad_assets), first resampled to 60 fps (the simulator take is variable frame rate): renders/app/airport-60.mp4.
# Measured on it: catalogue 36.0, scrolled to 空港・交通・ホテル 40.5-43.3, 空港 tapped 43.4, airport scenes 44.0-47.2 (scene tapped 47.2),
# loading 47.6-53.9, partner "May I see your passport?" 54.0, meaning on 56.4, hint tapped 59.5 (cards 59.8), record tapped 63.0
# ("返答を準備しています…"), reply + シチュエーション完了 69.2, back to the catalogue 74.4, scroll 74.4-76.4.
# app.mp4 (film 8.5-14.3): catalogue 42.5-43.5 | airport scenes 46.6-47.4 | loading 47.6-48.0 | partner+meaning 56.0-57.0
#                          | hints 59.3-60.3 | record 62.7-63.3 | reply 69.15-70.15
# catalog.mp4 (film 18.4-19.7): the catalogue scrolling 74.4-76.0 at 1.25x
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/airport-60.mp4 ] || ffmpeg -v error -y -i renders/app/airport.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/airport-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS,fps=60[$3];"; }
ffmpeg -v error -y -i renders/app/airport-60.mp4 -filter_complex "\
$(seg 42.5 43.5 a)$(seg 46.6 47.4 b)$(seg 47.6 48.0 c)$(seg 56.0 57.0 d)$(seg 59.3 60.3 e)$(seg 62.7 63.3 f)$(seg 69.15 70.15 g)\
[a][b][c][d][e][f][g]concat=n=7:v=1:a=0,trim=0:5.8,setpts=PTS-STARTPTS,scale=1206:2622,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffmpeg -v error -y -i renders/app/airport-60.mp4 -vf "trim=74.4:76.0,setpts=(PTS-STARTPTS)/1.25,fps=60,tpad=stop_mode=clone:stop_duration=0.1,format=yuv420p" -an -c:v libx264 -crf 16 hf/assets/app/catalog.mp4
for f in app catalog; do echo $f $(ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/$f.mp4); done
