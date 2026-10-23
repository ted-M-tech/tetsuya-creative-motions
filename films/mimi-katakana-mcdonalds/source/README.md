# Rebuild mimi-katakana-mcdonalds

From the repo root (worktree of branch `feat/mimi-katakana-mcdonalds`):

```sh
S=films/mimi-katakana-mcdonalds/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 058. Katakana Traps 1 - McDonalds/KT1_McDonalds_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # cut-outs (Mimi clerk poses), library plate + poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-katakana-mcdonalds    # -> renders/mimi-katakana-mcdonalds-en.mp4 and renders/mimi-katakana-mcdonalds.mp4
```

- `cues.json` is the cue sheet: beat times plus the measured beats inside the two takes (`LEARNER_BEATS`, `MODEL_BEATS`). `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script.
- Started from `films/mimi-disaster-hat/source` (layout, say bubble, card, end card), rebuilt for the Katakana Traps beats (hook, slip, explain, model, cta, end). No app shot, no Kokoro.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
