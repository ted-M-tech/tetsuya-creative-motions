#!/bin/sh
# The home-screen take -> hf/assets/app/home.mp4 (2 s, the film's 21.9-23.9).
# The take is variable frame rate: resample to 60 fps first. On renders/app/home60.mp4 Home is settled from 38.0 s
# (springboard and launch before it; Settings › ヘルプとアプリ情報 from about 55 s, used only to check the labels).
set -e
cd "$(dirname "$0")/.."
ffmpeg -v error -y -i renders/app/home.mov -vf fps=60 -an renders/app/home60.mp4
mkdir -p hf/assets/app
ffmpeg -v error -y -ss 38.5 -i renders/app/home60.mp4 -t 2.0 -an -c:v libx264 -pix_fmt yuv420p -crf 16 -r 60 hf/assets/app/home.mp4
