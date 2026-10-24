# Rebuild mimi-hack-water

From the repo root (worktree of branch `feat/mimi-hack-water`):

```sh
S=films/mimi-hack-water/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 073. Pronunciation Hacks 2 - Water (US T)/Hacks2_Water_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # episode waiter poses (cut out) + restaurant plate + library poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json; checks every cut edge, -14 LUFS)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-hack-water            # -> renders/mimi-hack-water-en.mp4 and renders/mimi-hack-water.mp4
```

- `cues.json` is the cue sheet: beat times, the cut of each take (`TAKES`: start, length, both at measured silence; `null` = not generated yet, the mix skips it), the measured chunk starts of the learner take and the measured flap inside the model takes (`WATER_FLAP`, `BETTER_FLAP`). `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script (`LW`, `WT`, `BT`, `FT`).
- Copied from `films/mimi-hack-check-it-out/source` (episode 1, series template). For the flap the `.pair` keeps its role: the t is red, a blue tap mark is drawn above it, and on the measured flap it turns blue with a small ラ under it; the tongue-tap icon (`#c-tongue`) taps on the same cue.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
