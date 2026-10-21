# Source

```sh
F=films/mimi-action-lesson/source
sh $F/scripts/app_track.sh                # renders/app/daily-60.mp4 (the 「積読」 simulator take, Drive 009 assets) and renders/app/settings.mov -> hf/assets/app/app.mp4 and settings.mp4 on the film's clock
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/bed.webp $F/art/wakeup.webp kits/mimi-short/library/{poses/jump,poses/reach}.webp kits/mimi-short/library/official/success.png films/mimi-action-add/source/art/paw.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-action-lesson  # renders/mimi-action-lesson-en.mp4 (English subtitles) and renders/mimi-action-lesson.mp4 (Japanese only)
```

Not in Git: the recordings, `hf/assets/`, renders. `assets/voice/` keeps the unused Kokoro Japanese take for reference.
