#!/bin/sh
# Cut the simulator take of the swipe walkthrough into one track on the film's clock: hf/assets/app/app.mp4 starts at 5.0 s.
# Source (not in Git): renders/app/swipe.mov = Lanclo Drive 002.SNS/014. Swipe Review/Swipe_assets/sim-swipe-review_fixture.mov, resampled to 60 fps CFR first
# (simctl records variable frame rate). Four swipes; each cut lands on the same card, so the joins are invisible:
#   right  27.8-29.9 at 1.25x (Bless your heart, meaning side; drag starts 28.0)  -> film 5.00-6.68
#   left   35.9-37.9 at 1.25x (Please leave the light on.; drag 36.2)             -> film 6.68-8.28
#   right  44.3-46.2 at 2x    (Please; drag 44.4; the quick one)                   -> film 8.28-9.23
#   up     52.2-55.6 at 1.25x (Thank you; drag 52.6; the "again" card comes back at 55.0) -> film 9.23-11.95
set -e
cd "$(dirname "$0")/.."
[ renders/app/swipe-60.mp4 -nt renders/app/swipe.mov ] || \
  ffmpeg -v error -y -i renders/app/swipe.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/swipe-60.mp4
mkdir -p hf/assets/app
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$4,fps=60[$3];"; }
ffmpeg -v error -y -i renders/app/swipe-60.mp4 -filter_complex "\
$(seg 27.8 29.9 a 1.25)$(seg 35.9 37.9 b 1.25)$(seg 44.3 46.2 c 2)$(seg 52.2 55.6 d 1.25)\
[a][b][c][d]concat=n=4:v=1:a=0,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 16 -preset medium hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
