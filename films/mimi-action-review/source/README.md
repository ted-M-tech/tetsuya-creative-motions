# Source

```sh
F=films/mimi-action-review/source
sh $F/scripts/app_track.sh                # renders/app/review.mov (simulator, ReviewWalkthrough + bless-note.patch) and renders/app/settings.mov -> hf/assets/app/app.mp4 and settings.mp4 on the film's clock
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/toilet.webp $F/art/sheepish.webp kits/mimi-short/library/poses/{stunned,jump,reach}.webp films/mimi-action-add/source/art/paw.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-action-review  # renders/mimi-action-review-en.mp4 (English subtitles) and renders/mimi-action-review.mp4 (Japanese only)
```

Not in Git: the recordings, `hf/assets/`, renders. `assets/voice/` keeps the unused Kokoro Japanese take for reference.
