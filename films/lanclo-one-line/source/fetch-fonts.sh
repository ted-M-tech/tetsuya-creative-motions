#!/bin/sh
# Zen Maru Gothic (SIL OFL 1.1) from the Google Fonts repository.
set -e
cd "$(dirname "$0")/assets/fonts"
for f in ZenMaruGothic-Regular.ttf ZenMaruGothic-Medium.ttf ZenMaruGothic-Bold.ttf OFL.txt; do
  curl -fsSL -o "$f" "https://raw.githubusercontent.com/google/fonts/main/ofl/zenmarugothic/$f"
done
