#!/bin/sh
# Cut the simulator take into the film's app clips (hf/assets/app/*.mp4) on the film clock (app beat 9.4-13.8 s).
# Source (not in Git): renders/app/slang.mov (app-capture/SlangWalkthrough.swift, no patch, Lanclo origin/main), kept in
# Drive 070/Slang3_Ghosted_assets/. The take is resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on slang-60.mp4 (scene changes): the app opened straight on the スラング・カジュアル unit list (8.8; the deck list
# left no frames), slow swipe 20.2-22.5, unit list still 22.5-23.5 (ユニット8 tapped 23.53), unit 8 top from 25.4, fast scroll
# 43.3-44.8 brings the "ghost" card to the top, save tapped 46.48 (tag menu 46.5-52.4), bookmark filled 52.45-56.2,
# swipe to "leave sb on read" 56.2-58.5.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/slang-60.mp4 ] || ffmpeg -v error -y -i renders/app/slang.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/slang-60.mp4
clip() { ffmpeg -v error -y -ss "$2" -i renders/app/slang-60.mp4 -t "$3" -an -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "hf/assets/app/$1.mp4"; }
clip units 22.5 1.05      # スラング・カジュアル: units 5-10 (counts masked in the edit), ユニット8 tapped at the end
clip unit 25.45 0.5       # ユニット8 SNS・ネット文化: DM …
clip scroll 43.5 0.9      # the real scroll to the "ghost" card
clip card 45.85 0.6       # the "ghost" card at the top, save tapped at 46.45
clip saved 52.5 1.35      # the bookmark filled
ls hf/assets/app
