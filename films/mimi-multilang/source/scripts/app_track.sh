#!/bin/sh
# Cut the simulator take into one track on the film's clock: hf/assets/app/app.mp4 starts at 5.7 s.
# Source (not in Git): renders/app/voice.mov (app-capture/MultilangWalkthrough.swift + voice-stub.patch; kept in Drive Multilang_assets/).
# First resampled to 60 fps (the simulator take is variable frame rate): renders/app/voice-60.mp4. Measured on it:
#   AIボイス / 将来の発音 in English settled 38.97 | 🌐 menu tapped 46.8 (opens 46.85-47.17) | Français tapped 53.33, 読み込み中… 53.4-54.4,
#   French passage 54.47 | 試聴 tapped 61.0, playing 61.35 (stub 0:04) | menu tapped 67.38 | 한국어 tapped 75.08, Korean passage 76.2
# Film times of the taps (hf/index.html, scripts/mix.py): 5.85 menu, 6.865 Français, 8.0 試聴, 12.28 menu, 13.09 한국어.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/voice-60.mp4 ] || ffmpeg -v error -y -i renders/app/voice.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/voice-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60[$4];"; }
ffmpeg -v error -y -i renders/app/voice-60.mp4 -filter_complex "\
$(seg 46.65 47.40 1 a)$(seg 52.90 53.30 1 b)$(seg 53.30 54.60 2 c)$(seg 54.60 55.00 1 d)$(seg 60.90 65.10 1 e)\
$(seg 67.20 67.90 1 f)$(seg 74.80 75.10 1 g)$(seg 75.10 76.30 1.5 h)$(seg 76.30 77.30 1 i)\
[a][b][c][d][e][f][g][h][i]concat=n=9:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
