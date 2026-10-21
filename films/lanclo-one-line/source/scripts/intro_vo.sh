#!/bin/sh
# Cut the Mimi (Kansai) narration take into lines v1..v10 at 1.2x (pitch kept).  usage: scripts/intro_vo.sh
# Source: Drive 002.SNS/010. アプリ紹介/Mimi.m4a -> assets/voice/vo-intro/Mimi.m4a
set -e
# Each cut ends ~0.12 s after the line's last sound (silencedetect -40 dB) so no tail is clipped.
cd "$(dirname "$0")/../assets/voice/vo-intro"
ffmpeg -v error -y -i Mimi.m4a -ac 1 -ar 48000 mimi.wav
while read k a b; do
  ffmpeg -v error -y -i mimi.wav -af "atrim=$a:$b,asetpts=PTS-STARTPTS,atempo=1.2,afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse" "$k.wav"
done <<CUTS
v1 0.30 2.33
v2 2.64 5.11
v3 5.48 8.08
v4 9.69 13.01
v5 13.47 15.89
v6 16.52 18.43
v7 18.90 23.35
v8 23.80 25.68
v9 25.99 27.60
v10 27.86 30.30
CUTS
