#!/bin/sh
# 「積読」: record the daily lesson walkthrough and cut the clips the edit uses (times are in the take, checked on a contact sheet).
set -e
src="$(cd "$(dirname "$0")/.." && pwd)"; kit="$src/../../../kits/mimi-short/app-capture"
[ -f "$src/renders/app/daily.mov" ] || "$kit/capture.sh" "$src/app-capture/DemoWalkthrough.swift" DescribeUITests.swift \
  DescribeUITests/testDailyWalkthrough "$src/renders/app/daily.mov"
"$kit/cut.sh" "$src/renders/app/daily.mov" "$src/hf/assets/app" \
  home:42.0:43.6 lesson:44.0:46.4 rec:51.0:53.4 tip:58.4:60.4
