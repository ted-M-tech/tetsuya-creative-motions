#!/bin/sh
# Cut the simulator import take into two tracks on the film's clock: hf/assets/app/app1.mp4 (8.6-9.9) and app2.mp4 (12.1-18.2).
# Source (not in Git): renders/app/flashcards.mov (app-capture/FlashcardsWalkthrough.swift + note-import.patch + 単語帳.csv,
# Lanclo origin/main 5998d20d; kept in Drive Flashcards_assets/). Resampled to 60 fps: renders/app/flashcards-60.mp4. Measured on it
# (ffmpeg scene detection + frames):
#   My Notes 26 (すべて 1) | menu 32 | CSVからノートを読み込む sheet settled 35.2, CSVファイルを選ぶ tapped 42.5 | picker 46.8,
#   このiPhone内 49.7, 単語帳 tapped -> preview 51.1 (新しく追加できるノート 10件, 10件を追加) | 10件を追加しました。 55.2
#   | closed: My Notes 59.1 (すべて 11, 単語帳 10) | 単語帳 list 63.7 | review card 68.0 "look forward to" | flipped 71.45
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/flashcards-60.mp4 ] || ffmpeg -v error -y -i renders/app/flashcards.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/flashcards-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS,fps=60[$3];"; }
ffmpeg -v error -y -i renders/app/flashcards-60.mp4 -filter_complex "$(seg 35.25 36.55 a)[a]format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app1.mp4
ffmpeg -v error -y -i renders/app/flashcards-60.mp4 -filter_complex "\
$(seg 51.2 52.5 a)$(seg 55.25 56.25 b)$(seg 59.2 60.2 c)$(seg 63.8 64.8 d)$(seg 68.1 69.9 e)\
[a][b][c][d][e]concat=n=5:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app2.mp4
for f in app1 app2; do ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/$f.mp4; done
