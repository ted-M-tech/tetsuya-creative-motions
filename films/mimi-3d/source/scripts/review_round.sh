#!/bin/sh
# One review round: render the hero view, put it beside the target, ask codex-p (art director) for ranked fixes.
# usage: scripts/review_round.sh <tag>      -> renders/review-<tag>.png and renders/review-<tag>.md
set -e
cd "$(dirname "$0")/.."
tag=$1
blender -b -P scripts/mimi.py -- --out renders/$tag --views hero:-26 --samples 64 --pct 60 >/dev/null 2>&1
magick ref/codex/toy-look.png renders/$tag-hero.png -resize x900 +append renders/review-$tag.png
codex-p exec --skip-git-repo-check --sandbox read-only --image renders/review-$tag.png \
  --output-last-message renders/review-$tag.md - < scripts/review_prompt.txt > renders/review-$tag.log 2>&1
cat renders/review-$tag.md
