#!/bin/sh
# Cut the Mimi report from the simulator take into one track on the film's clock: hf/assets/app/app.mp4 starts at 3.9 s and runs 6.4 s.
# Source (not in Git): renders/app/loop.mov, the --qa-mimi take recorded for films/mimi-loop (branch feat/mimi-loop,
#   app-capture/LoopWalkthrough.swift; Lanclo 03ea125d), kept in Drive 002.SNS/018. One Loop in Lanclo/Loop_assets/ and copied to
#   024. Mimi Is Always Watching/Watching_assets/. Resampled to 60 fps CFR first (renders/app/loop-60.mp4).
# Measured on contact sheets of loop-60.mp4 (seconds):
#   13.0-17.0  Mimiのアドバイス top: 10月20日(火)のまとめ, 次回 20:00, あなたの癖 > ボキャブラリー 1 "And then" 4回
#   19.0-20.6  scroll | 21.0-24.0 発音 1 /l/ 録音4 (and 単語の強勢 録音2), Mimi's bubble | 24.4-26.4 scroll
#   26.5-30.5  1 "And then": あなた "And then we went to the station." > ほかの言い方 "After that," / ", so" / "Later that day,"
#   30.6-38.6  scrolls through "good" and the diary rewrites | 39.0-40.5 ネイティブなら "After lunch, Ken and I headed to the station."
# Film clock: a 3.9-5.1 top | b 5.1-5.9 scroll (2x) | c 5.9-7.1 発音 | d 7.1-7.6 scroll (4x), 7.6-8.5 ほかの言い方
#   | e 8.5-9.0 fast scroll (16x), 9.0-10.3 ネイティブなら
set -e
cd "$(dirname "$0")/.."
A=renders/app
[ -f $A/loop-60.mp4 ] || ffmpeg -v error -y -i $A/loop.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 14 -preset fast $A/loop-60.mp4
mkdir -p hf/assets/app
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60[$4];"; }
ffmpeg -v error -y -i $A/loop-60.mp4 -filter_complex "\
$(seg 14.0 15.2 1 a)$(seg 19.0 20.6 2 b)$(seg 21.3 22.5 1 c)$(seg 24.4 26.4 4 d)$(seg 26.6 27.5 1 e)$(seg 30.6 38.6 16 f)$(seg 39.1 40.4 1 g)\
[a][b][c][d][e][f][g]concat=n=7:v=1:a=0,trim=0:6.4,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
