#!/bin/sh
# Cut the simulator take into the film's app clips (hf/assets/app/*.mp4) on the film clock (app beat 10.1-14.5 s).
# Source (not in Git): renders/app/slang.mov (app-capture/SlangWalkthrough.swift, no patch, Lanclo origin/main ff11569c),
# kept in Drive 069/Slang2_Hangry_assets/. The take is resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on slang-60.mp4 (scene changes + frames): deck list 30.05-34.3 (スラング・カジュアル tapped ~34.3), units 34.8-39.1
# (ユニット6 tapped ~39.05, the row sits at the bottom, its count line ghosts under the tab bar), unit 6 top 39.6-43.8,
# swipes 43.8-74.9, the "hangry" card mid-screen 74.9-90.95, dragged to the top 90.95-91.55, save tapped ~96.05
# (tag menu 96.2-100.1), bookmark filled 100.15-104, swipe to "I'm dead" 104.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/slang-60.mp4 ] || ffmpeg -v error -y -i renders/app/slang.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/slang-60.mp4
clip() { ffmpeg -v error -y -ss "$2" -i renders/app/slang-60.mp4 -t "$3" -an -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "hf/assets/app/$1.mp4"; }
clip list 33.35 1.0       # 単語帳: the deck list (counts masked in the edit), スラング・カジュアル tapped at the end
clip units 38.2 0.9       # スラング・カジュアル: the units (counts masked; the tab bar is patched), ユニット6 tapped at the end
clip unit 40.0 0.4        # ユニット6 気分・テンション: chill, vibe …
clip scroll 90.95 0.6     # the "hangry" card dragged up to the top (real scroll)
clip card 95.6 0.5        # the card, save tapped at 96.05
clip saved 100.2 1.0      # the bookmark filled
# a clean tab bar (from the deck list, nothing behind it) to cover unit 6's count line ghosting under the glass bar
ffmpeg -v error -y -ss 33.9 -i renders/app/slang-60.mp4 -frames:v 1 -vf "crop=1078:182:64:2374" hf/assets/app/tabbar.png
ls hf/assets/app
