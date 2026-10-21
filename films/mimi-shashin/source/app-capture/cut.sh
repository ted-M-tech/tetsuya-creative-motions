#!/bin/sh
# 「写真で英語」: record the Describe walkthrough and cut the clips the edit uses (times are in the take, checked on a contact sheet).
set -e
src="$(cd "$(dirname "$0")/.." && pwd)"; kit="$src/../../../kits/mimi-short/app-capture"
[ -f "$src/renders/app/describe.mov" ] || "$kit/capture.sh" "$src/app-capture/DemoWalkthrough.swift" DescribeUITests.swift \
  DescribeUITests/testWalkthrough "$src/renders/app/describe.mov"
"$kit/cut.sh" "$src/renders/app/describe.mov" "$src/hf/assets/app" \
  menu:22.0:24.2 photos:24.2:26.2 cafe:29.9:32.9 result:38.4:40.9 fix:43.4:45.4 better:47.8:50.4
