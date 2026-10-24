# Rebuild mimi-hack-milk

From the repo root (worktree of branch `feat/mimi-hack-milk`):

```sh
S=films/mimi-hack-milk/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 075. Pronunciation Hacks 4 - Milk/Hacks4_Milk_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # cut out the episode poses, stage plate, counter and poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json; checks every cut edge, -14 LUFS)
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-hack-milk             # -> renders/mimi-hack-milk-en.mp4 and renders/mimi-hack-milk.mp4
```

- `cues.json` is the cue sheet: beat times, the cut of each take (`TAKES`: start, length, both at measured silence with ≥ 40 ms pre-roll) and the measured syllable / word starts inside the placed takes. `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script.
- Copied from `films/mimi-hack-check-it-out/source` (series template): same beat ids, CSS colours, fonts and sizes; the link arcs are replaced by beat dots and a strike on the added vowels.
- `art/*.png` are the codex-p originals of the two Mimi barista poses; `art.sh` cuts them out (`art/*.webp`).
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
