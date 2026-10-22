#!/bin/sh
# Copy the shared HyperFrames kit (CSS, JS, brand, fonts, library props) into an episode's HyperFrames project as assets/kit/.
# HyperFrames serves only files inside the project, so the kit is staged, not linked. assets/kit/ is ignored by Git.
# usage: kits/mimi-short/stage.sh films/<id>/source/hf
set -e
kit="$(cd "$(dirname "$0")" && pwd)"; dst="$1/assets/kit"
"$kit/fetch-fonts.sh"
[ -f "$kit/library/bgm/everyone-get-up.mp3" ] || "$kit/scripts/fetch-bgm.sh" || true
rm -rf "$dst"; mkdir -p "$dst"
cp "$kit"/hf/* "$dst/"; cp -R "$kit/brand" "$kit/fonts" "$kit/library/props" "$dst/"
echo "staged kit -> $dst"
