# Rebuild mimi-katakana-mansion

From the repo root (worktree of branch `feat/mimi-katakana-mansion`):

```sh
S=films/mimi-katakana-mansion/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 059. Katakana Traps 2 - Mansion/KT2_Mansion_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # cut-outs (props), library plate + poses -> hf/assets/art/
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json), -14 LUFS
kits/mimi-short/stage.sh $S/hf
(cd $S/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $S/hf mimi-katakana-mansion      # -> renders/mimi-katakana-mansion-en.mp4 and renders/mimi-katakana-mansion.mp4
```

- `cues.json` is the cue sheet: beat times plus `TRIM` (leading silence cut from each take). `scripts/mix.py` reads it; `hf/index.html` repeats the same numbers at the top of its script.
- Copied from `films/mimi-katakana-mcdonalds/source` (episode 1) with the beat ids kept; the `model` beat holds the quick-fire trap card in this meaning-trap episode.
- `hyperframes check` reports one layout item: the red strike line over コンセント / クレーム "occludes" the text. That is the intended cross-out.
- Platform safe zones (TikTok / Reels / Shorts UI): nothing meaningful below y 1500, no text or small figures in the right rail (x > 900, y 820–1520), text from y 200; English subtitles sit at bottom 420 px within x 60–880. Overlay check: ../process/01-safe-zones.jpg.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
