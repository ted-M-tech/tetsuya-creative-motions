# Source

```sh
F=films/mimi-action-add/source
# 0. inputs not in Git (Lanclo Drive 002.SNS/011. Action Button 1 - Add a Phrase/AB1_assets/):
#    iphone-add-phrase_bless-your-heart.mov -> $F/renders/app/iphone.mov ; iphone-settings_action-button.mov -> $F/renders/app/settings.mov
sh $F/scripts/app_track.sh                         # hf/assets/app/app.mp4 and settings.mp4 on the film's clock
for p in blush angry paw; do kits/mimi-short/scripts/cutout.sh $F/art/$p.png $F/art/$p.webp; done
for p in aww oops; do kits/mimi-short/scripts/cutout.sh $F/art/friend/$p.png $F/art/friend-$p.webp; done
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py && sh $F/scripts/render.sh
sh $F/scripts/voices.sh                            # only to rebuild the friend's line (committed)
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/paw.webp $F/art/blush.webp $F/art/friend-aww.webp $F/art/friend-oops.webp \
  kits/mimi-short/library/poses/jump.webp kits/mimi-short/library/poses/reach.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-action-add   # -en.mp4 with English subtitles, .mp4 Japanese only
```

| File | Role |
|---|---|
| `scripts/app_track.sh` | Cuts the iPhone recordings onto the film's clock (typing at 4x, waits skipped, holds) |
| `scripts/shots.py`, `render.sh` | Rive shots: blush, stunned, angry, success |
| `scripts/mix.py` | Cue sheet and sound (friend line, SFX, theme bed, CTA pochi) |
| `hf/index.html` | The edit: two-shot, button macro and tiny Mimi, copy cards, phone, highlights, taps, close with the settings walk, end card |
| `art/` | Codex drawings (PNG) and cut-outs (WebP); `art/friend/` the friend's concepts and final poses |

Positions of highlights and taps are percentages of the recording (1206×2622) after `object-fit: cover`; re-measure if the recording changes.

Not in Git: the iPhone recordings, `hf/assets/` (app track, shots, art copies, mix, staged kit), renders and the final MP4.
