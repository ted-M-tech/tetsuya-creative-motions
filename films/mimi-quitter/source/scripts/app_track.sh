#!/bin/sh
# Cut the simulator take into the film's three app clips (hf/assets/app/*.mp4) and copy the widget artwork from the app.
# Source (not in Git): renders/app/quitter.mov (app-capture/QuitterWalkthrough.swift + month-streak.patch, Lanclo 5998d20d),
# kept in Drive 029/Quitter_assets/. The take is resampled to 60 fps first (simulator recordings are variable frame rate).
# Measured on quitter-60.mp4: lesson overview 12.6-17.5, Mimi's report top 29.5-33.5, Home 49.5-62, Progress (学習記録) 65.5-72.5.
set -e
cd "$(dirname "$0")/.."
mkdir -p hf/assets/app
[ -f renders/app/quitter-60.mp4 ] || ffmpeg -v error -y -i renders/app/quitter.mov -an -vf fps=60 -c:v libx264 -pix_fmt yuv420p -crf 16 renders/app/quitter-60.mp4
clip() { ffmpeg -v error -y -ss "$2" -i renders/app/quitter-60.mp4 -t "$3" -an -vf "fps=60,scale=1206:2622,format=yuv420p" -c:v libx264 -crf 16 "hf/assets/app/$1.mp4"; }
clip lesson 13.5 1.7      # the daily lesson the widget opens (overview)
clip report 30.5 2.2      # Mimi's daily report: the habits ranking
clip home 51.0 2.6        # Home: the 30-day streak (flame, top right) and the week strip
# widget artwork, as in the app's widget asset catalog
R=${LANCLO_REPO:-$HOME/Develop/native-voice-clone}
for f in MimiListening.imageset/listening-poster.png MimiArtist.imageset/artist.png MimiJournal.imageset/MimiJournal.svg MimiAdd.imageset/MimiAdd.svg; do
  git -C "$R" show origin/main:native-ios/LancloWidgets/Assets.xcassets/$f > hf/assets/app/w-$(basename $f)
done
ls hf/assets/app
