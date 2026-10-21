# Source

```sh
F=films/mimi-roleplay/source
# 0. the app take (needs ~/Develop/native-voice-clone and Xcode; or take it from Lanclo Drive
#    002.SNS/017. Roleplay - Frozen at the Cafe/Roleplay_assets/sim-roleplay-cafe_fixture.mov -> $F/renders/app/roleplay.mov)
#    The simulator is shared: hold /tmp/lanclo-capture.lock while capturing.
LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/RoleplayWalkthrough.swift SituationUITests.swift SituationUITests/testRoleplayWalkthrough $F/renders/app/roleplay.mov
sh $F/scripts/app_track.sh                 # hf/assets/app/app.mp4 (film 4.3-10.6) and catalog.mp4 (film 15.55-)
# 1. art (Codex drawings in art/*.png, art/friend/*.png) -> cut-outs and plates
for p in grin; do kits/mimi-short/scripts/cutout.sh $F/art/$p.png $F/art/$p.webp; done
for p in barista-ask barista-smile; do kits/mimi-short/scripts/cutout.sh $F/art/friend/$p.png $F/art/$p.webp; done
magick $F/art/cafe.png -resize 1080x1920! -quality 90 $F/art/cafe.webp
magick $F/art/cafe.png -crop 1080x362+0+1140 +repage -define webp:lossless=true $F/art/counter.webp   # counter front, laid over the barista
# 2. voices (committed) and sound
sh $F/scripts/voices.sh
uv run --no-project --with numpy python $F/scripts/mix.py
# 3. edit
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/{cafe,counter,barista-ask,barista-smile,grin}.webp kits/mimi-short/library/poses/{stunned,confident,reach}.webp $F/hf/assets/art/
magick kits/mimi-short/library/official/master.png -crop 960x1213+90+23 +repage -bordercolor none -border 24 -define webp:lossless=true $F/hf/assets/art/master.webp  # faint alpha defeats -trim
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-roleplay   # renders/mimi-roleplay-en.mp4 (English subtitles) and renders/mimi-roleplay.mp4 (Japanese only)
```

| File | Role |
|---|---|
| `app-capture/RoleplayWalkthrough.swift` | UI test (replaces `SituationUITests.swift` in the capture checkout): Practice tab → 会話練習 catalogue (scroll) → カフェ → 飲み物を注文する → meaning on → hint → record (fixture take) → completed → back to the catalogue (scroll) |
| `scripts/app_track.sh` | Measured times on the 60 fps take and the cuts on the film's clock |
| `scripts/voices.sh`, `assets/voice/` | Kokoro English lines (barista `bf_emma`, Mimi `af_heart`) |
| `scripts/mix.py` | Cue sheet and sound; the times match `hf/index.html` |
| `hf/index.html` | The edit: café two-shots with bubbles, ice + カチッ, copy cards, phone + taps + mask + captions, shatter, close, end card; English subtitles (`.sub`, hidden by `<body class="no-subs">`) |
| `art/` | Codex drawings (PNG) and cut-outs/plates (WebP); `art/friend/` the barista drawings |

If the take is re-recorded, re-measure on a contact sheet of `renders/app/roleplay-60.mp4` and update `scripts/app_track.sh`, the tap times in `hf/index.html` and `TAPS` in `scripts/mix.py`.

Not in Git: the simulator take, `hf/assets/` (app tracks, art copies, mix, staged kit), renders and the final MP4s.
