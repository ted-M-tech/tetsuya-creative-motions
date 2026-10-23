#!/bin/sh
# Cut the simulator take into the film's app clips (hf/assets/app/*.mp4) on the film clock (5.5-12.2 s).
# Source (not in Git): renders/app/decks.mov (app-capture/DecksWalkthrough.swift, no patch, Lanclo origin/main 5f5571ad),
# kept in Drive 065/Decks_ImFine_assets/. The take is resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on decks-60.mp4: deck list 28.0-31.5, slang units 32.5-35.5, unit 4 top 36.5-46.5, scrolling 47-92,
# the "all good" card settled 128.5, save tapped 128.75 (tag menu 129.0-132.4), bookmark filled 132.75-136.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/decks-60.mp4 ] || ffmpeg -v error -y -i renders/app/decks.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/decks-60.mp4
clip() { ffmpeg -v error -y -ss "$2" -i renders/app/decks-60.mp4 -t "$3" -an -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "hf/assets/app/$1.mp4"; }
clip list 28.2 1.5        # 単語帳: the deck list (counts masked in the edit)
clip units 32.6 1.2       # スラング・カジュアル: the units (counts masked in the edit)
clip unit4 36.6 0.8       # ユニット4 あいさつ・お礼・謝罪: what's up …
# the scroll down the unit, 45 s of the take in 1.0 s
ffmpeg -v error -y -ss 47 -i renders/app/decks-60.mp4 -t 45 -an -vf "setpts=PTS/45,fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 hf/assets/app/scroll.mp4
clip card 128.4 0.7       # the "all good" card, save tapped
clip saved 132.6 1.5      # the bookmark filled
ls hf/assets/app
