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
# Film clock (app.mp4 starts at 13.85 s, 9.6 s long; the entrance stop before it is drawn in HTML), 1.25 s per stop:
#   lesson 13.85-15.1 | own-voice model 15.1-16.35 | Mimi's advice 16.35-16.95 (habits), 16.95-17.6 (「ネイティブなら」)
#   | save (the same rewrite card, its bookmark) 17.6-18.85 | swipe review 18.85-20.1 | study record 20.1-20.85, 20.85-21.35
#   | back to the lesson 21.35-22.55 | fast lap: stills 0.9/7 s x7 (22.55-23.45)
# bed.mp4 (the night scene's small phone, 25.75-28.85): four swipes from the swipe take at 2x, 3.1 s
set -e
cd "$(dirname "$0")/.."
A=renders/app
[ -f $A/loop-60.mp4 ] || ffmpeg -v error -y -i $A/loop.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 14 -preset fast $A/loop-60.mp4
mkdir -p hf/assets/app
# seg <input index> <start> <end> <label>: a piece at 1x; still <input> <time> <duration> <label>: a held frame
seg() { echo "[$1:v]trim=$2:$3,setpts=PTS-STARTPTS,fps=60[$4];"; }
still() { echo "[$1:v]trim=$2:$(echo "$2 + 0.02" | bc),setpts=PTS-STARTPTS,fps=60,tpad=stop_mode=clone:stop_duration=$3,trim=0:$3[$4];"; }
D=0; L=1; S=2
F="$(seg $L 102.0 103.25 a)$(seg $D 51.6 52.85 b)$(seg $L 14.0 14.6 c)$(seg $L 38.6 39.25 d)$(seg $L 39.25 40.5 e)"
F="$F$(seg $S 36.1 37.35 f)$(seg $L 134.0 134.75 g)$(seg $L 137.0 137.5 h)$(seg $L 102.0 103.2 i)"
n=0; list="[a][b][c][d][e][f][g][h][i]"
for spec in "$L 103.5" "$L 103.0" "$D 52.0" "$L 14.5" "$L 40.0" "$S 36.0" "$L 134.5"; do
  set -- $spec; F="$F$(still $1 $2 0.128571 m$n)"; list="$list[m$n]"; n=$((n + 1))
done
ffmpeg -v error -y -i $A/daily-60.mp4 -i $A/loop-60.mp4 -i $A/swipe-60.mp4 -filter_complex \
  "$F${list}concat=n=$((n + 9)):v=1:a=0,trim=0:9.6,setpts=PTS-STARTPTS,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
sw() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/2,fps=60[$3];"; }
ffmpeg -v error -y -i $A/swipe-60.mp4 -filter_complex "$(sw 27.9 29.9 p)$(sw 36.0 37.9 q)$(sw 44.3 46.0 r)$(sw 52.5 54.6 s)[p][q][r][s]concat=n=4:v=1:a=0,trim=0:3.1,setpts=PTS-STARTPTS,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/bed.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
