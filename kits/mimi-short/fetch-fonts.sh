#!/bin/sh
# Zen Maru Gothic (SIL OFL 1.1) from the Google Fonts repository -> kits/mimi-short/fonts (not in Git).
set -e
mkdir -p "$(dirname "$0")/fonts" && cd "$(dirname "$0")/fonts"
for f in ZenMaruGothic-Regular.ttf ZenMaruGothic-Bold.ttf OFL.txt; do
  [ -f "$f" ] || curl -fsSL -o "$f" "https://raw.githubusercontent.com/google/fonts/main/ofl/zenmarugothic/$f"
done
