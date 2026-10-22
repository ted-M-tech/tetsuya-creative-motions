#!/bin/sh
# Cut the simulator import take into two tracks on the film's clock: hf/assets/app/app1.mp4 (4.0-5.3) and app2.mp4 (7.5-13.3).
# Source (not in Git): renders/app/import.mov (app-capture/ImportWalkthrough.swift + note-import.patch; kept in Drive Import_assets/).
# First resampled to 60 fps (the simulator take is variable frame rate): renders/app/import-60.mp4. Measured on it (scene changes):
#   My Notes 24.0 (すべて 1) | menu 29.0 | CSVからノートを読み込む sheet settled 31.7, CSVファイルを選ぶ tapped 38.9 | picker 最近使った項目 42.3,
#   このiPhone内 45.95, 旅行フレーズ tapped 50.55 | preview 51.12 (新しく追加できるノート 12件, 12件を追加) | 12件を追加しました。 54.72
#   | closed: My Notes 58.55 (すべて 13, 旅行 12) | 旅行 list 62.95 | review card 67.4 "Could I have the check?" | flipped 70.6
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/import-60.mp4 ] || ffmpeg -v error -y -i renders/app/import.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/import-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS,fps=60[$3];"; }
ffmpeg -v error -y -i renders/app/import-60.mp4 -filter_complex "$(seg 31.75 33.05 a)[a]format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app1.mp4
ffmpeg -v error -y -i renders/app/import-60.mp4 -filter_complex "\
$(seg 51.2 52.5 a)$(seg 54.75 55.75 b)$(seg 58.6 59.6 c)$(seg 62.97 63.97 d)$(seg 67.45 68.95 e)\
[a][b][c][d][e]concat=n=5:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app2.mp4
for f in app1 app2; do ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/$f.mp4; done
