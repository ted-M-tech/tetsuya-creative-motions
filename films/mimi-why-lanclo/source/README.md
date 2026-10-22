# Source

```sh
F=films/mimi-why-lanclo/source
# 1. app clips: copy the earlier films' takes from Drive into $F/renders/app/ (names in scripts/app_track.sh), then
sh $F/scripts/app_track.sh            # -> hf/assets/app/{photo,debate,roleplay,journal,daily}.mp4 (1.6 s each)
# 2. poses (already cut in art/*.webp): codex-p with prompts/01-codex-poses.txt and the cast references
#    (kits/mimi-short/cast/mimi/master.webp, friend/sheet.webp, friend/aww.webp, library/poses/friend-french.webp, side/duck/smile.webp, side/cat/happy.webp), then
kits/mimi-short/scripts/cutout.sh $F/art/<pose>.png $F/art/<pose>.webp
# 3. voices (committed) and sound
sh $F/scripts/voices.sh
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp kits/mimi-short/library/poses/{bruno-talk,bruno-boss-nod,bruno-tourist-laugh,confident,notes}.webp \
  kits/mimi-short/library/poses/stunned.webp kits/mimi-short/library/backgrounds/{meeting,cafe,lobby,desk}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-why-lanclo   # renders/mimi-why-lanclo-en.mp4 and renders/mimi-why-lanclo.mp4
```

| Path | Role |
|---|---|
| `art/` | The seven new poses (PNG from Codex, cut-out WebP) |
| `assets/voice/` | Kokoro: the discussion chatter (b1, p1, c1, b2, p2, c2), the self-introduction questions (q1 Bruno, q2 Pippa, q3 Coco, q4 Bruno's deeper question) and the confident lines (b3 Bruno, c3 Coco) |
| `scripts/voices.sh` | Kokoro lines and voices |
| `scripts/app_track.sh` | The five 1.6 s app clips, with the source takes and times |
| `scripts/mix.py` | Cue sheet (same times as `hf/index.html`), bed lowered in the middle, static gain to -14 LUFS + limiter |
| `hf/index.html` | The edit; the fixture masks are `#mk-demo` and `#mk-qa` (screen percentages) |

Not in Git: the source takes and the cut clips (Drive), `hf/assets/`, renders, the theme BGM.
