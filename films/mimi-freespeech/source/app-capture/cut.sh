#!/bin/sh
# 「3分、話しつづけて」: record the free-speech walkthrough (only if the take is missing) and cut the two clips the edit uses.
# Times are frame numbers / 60 in the 60 fps resample of the take (renders/app/describe-60.mp4), read from frame-indexed sheets
# (select='between(n,A,B)*not(mod(n,15))'; seeking with -ss before a tile filter drifted by ~2 s):
#   splash to 36.2 | cafe photo, 最大 3:00 under the record button 36.25-39.0+ | fixture take pill, then 採点中 ~52.5
#   | feedback top (five-axis radar 66, 話した内容) from 53.0 | slow scrolls later. App origin/main e33cd888.
set -e
src="$(cd "$(dirname "$0")/.." && pwd)"; kit="$src/../../../kits/mimi-short/app-capture"
[ -f "$src/renders/app/describe.mov" ] || "$kit/capture.sh" "$src/app-capture/FreeSpeechWalkthrough.swift" DescribeUITests.swift \
  DescribeUITests/testFreeSpeechWalkthrough "$src/renders/app/describe.mov"
"$kit/cut.sh" "$src/renders/app/describe.mov" "$src/hf/assets/app" photo:36.4:38.45 result:53.1:56.05
