#!/bin/sh
# Cut the simulator take onto the film's clock (hf/assets/app/app.mp4, 4.9 s from 9.1 s).
# Source (not in Git): renders/app/recheck.mov (capture.sh + app-capture/Walkthrough.swift + PATCH=app-capture/recheck-row.patch,
# Lanclo 5f5571ad), kept in Drive 066. The R Came Back/Recheck_R_assets/recheck-overview-take.mov; resampled to 60 fps first.
# Measured on recheck-60.mp4: the overview is settled 12.0-20.5; row 5 「/ɹ/ (right) · 再確認」 sits at 66.5-74 % of the screen height.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/recheck-60.mp4 ] || ffmpeg -v error -y -i renders/app/recheck.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/recheck-60.mp4
ffmpeg -v error -y -ss 13.0 -i renders/app/recheck-60.mp4 -t 4.9 -an -vf "fps=60,format=yuv420p" -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
