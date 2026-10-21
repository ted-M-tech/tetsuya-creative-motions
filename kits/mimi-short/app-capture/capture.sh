#!/bin/sh
# Record the real Lanclo app in the simulator (QA fixture data, no personal data) while a walkthrough UI test taps through it.
# usage: kits/mimi-short/app-capture/capture.sh <walkthrough.swift> <UITests file it replaces> <TestClass/testMethod> <out.mov> [ref]
#   e.g. capture.sh films/mimi-shashin/source/app-capture/DemoWalkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough \
#        films/mimi-shashin/source/renders/app/describe.mov
# PATCH=<file> applies a capture-only fixture tweak (exact-text insertion, see apply-patch.py) and reverts it afterwards.
# The walkthrough keeps the replaced file's class name, so the Xcode target needs no change. The app checkout and its build live
# in a cache (~/Library/Caches/lanclo-app-capture) and are reused: only the first run builds from scratch (about 7 minutes);
# later runs rebuild incrementally and the recording itself is the walkthrough's length (about a minute).
set -e
walk=$(cd "$(dirname "$1")" && pwd)/$(basename "$1"); target=$2; test=$3; out=$4; ref=${5:-origin/main}
repo=${LANCLO_REPO:-$HOME/Develop/native-voice-clone}; cache=$HOME/Library/Caches/lanclo-app-capture; work=$cache/nvc
mkdir -p "$(dirname "$out")"; out=$(cd "$(dirname "$out")" && pwd)/$(basename "$out")
sim=$(xcrun simctl list devices available | awk -F '[()]' '/Lanclo iPhone 18 Pro QA/ {print $2; exit}')
git -C "$repo" fetch -q origin main
if [ ! -d "$work" ]; then mkdir -p "$cache"; git -C "$repo" worktree add -q --detach "$work" "$ref"; fi
git -C "$work" checkout -q --force --detach "$ref"
cp "$walk" "$work/native-ios/LancloUITests/$target"
# Optional capture-only fixture tweak (never committed to the app): PATCH=film/app-capture/x.patch
if [ -n "$PATCH" ]; then python3 "$(dirname "$0")/apply-patch.py" "$PATCH" "$work"; fi
xcrun simctl boot "$sim" 2>/dev/null || true
xcrun simctl status_bar "$sim" override --time 9:41 --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
cd "$work/native-ios"
args="-project Lanclo.xcodeproj -scheme Lanclo -testPlan Full -destination id=$sim -derivedDataPath $cache/dd"
xcodebuild $args build-for-testing -quiet
xcrun simctl io "$sim" recordVideo --codec h264 --force "$out" & rec=$!
sleep 2
xcodebuild $args test-without-building -only-testing:"LancloUITests/$test" -quiet || true
sleep 1; kill -INT $rec; wait $rec 2>/dev/null || true
git -C "$work" checkout -q -- native-ios/LancloUITests/"$target"
[ -n "$PATCH" ] && git -C "$work" checkout -q -- native-ios/Lanclo
echo "$out (app $(git -C "$work" rev-parse --short HEAD))"
