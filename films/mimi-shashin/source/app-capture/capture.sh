#!/bin/sh
# Record the real Lanclo app (simulator, fixture data) walking through Describe (写真描写).
# usage: films/mimi-shashin/source/app-capture/capture.sh [native-voice-clone checkout] [ref]
# Builds a throwaway checkout of the app at <ref>, swaps DescribeUITests.swift for DemoWalkthrough.swift,
# runs it on the "Lanclo iPhone 18 Pro QA" simulator while recording -> ../renders/app/describe.mov
set -e
here="$(cd "$(dirname "$0")" && pwd)"; repo=${1:-$HOME/Develop/native-voice-clone}; ref=${2:-origin/main}
work="$(mktemp -d)/nvc"; out="$here/../renders/app"; mkdir -p "$out"
sim=$(xcrun simctl list devices available | awk -F '[()]' '/Lanclo iPhone 18 Pro QA/ {print $2; exit}')
git -C "$repo" fetch -q origin main
git -C "$repo" worktree add -q --detach "$work" "$ref"
trap 'git -C "$repo" worktree remove --force "$work"' EXIT
cp "$here/DemoWalkthrough.swift" "$work/native-ios/LancloUITests/DescribeUITests.swift"
xcrun simctl boot "$sim" 2>/dev/null || true
xcrun simctl status_bar "$sim" override --time 9:41 --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
cd "$work/native-ios"
xcodebuild -project Lanclo.xcodeproj -scheme Lanclo -testPlan Full -destination "id=$sim" -derivedDataPath "$work/dd" build-for-testing -quiet
xcrun simctl io "$sim" recordVideo --codec h264 --force "$out/describe.mov" & rec=$!
sleep 2
xcodebuild -project Lanclo.xcodeproj -scheme Lanclo -testPlan Full -destination "id=$sim" -derivedDataPath "$work/dd" test-without-building \
  -only-testing:LancloUITests/DescribeUITests/testWalkthrough -quiet || true
sleep 1; kill -INT $rec; wait $rec 2>/dev/null || true
echo "$out/describe.mov ($(git -C "$repo" rev-parse --short "$ref"))"
