#!/bin/sh
# Cut the simulator take onto the film's clock (hf/assets/app/app.mp4, see app-capture/app-track.json for the taps).
# Source (not in Git): renders/app/peace.mov (capture.sh + app-capture/Walkthrough.swift + PATCH=app-capture/peace-lesson.patch),
# kept in Drive as <prefix>_assets/peace-lesson-take.mov; resampled to 60 fps first (simctl records variable frame rate).
#   SEG_A  the sentence with its score (お手本 tapped 0.6 s in)
#   SEG_B  the record button pressed
#   SEG_C  the flagged word row (Model / Your voice / Practice / Save). Stop before the offline fixture shows its scoring error.
set -e
cd "$(dirname "$0")/.."
. app-capture/segments.sh
[ -f renders/app/peace-60.mp4 ] || ffmpeg -v error -y -i renders/app/peace.mov -vf fps=60 -an -c:v libx264 -crf 16 -pix_fmt yuv420p renders/app/peace-60.mp4
seg() { echo "[0:v]trim=$1:$2,setpts=PTS-STARTPTS[$3];"; }
mkdir -p hf/assets/app
ffmpeg -v error -y -i renders/app/peace-60.mp4 -filter_complex "\
$(seg $SEG_A a)$(seg $SEG_B b)$(seg $SEG_C c)[a][b][c]concat=n=3:v=1:a=0,fps=60,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4
