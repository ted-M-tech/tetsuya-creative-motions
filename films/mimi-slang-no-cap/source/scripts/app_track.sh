#!/bin/sh
# Cut the simulator take into the film's app clips (hf/assets/app/*.mp4) on the film clock (app beat 9.7-14.1 s).
# Source (not in Git): renders/app/slang.mov (app-capture/SlangWalkthrough.swift, no patch, Lanclo origin/main 1088ae0b),
# kept in Drive 068/Slang1_NoCap_assets/. The take is resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on slang-60.mp4 (scene changes): deck list 18.4-22.4 (スラング・カジュアル tapped ~22.2), units 22.43-26.4
# (ユニット3 tapped ~26.2), unit 3 top 26.4-26.9, the "no cap" card at the top from 27.0 (the fast swipes left no scroll
# frames in the recording), save tapped 63.6 (tag menu 63.8-67.0), bookmark filled 67.1-71, swipe to the "cap" card 71-72.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/slang-60.mp4 ] || ffmpeg -v error -y -i renders/app/slang.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/slang-60.mp4
clip() { ffmpeg -v error -y -ss "$2" -i renders/app/slang-60.mp4 -t "$3" -an -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "hf/assets/app/$1.mp4"; }
clip list 21.25 1.0       # 単語帳: the deck list (counts masked in the edit), スラング・カジュアル tapped at the end
clip units 25.35 0.9      # スラング・カジュアル: the units (counts masked in the edit), ユニット3 tapped at the end
clip unit 26.45 0.4       # ユニット3 賛成・反対・返事: yeah, yep …
clip scroll 27.5 0.6      # the "no cap" card (slides up in the edit: the scroll itself left no frames)
clip card 63.25 0.5       # the card, save tapped at 63.6
clip saved 67.2 1.0       # the bookmark filled
ls hf/assets/app
