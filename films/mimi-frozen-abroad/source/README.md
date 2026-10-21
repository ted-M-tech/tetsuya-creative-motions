# Source

```sh
F=films/mimi-frozen-abroad/source
# 0. the app take (needs ~/Develop/native-voice-clone and Xcode; or take it from Lanclo Drive
#    002.SNS/032. Frozen Abroad - Roleplay Series/FrozenAbroad_assets/sim-roleplay-airport_fixture.mov -> $F/renders/app/airport.mov)
#    The simulator is shared: hold /tmp/lanclo-capture.lock while capturing.
PATCH=$F/app-capture/airport-lines.patch LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/RoleplayAirportWalkthrough.swift SituationUITests.swift SituationUITests/testAirportWalkthrough $F/renders/app/airport.mov
sh $F/scripts/app_track.sh                 # hf/assets/app/app.mp4 (film 8.5-14.3) and catalog.mp4 (film 18.7-)
# 1. art (Codex drawings in art/*.png, art/friend/*.png) -> cut-outs, plates and counter fronts
for p in airport-ask hotel-ask driver-ask; do kits/mimi-short/scripts/cutout.sh $F/art/friend/$p.png $F/art/$p.webp; done
kits/mimi-short/scripts/cutout.sh $F/art/hand-up.png $F/art/hand-up.webp
for b in airport hotel bus; do magick $F/art/$b.png -resize 1080x1920! -quality 90 $F/art/$b.webp; done
magick $F/art/airport.png -crop 1080x800+0+1110 +repage -define webp:lossless=true $F/art/airport-counter.webp
magick $F/art/hotel.png -crop 1080x860+0+1060 +repage -define webp:lossless=true $F/art/hotel-counter.webp
magick $F/art/bus.png -crop 1080x770+0+1150 +repage -define webp:lossless=true $F/art/bus-counter.webp
# 2. voices and sound
sh $F/scripts/voices.sh                                   # staff (Kokoro, committed)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # Mimi (owner's voice, not in Git; or copy from Drive FrozenAbroad_assets/own-voice/ to $F/assets/own-voice/)
uv run --no-project --with numpy python $F/scripts/mix.py
# 3. edit
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp films/mimi-roleplay/source/art/{cafe,counter,grin}.webp $F/art/*.webp kits/mimi-short/library/poses/{stunned,confident}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-frozen-abroad   # renders/mimi-frozen-abroad-en.mp4 and renders/mimi-frozen-abroad.mp4
```

| File | Role |
|---|---|
| `app-capture/RoleplayAirportWalkthrough.swift` | UI test (replaces `SituationUITests.swift` in the capture checkout): 練習 → 会話練習 catalogue (scroll) → 空港 → 飛行機の搭乗手続きをする → meaning → hint → record (fixture take) → completed → back to the catalogue (scroll) |
| `app-capture/airport-lines.patch` | Capture-only: the QA fixture answers the airport scene with its authored lines instead of the café's (never committed to the app) |
| `scripts/app_track.sh` | Measured times on the 60 fps take and the cuts on the film's clock |
| `scripts/voices.sh`, `assets/voice/` | Kokoro staff lines |
| `own-voice.json`, `own-voice.receipt.json` | Mimi's three replies in the owner's voice (`us`); the WAVs stay out of Git |
| `scripts/mix.py` | Cue sheet and sound; the times match `hf/index.html` |
| `hf/index.html` | The edit |
| `art/` | Codex drawings (PNG) and cut-outs/plates (WebP) |

Not in Git: the simulator take, the owner's voice clips, `hf/assets/`, renders and the final MP4s.
