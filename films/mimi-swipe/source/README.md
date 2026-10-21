# Source

```sh
F=films/mimi-swipe/source
# 0. the app take (needs ~/Develop/native-voice-clone and Xcode; or take it from Lanclo Drive
#    002.SNS/014. Swipe Review/Swipe_assets/sim-swipe-review_fixture.mov -> $F/renders/app/swipe.mov)
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/bless-note.patch sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/SwipeWalkthrough.swift NotesPerformanceUITests.swift NotesPerformanceUITests/testSwipeWalkthrough $F/renders/app/swipe.mov
sh $F/scripts/app_track.sh                         # hf/assets/app/app.mp4 on the film's clock (starts at 5.0 s)
for p in swipe fluster date; do kits/mimi-short/scripts/cutout.sh $F/art/$p.png $F/art/$p.webp; done
for p in tease tsukkomi; do kits/mimi-short/scripts/cutout.sh $F/art/friend/$p.png $F/art/friend-$p.webp; done
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py && sh $F/scripts/render.sh
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/swipe.webp $F/art/fluster.webp $F/art/date.webp $F/art/friend-tease.webp \
  $F/art/friend-tsukkomi.webp $F/art/friend-oops.webp $F/hf/assets/art/
cd $F/hf && npx --yes hyperframes@0.8.181 check && npx --yes hyperframes@0.8.181 render --output ../renders/mimi-swipe.mp4 --fps 60
```

| File | Role |
|---|---|
| `app-capture/SwipeWalkthrough.swift` | UI test (replaces `NotesPerformanceUITests.swift` in the capture checkout): open review with fixture notes, flip the first card, then drag right, left, right, up slowly and hold before letting go |
| `app-capture/bless-note.patch` | Capture-only fixture tweak (from `films/mimi-action-review`): adds the "Bless your heart" note |
| `scripts/app_track.sh` | Four swipes from the 60 fps take at 1.25x, cut on the same card so the joins don't show |
| `scripts/shots.py`, `render.sh` | The Rive shot of Mimi swiping beside the phone |
| `scripts/mix.py` | Cue sheet and sound (soft SFX, theme bed, end chord, CTA pochi) |
| `hf/index.html` | The edit: hook with flying cards, two-shots with speech bubbles, copy card, phone + direction chips + captions, the retort, end card |
| `art/` | Codex drawings (PNG) and cut-outs (WebP); `art/friend/` the friend's drawings and her design reference (`chosen-2.png`) |

If the take is re-recorded, re-measure the swipe times on a contact sheet of `renders/app/swipe-60.mp4` and update `scripts/app_track.sh`, the chip times in `hf/index.html` and `DRAGS`/`FLY` in `scripts/mix.py`.

Not in Git: the simulator take, `hf/assets/` (app track, shot, art copies, mix, staged kit), renders and the final MP4.
