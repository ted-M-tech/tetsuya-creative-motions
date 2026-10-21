#!/bin/sh
# Real screens -> hf/assets/app/ (JPEG, film sizes). Web: renders/web/*.png (web-capture/*.ts); iOS: two frames of the mimi-loop take.
# The roleplay frame's 「デモデータ」 label is painted over with the screen's own background colour.
set -e
F=$(cd "$(dirname "$0")/.." && pwd); O=$F/hf/assets/app; mkdir -p $O
magick $F/renders/app/ios-roleplay.png -fill 'rgb(239,239,243)' -draw 'rectangle 50,405 260,470' -resize 600x -quality 92 $O/phone-study.jpg
magick $F/renders/app/ios-mimi-report.png -resize 600x -quality 92 $O/phone-report.jpg
magick $F/renders/web/laptop-habits.png -resize 1440x -quality 90 $O/web-home.jpg
magick $F/renders/web/laptop-habits-full.png -resize 1440x -quality 90 $O/web-home-full.jpg
magick $F/renders/web/tablet-practice.png -resize 1366x -quality 90 $O/web-practice.jpg
ls -la $O
