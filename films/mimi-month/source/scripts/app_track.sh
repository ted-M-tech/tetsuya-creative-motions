#!/bin/sh
# Cut the simulator take into the five day clips (hf/assets/app/d*.mp4) on the film's clock.
# Source (not in Git): renders/app/month.mov (app-capture/MonthWalkthrough.swift + month-days.patch, Lanclo 5998d20d),
# kept in Drive 036/Month_assets/. Resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on month-60.mp4: day 1 report 12.5-21.5 (scrolled past the fixture's「デモデータ」label from 18.0),
# day 7 (10月27日) 27-34, day 14 (11月3日) 42-47, day 21 (11月10日) 59-64, day 30 (11月19日) 71-79.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/month-60.mp4 ] || ffmpeg -v error -y -i renders/app/month.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/month-60.mp4
clip() { ffmpeg -v error -y -ss "$2" -i renders/app/month-60.mp4 -t "$3" -an -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "hf/assets/app/$1.mp4"; }
clip d1 18.2 2.7
clip d7 28.0 2.7
clip d14 42.3 2.7
clip d21 59.2 2.5
clip d30 72.0 3.1
ls hf/assets/app
