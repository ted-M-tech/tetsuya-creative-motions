# Rebuild mimi-hack-check-it-out

From the repo root (worktree of branch `feat/mimi-hack-check-it-out`):

```sh
S=films/mimi-hack-check-it-out/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 072. Pronunciation Hacks 1 - Check It Out/Hacks1_CheckItOut_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # library plate + poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json; checks every cut edge, -14 LUFS)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-hack-check-it-out     # -> renders/mimi-hack-check-it-out-en.mp4 and renders/mimi-hack-check-it-out.mp4
```

- `cues.json` is the cue sheet: beat times, the cut of each take (`TAKES`: start, length, both at measured silence) and the measured word starts inside the placed takes. `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script.
- Started from `films/mimi-katakana-mcdonalds/source` (layout, say bubble, card, CTA, end card, subtitles, loudness step), rebuilt for the Pronunciation Hacks beats (hook, slip, tip, model, fix, cta, end). No app shot, no Kokoro, no new poses.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
