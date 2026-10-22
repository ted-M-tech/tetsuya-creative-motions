#!/bin/sh
# The app track on the film's clock (6.6-10.6).
# Source (not in Git): the daily-lesson take recorded for films/mimi-daily (app-capture/DemoWalkthrough.swift there, 2026-10-20, QA fixture),
# kept in Drive 035/NoShadowing_assets/sim-daily-model_fixture.mov; resampled to 60 fps: renders/app/daily-60.mp4.
# (A fresh take with app-capture/ModelWalkthrough.swift was queued for an hour on the shared simulator lock and not recorded.)
# Measured on it: lesson "Please leave the light on." 44.0, お手本 tapped 46.6 (button dims while the model plays, 46.7-49.6).
# app.mp4: 45.6-49.6
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/daily-60.mp4 ] || ffmpeg -v error -y -i renders/app/daily.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/daily-60.mp4
ffmpeg -v error -y -i renders/app/daily-60.mp4 -vf "trim=45.6:49.6,setpts=PTS-STARTPTS,fps=60,scale=1206:2622,format=yuv420p" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
echo app $(ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4)
