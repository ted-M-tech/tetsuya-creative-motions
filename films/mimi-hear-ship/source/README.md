# Rebuild mimi-hear-ship

From the repo root (worktree of branch `feat/mimi-hear-ship`):

```sh
S=films/mimi-hear-ship/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 078. Can You Hear It 3 - Ship or Sheep/Hear3_Ship_assets/own-voice/ into $S/assets/own-voice/
uv run --no-project --with praat-parselmouth --with numpy python -I $S/scripts/check_voice.py $S/assets/own-voice/us-ship.wav $S/assets/own-voice/us-sheep.wav
sh $S/scripts/art.sh                                            # library poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json, -14 LUFS post-gain)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-hear-ship             # -> renders/mimi-hear-ship-en.mp4 and renders/mimi-hear-ship.mp4
```

- Copied from films/mimi-hear-can/source (episode 1; see its README “Series template”); beat ids unchanged (hook, play, reveal, rule, ask, end). `cues.json` is the cue sheet; `scripts/mix.py` reads it and `hf/index.html` repeats the same constants (keep them equal).
- `scripts/check_voice.py` here finds the vowel after the sh by energy and spectrum (the final vowel is often creaky, so not by the pitch track) and prints its duration and median F1 / F2.
- No app beat, no side cast, no new art (the sheep / ship icons are inline SVG).
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
