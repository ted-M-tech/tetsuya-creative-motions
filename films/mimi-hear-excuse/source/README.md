# Rebuild mimi-hear-excuse

From the repo root (worktree of branch `feat/mimi-hear-excuse`):

```sh
S=films/mimi-hear-excuse/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 062. Can You Hear It 2 - Excuse Me/Hear2_ExcuseMe_assets/own-voice/ into $S/assets/own-voice/
uv run --no-project --with praat-parselmouth --with numpy python -I $S/scripts/check_voice.py $S/assets/own-voice/us-*.wav
sh $S/scripts/art.sh                                            # library poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json, -14 LUFS)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-hear-excuse           # -> renders/mimi-hear-excuse-en.mp4 and renders/mimi-hear-excuse.mp4
```

- `cues.json` is the cue sheet; `scripts/mix.py` reads it and `hf/index.html` repeats the same constants (keep them equal). Copied from films/mimi-hear-can/source (episode 1) in its three-option form; see films/mimi-hear-can/README.md “Series template”.
- No app beat, no side cast, no new art.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
