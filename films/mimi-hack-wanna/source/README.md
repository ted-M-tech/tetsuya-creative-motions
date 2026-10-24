# Rebuild mimi-hack-wanna

From the repo root (worktree of branch `feat/mimi-hack-wanna`):

```sh
S=films/mimi-hack-wanna/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 074. Pronunciation Hacks 3 - Wanna and Gonna/Hacks3_Wanna_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # library plate + poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json; checks every cut edge, -14 LUFS)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-hack-wanna     # -> renders/mimi-hack-wanna-en.mp4 and renders/mimi-hack-wanna.mp4
```

- `cues.json` is the cue sheet: beat times, the cut of each take (`TAKES`: start, length, both at measured silence) and the measured word starts inside the placed takes. `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script.
- Started from `films/mimi-hack-check-it-out/source` (series template, episode 1): same beat ids, layout, colours, sizes and loudness step; swapped the hook, the slip bubble (two lines, reduced words as 「？？？」), the card rows (slow form with the to struck → casual form with na in blue), the fix (Mimi once more, then the Friend's line), the plate (`cafe`) and the takes. No app shot, no Kokoro, no new poses.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
