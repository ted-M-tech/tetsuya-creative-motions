# Rebuild mimi-katakana-vitamin

From the repo root (worktree of branch `feat/mimi-katakana-vitamin`):

```sh
S=films/mimi-katakana-vitamin/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 076. Katakana Traps 4 - Vitamin/KT4_Vitamin_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # cut-outs (Mimi pharmacist poses), pharmacy plate, V mouth panel, library poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json), -14 LUFS
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-katakana-vitamin      # -> renders/mimi-katakana-vitamin-en.mp4 and renders/mimi-katakana-vitamin.mp4
```

- `cues.json` is the cue sheet: beat times, the placed segment of each take (`LEARNER_CUT`, `MODEL_CUT` = [start, length], cut at silence with ≥ 40 ms pre-roll) and the measured syllable nuclei (`LEARNER_BEATS`, `MODEL_BEATS`, seconds from the take start). `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script.
- Copied from `films/mimi-katakana-mcdonalds/source` (episode 1): beat ids and element ids kept; the stressed dot moved to the first syllable; the card adds the V mouth panel (`#c-v`) and the US/UK note (`#c-note`). No app shot, no Kokoro.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
