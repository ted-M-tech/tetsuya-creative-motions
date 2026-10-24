#!/bin/sh
# The app track on the film's clock (28.3-32.6).
# Source (not in Git): a fresh take with app-capture/ModelWalkthrough.swift (2026-10-23, QA fixture, app origin/main 9ef0df1b),
# kept in Drive 067/Cloning_assets/sim-daily-model_fixture.mov -> renders/app/daily.mov; resampled to 60 fps: renders/app/daily-60.mp4.
# Measured on it: the daily lesson "Please leave the light on." is on screen from 27.0 (home before it, not used).
# app.mp4: 27.4-31.7. The middle of the screen (fixture scores and the 「QA用データ」 feedback) is covered by a label in hf/index.html.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/daily-60.mp4 ] || ffmpeg -v error -y -i renders/app/daily.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/daily-60.mp4
ffmpeg -v error -y -i renders/app/daily-60.mp4 -vf "trim=27.4:31.7,setpts=PTS-STARTPTS,fps=60,scale=1206:2622,format=yuv420p" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
echo app $(ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4)
