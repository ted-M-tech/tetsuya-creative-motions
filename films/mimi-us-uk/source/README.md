# Source

```sh
F=films/mimi-us-uk/source
# 1. app track: the simulator take of films/mimi-tuning (see its source/README.md; Drive 030. US vs UK English in My Own Voice/
#    US_UK_assets/simulator_voice-tuning.mov) -> $F/renders/app/tuning.mov
sh $F/scripts/app_track.sh            # -> hf/assets/app/app.mp4 on the film's clock (timings in the script)
# 2. voices (the owner's own registered voice; paid generation — or copy them from Drive US_UK_assets/own-voice/)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/mix.py
# 3. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp kits/mimi-short/library/poses/speak-{open,closed}.webp films/mimi-swipe/source/art/friend-tease.webp \
  films/mimi-action-add/source/art/friend-oops.webp films/mimi-voice/source/art/{mimi-tease,friend-amazed}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-us-uk   # renders/mimi-us-uk-en.mp4 and renders/mimi-us-uk.mp4
```

Not in Git: the recording, the voice WAVs (biometric), `hf/assets/`, renders. `own-voice.json` and `own-voice.receipt.json` (text, style, hashes; no voice ID) are in Git. Measurements of the clips (speech spans, word starts, the F3 check) are in `scripts/mix.py`.
