#!/bin/sh
# Cut the simulator debate take into one track on the film's clock: hf/assets/app/app.mp4 plays at film 3.4-11.0.
# Source (not in Git): renders/app/debate.mov (app-capture/DebateWalkthrough.swift + live-mic.patch; kept in Drive Debate_assets/).
# First resampled to 60 fps (the simulator take is variable frame rate): renders/app/debate-60.mp4. Measured on it:
#   ディベート練習 (themes) 34.25, お金と幸せ tapped 37.75 | 立場を選ぶ 38.0, 賛成 tapped 43.5 | 1/2 practice 43.75, record 47.0,
#   recording 47.25-54.9 (meter, 0:0x), send 55.2,「Mimiが回答を振り返っています…」55.25 | feedback 56.0: radar, 話した内容, 文法
#   (Money make → makes), 発音, よかったところ (62.9-64.2), 個別の改善ポイント, 回答全体のお手本 | 返答を録音する 78.4 -> 2/2 with
#   相手の意見 (rebuttal + question) 78.5 | record 82.75, recording to 91.4, send 91.6 | final feedback, 完了 92.0.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/debate-60.mp4 ] || ffmpeg -v error -y -i renders/app/debate.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 14 -preset fast renders/app/debate-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60[$4];"; }
# themes x4 | positions x1 (cut on the tap, before the push: the next screen shows デモデータ) | record + send x6 | phrasing feedback x1 | 2/2 with the opponent x1 | reply + send x8
ffmpeg -v error -y -i renders/app/debate-60.mp4 -filter_complex "\
$(seg 34.95 37.95 4 a)$(seg 42.45 43.45 1 b)$(seg 46.55 55.45 6 c)$(seg 62.95 64.15 1 d)$(seg 78.35 80.35 1 e)$(seg 82.6 91.9 8 f)\
[a][b][c][d][e][f]concat=n=6:v=1:a=0,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
