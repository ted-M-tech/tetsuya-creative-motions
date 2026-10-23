#!/bin/sh
# Copy the Lanclo SNS theme (OpenTracks「Everyone Get Up」, Anonyment) into library/bgm/ (ignored by Git).
# The licence forbids passing the file on, so it lives only in Lanclo's private repo (design/sns-bgm);
# this reads its committed origin/main, never the working tree. Without that repo, bring your own BGM.
# usage: kits/mimi-short/scripts/fetch-bgm.sh   (LANCLO_REPO=<native-voice-clone checkout> to override)
set -e
repo=${LANCLO_REPO:-$HOME/Develop/native-voice-clone}
kit="$(cd "$(dirname "$0")/.." && pwd)"; out="$kit/library/bgm/everyone-get-up.mp3"
mkdir -p "$(dirname "$out")"
if git -C "$repo" fetch -q origin main 2>/dev/null &&
   git -C "$repo" show origin/main:design/sns-bgm/everyone-get-up.mp3 > "$out.tmp" 2>/dev/null; then
  mv "$out.tmp" "$out"; echo "bgm <- $repo origin/main:design/sns-bgm/everyone-get-up.mp3"
else
  rm -f "$out.tmp"
  echo "fetch-bgm: the Lanclo theme is in a private repo you cannot read ($repo)." >&2
  echo "Put your own track at $out, or build with MIMI_BGM=builtin for the code-made bed." >&2
  exit 1
fi
