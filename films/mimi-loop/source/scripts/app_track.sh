#!/bin/sh
# Cut the three simulator takes into one track on the film's clock: hf/assets/app/app.mp4 starts at 6.3 s (the loop) and runs 20.7 s.
# Sources (not in Git, all 1206x2622, resampled to 60 fps CFR):
#   renders/app/daily-60.mp4  Drive 002.SNS/009. Unread Books - Daily Lesson/Mimi_06_Unread_Books_assets/daily-60.mp4 (mimi-daily take)
#   renders/app/swipe-60.mp4  Drive 002.SNS/014. Swipe Review/Swipe_assets/sim-swipe-review_fixture.mov at 60 fps (mimi-swipe take)
#   renders/app/loop.mov      app-capture/LoopWalkthrough.swift (this film; Drive 018/Loop_assets) -> loop-60.mp4
# Measured on contact sheets (seconds in each take):
#   daily  50.5-53.4 recording (お手本 / 録音 / 自分) | 44.0-46.4 the five-angle radar (音・単語の強勢・リズム・抑揚・流暢さ)
#   loop   14.0-15.2 Mimiのアドバイス top (あなたの癖) | 38.6-40.0 「ネイティブなら」 rewrites | 55.0-56.4 journal: Mimiによる添削
#          92.0-93.4 roleplay: シチュエーション完了 | 102.5-104.9 lesson overview (Mimiが気づいた…) | 133.8-135.4 学習記録 trend,
#          137.0-137.8 the same with 音 highlighted
#   swipe  35.8-38.0 left swipe「Please leave the light on.」(もう一度)
# Film clock (app.mp4 starts at 12.9 s, 13.6 s long): ① 12.9-14.7 | ② 14.7-16.4 | ③ 16.4-17.25 journal, 17.25-18.1 situation
#   | ④ 18.1-18.85, 18.85-19.8 | ⑤ 19.8-21.5 | ⑥ 21.5-22.65, 22.65-23.2 | ⑦ 23.2-24.9 | fast lap: stills 1/7 s x7 (24.9-25.9), trend 25.9-26.5
# bed.mp4 (the night scene's small phone, 29.2-32.1): four swipes from the swipe take at 2x, 2.9 s
set -e
cd "$(dirname "$0")/.."
A=renders/app
[ -f $A/loop-60.mp4 ] || ffmpeg -v error -y -i $A/loop.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 14 -preset fast $A/loop-60.mp4
mkdir -p hf/assets/app
# seg <input index> <start> <end> <label>: a piece at 1x; still <input> <time> <duration> <label>: a held frame
seg() { echo "[$1:v]trim=$2:$3,setpts=PTS-STARTPTS,fps=60[$4];"; }
still() { echo "[$1:v]trim=$2:$(echo "$2 + 0.02" | bc),setpts=PTS-STARTPTS,fps=60,tpad=stop_mode=clone:stop_duration=$3,trim=0:$3[$4];"; }
D=0; L=1; S=2
F="$(seg $D 50.5 52.3 a)$(seg $D 44.0 45.7 b)$(seg $L 55.0 55.85 c)$(seg $L 92.0 92.85 d)$(seg $L 14.0 14.75 e)$(seg $L 38.6 39.55 f)"
F="$F$(seg $L 102.5 104.2 g)$(seg $L 133.8 134.95 h)$(seg $L 137.0 137.55 i)$(seg $S 36.0 37.7 j)"
n=0; list="[a][b][c][d][e][f][g][h][i][j]"
for spec in "$D 52.0" "$D 45.0" "$L 55.5" "$L 39.0" "$L 103.5" "$L 134.5" "$S 36.0"; do
  set -- $spec; F="$F$(still $1 $2 0.142857 m$n)"; list="$list[m$n]"; n=$((n + 1))
done
F="$F$(still $L 137.5 0.62 z)"; list="$list[z]"
ffmpeg -v error -y -i $A/daily-60.mp4 -i $A/loop-60.mp4 -i $A/swipe-60.mp4 -filter_complex \
  "$F${list}concat=n=$((n + 11)):v=1:a=0,trim=0:13.6,setpts=PTS-STARTPTS,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
sw() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/2,fps=60[$3];"; }
ffmpeg -v error -y -i $A/swipe-60.mp4 -filter_complex "$(sw 27.9 29.9 p)$(sw 36.0 37.9 q)$(sw 44.3 46.0 r)$(sw 52.5 54.6 s)[p][q][r][s]concat=n=4:v=1:a=0,trim=0:2.9,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/bed.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
