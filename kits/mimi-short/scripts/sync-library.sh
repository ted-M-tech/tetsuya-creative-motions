#!/bin/sh
# Copy the Mimi 2D library (master: native-voice-clone design/mimi-2d, official art in voice-web/public/mascot/mimi)
# into kits/mimi-short/library so episodes rebuild from this repo alone. Reads a committed ref, never the working tree.
# usage: kits/mimi-short/scripts/sync-library.sh [native-voice-clone checkout] [ref]
set -e
repo=${1:-$HOME/Develop/native-voice-clone}; ref=${2:-origin/main}
kit="$(cd "$(dirname "$0")/.." && pwd)"
git -C "$repo" fetch -q origin main
tmp="$(mktemp -d)"
git -C "$repo" archive "$ref" design/mimi-2d voice-web/public/mascot/mimi | tar -x -C "$tmp"
rm -rf "$kit/library"; mkdir -p "$kit/library/official"
cp -R "$tmp/design/mimi-2d/poses" "$tmp/design/mimi-2d/backgrounds" "$tmp/design/mimi-2d/catalog.json" "$kit/library/"
cp "$tmp/design/mimi-2d/scripts/lipsync-model.json" "$kit/library/"
cp "$tmp"/voice-web/public/mascot/mimi/*.png "$kit/library/official/"
echo "$(git -C "$repo" rev-parse "$ref") $ref" > "$kit/library/SOURCE"
echo "library <- $(cat "$kit/library/SOURCE")"
