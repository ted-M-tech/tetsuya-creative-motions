#!/bin/sh
# Cut the owner's iPhone screen recording (Action Button -> Add phrase -> "Bless your heart" -> Generate meaning / example)
# into one track on the film's clock: hf/assets/app/app.mp4 starts at 0.6 s (when tiny Mimi opens the screen).
# Source (not in Git): renders/app/iphone.mov = Lanclo Drive 002.SNS/011. Action Button 1 - Add a Phrase/AB1_assets/iphone-add-phrase_bless-your-heart.mov
# Segments (source s -> film s): still 3.2 (0.6-2.2) | typing 3.3-8.6 at 4x, then holds (2.2-4.4) | tap meaning 8.9-9.5 (4.4-5.0)
#   | meaning appears 12.4-13.0 then holds (5.0-9.6) | tap example 13.0-13.6 (9.6-10.2) | example 19.9-20.6 then holds (10.2-13.0)
set -e
cd "$(dirname "$0")/.."
seg() { echo "[0:v]trim=$1:$2,setpts=(PTS-STARTPTS)/$3,fps=60,tpad=stop_mode=clone:stop_duration=$4[$5];"; }
ffmpeg -v error -y -i renders/app/iphone.mov -filter_complex "\
$(seg 3.2 3.22 1 1.58 a)$(seg 3.3 8.6 4 0.875 b)$(seg 8.9 9.5 1 0 c)$(seg 12.4 13.0 1 4.0 d)$(seg 13.0 13.6 1 0 e)$(seg 19.9 20.6 1 2.1 f)\
[a][b][c][d][e][f]concat=n=6:v=1:a=0,trim=0:12.4,setpts=PTS-STARTPTS,scale=1206:2622,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -crf 16 -preset medium hf/assets/app/app.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/app.mp4

# The in-app settings walk (Home > gear > 言語と学習 > アクションボタン) at 2x, then the last screen holds: hf/assets/app/settings.mp4
# Source (not in Git): renders/app/settings.mov = Drive .../011. Action Button 1 - Add a Phrase/AB1_assets/iphone-settings_action-button.mov
ffmpeg -v error -y -i renders/app/settings.mov -vf "setpts=PTS/2,fps=60,tpad=stop_mode=clone:stop_duration=0.35,format=yuv420p" -an -c:v libx264 -crf 16 hf/assets/app/settings.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 hf/assets/app/settings.mp4
