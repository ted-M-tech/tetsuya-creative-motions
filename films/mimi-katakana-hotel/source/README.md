# Rebuild mimi-katakana-hotel

From the repo root (worktree of branch `feat/mimi-katakana-hotel`):

```sh
S=films/mimi-katakana-hotel/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 060. Katakana Traps 3 - Hotel Guitar Shampoo/KT3_Hotel_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # library plate (lobby) + poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json), -14 LUFS
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-katakana-hotel        # -> renders/mimi-katakana-hotel-en.mp4 and renders/mimi-katakana-hotel.mp4
```

- `cues.json` is the cue sheet: beat times, where each word sits in the learner take (`LEARNER_CLIPS`), and the measured syllable nuclei inside every clip / take (`LEARNER_BEATS`, `MODEL_BEATS`, `JAPANESE_BEATS`). `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script.
- Copied from `films/mimi-katakana-mcdonalds/source` (episode 1): hook, slip, explain, model, cta, end kept; `challenge` and `reveal` added for the viewer quiz. No app shot, no Kokoro, no new art.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
