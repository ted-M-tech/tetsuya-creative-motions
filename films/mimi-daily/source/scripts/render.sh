#!/bin/sh
# Render every Rive shot (or the ones named) -> renders/rive/<shot>.mp4, copied into hf/assets/shots/.
# usage: films/mimi-daily/source/scripts/render.sh [shot ...]
set -e
src="$(cd "$(dirname "$0")/.." && pwd)"; kit="$src/../../../kits/mimi-short/scripts"
mkdir -p "$src/hf/assets/shots"
for d in ${@:-$(ls "$src/rive")}; do
  n=$(grep -o 'duration="[0-9]*"' "$src/rive/$d/scene.rml" | head -1 | tr -dc 0-9)
  "$kit/render_rive.sh" "$src/rive/$d" $((n + 1)) "$src/renders/rive/$d"
  cp "$src/renders/rive/$d.mp4" "$src/hf/assets/shots/$d.mp4"
done
