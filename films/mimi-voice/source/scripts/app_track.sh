#!/bin/sh
# Cut the simulator voice-setup take into one track on the film's clock: hf/assets/app/app.mp4 starts at 5.5 s.
# Source (not in Git): renders/app/setup.mov (app-capture/VoiceSetupWalkthrough.swift + first-voice.patch; kept in Drive AIV_assets/).
# First resampled to 60 fps (the simulator take is variable frame rate): renders/app/setup-60.mp4. Measured on it:
#   声の登録 19.6 (toggles flip on 25.8 / 29.5 / 34.0 / 38.0, 続ける tapped 44.25) | 同意を録音 44.5, 録音 48.0, 録音の停止 53.75, 続ける 56.75
#   | 声のサンプル 57.0, 録音 60.5, 録音の停止 74.0 (13.5 s sample), 自分の声を作る shown 74.25 (not tapped) | relaunch: AIボイス 85.5-92 (clean)
# Opening the screen to 自分の声を作る: 19.6 -> 74.25 = 55 s of real time (the film's clock chip).
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/setup-60.mp4 ] || ffmpeg -v error -y -i renders/app/setup.mov -vf fps=60 -c:v libx264 -crf 14 -preset fast renders/app/setup-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60[$4];"; }
ffmpeg -v error -y -i renders/app/setup-60.mp4 -filter_complex "\
$(seg 19.6 19.75 1 a)$(seg 25.0 39.6 10 b)$(seg 43.9 44.7 2 c)$(seg 45.5 48.3 4 d)$(seg 48.3 54.1 8 e)$(seg 56.4 57.4 2 f)$(seg 58.0 60.9 4 g)$(seg 60.9 74.2 10 h)$(seg 74.2 74.9 1 i)$(seg 86.0 87.2 1 j)\
[a][b][c][d][e][f][g][h][i][j]concat=n=10:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
