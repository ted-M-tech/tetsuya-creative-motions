#!/bin/sh
# Cut the montage clips (one per feature) from earlier films' simulator takes; each clip 2.2 s at 1x, 60 fps.
# Sources (not in Git; copied from Lanclo Drive, each resampled to 60 fps first because the takes are variable frame rate):
#   renders/app/describe.mov  021. Keep Talking for 3 Minutes/FreeSpeech_assets/simulator_free-speech-describe.mov
#                             (photo description, 最大 3:00 under the record button from 36.25)
#   renders/app/debate.mov    019. Lost an Argument in English/Debate_assets/sim-debate_fixture.mov (recording 47.25-54.9)
#   renders/app/roleplay.mov  017. Roleplay - Frozen at the Cafe/Roleplay_assets/sim-roleplay-cafe_fixture.mov (hint opens 45.7)
#   renders/app/loop.mov      018. One Loop in Lanclo/Loop_assets/sim-loop_..._fixture.mov (journal feedback, scroll to Mimiによる添削 ~51.5)
#   renders/app/daily-60.mp4  009. Unread Books - Daily Lesson/Mimi_06_Unread_Books_assets/daily-60.mp4 (recording 52.5-)
# Measured on frame sheets of the 60 fps resamples (select every 30th frame).
set -e
cd "$(dirname "$0")/.."
A=renders/app
for f in describe debate roleplay loop; do
  [ -f $A/$f-60.mp4 ] || ffmpeg -v error -y -i $A/$f.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 14 -preset fast $A/$f-60.mp4
done
mkdir -p hf/assets/app
cut() { ffmpeg -v error -y -ss $3 -i $A/$1 -t 2.2 -an -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 hf/assets/app/$2.mp4; }
cut describe-60.mp4 photo 36.9
cut debate-60.mp4 debate 47.3
cut roleplay-60.mp4 roleplay 45.3
cut loop-60.mp4 journal 51.6
cut daily-60.mp4 daily 52.3
for f in photo debate roleplay journal daily; do echo $f $(ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/$f.mp4); done
