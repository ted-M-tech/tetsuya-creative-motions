# Rebuild mimi-hear-can

From the repo root (worktree of branch `feat/mimi-hear-can`):

```sh
S=films/mimi-hear-can/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 061. Can You Hear It 1 - Can or Cant/Hear1_Can_assets/own-voice/ into $S/assets/own-voice/
uv run --no-project --with praat-parselmouth --with numpy python -I $S/scripts/check_voice.py $S/assets/own-voice/us-can.wav $S/assets/own-voice/us-cant.wav
sh $S/scripts/art.sh                                            # library poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-hear-can              # -> renders/mimi-hear-can-en.mp4 and renders/mimi-hear-can.mp4
```

- `cues.json` is the cue sheet; `scripts/mix.py` reads it and `hf/index.html` repeats the same constants (keep them equal). Started from films/mimi-disaster-hat/source, rebuilt as the “Can You Hear It?” quiz layout with generic beat ids (hook, play, reveal, rule, ask, end); see ../README.md “Series template”.
- No app beat, no side cast, no new art.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
