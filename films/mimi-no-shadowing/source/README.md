# Source

```sh
F=films/mimi-no-shadowing/source
# 0. the app take: the daily-lesson recording made for films/mimi-daily (2026-10-20), from Lanclo Drive
#    002.SNS/035. I Stopped Shadowing Native Speakers/NoShadowing_assets/sim-daily-model_fixture.mov -> $F/renders/app/daily.mov
#    (or record a fresh one: hold /tmp/lanclo-capture.lock, then
#     LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh $F/app-capture/ModelWalkthrough.swift \
#       DescribeUITests.swift DescribeUITests/testModelWalkthrough $F/renders/app/daily.mov  — and re-measure scripts/app_track.sh)
sh $F/scripts/app_track.sh                 # hf/assets/app/app.mp4 (film 6.6-10.6)
# 1. art (Codex drawings art/*.png) -> cut-outs
for p in bruno-talk bruno-shrug struggle toss-v2 cassette; do kits/mimi-short/scripts/cutout.sh $F/art/$p.png $F/art/$p.webp; done
magick $F/art/bruno-talk.webp -crop 760x660+90+0 +repage -resize 300x $F/art/bruno-head.webp   # the face on the cassette
# 2. voices and sound
sh $F/scripts/voices.sh                                         # Bruno, the stranger (Kokoro am_michael, committed)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # Mimi + model (owner's voice, not in Git; or copy Drive NoShadowing_assets/own-voice/ to $F/assets/own-voice/)
uv run --no-project --with numpy python $F/scripts/mix.py
# 3. edit
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp kits/mimi-short/library/poses/{speak-open,speak-closed,confident,jump}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-no-shadowing   # renders/mimi-no-shadowing-en.mp4 and renders/mimi-no-shadowing.mp4
```

| File | Role |
|---|---|
| `app-capture/ModelWalkthrough.swift` | UI test for a fresh take (home → daily lesson → お手本 → record); not used for this cut (see PROCESS.md) |
| `scripts/app_track.sh` | Measured times on the take and the cut on the film's clock |
| `scripts/voices.sh`, `assets/voice/` | The stranger's line (Kokoro) |
| `own-voice.json`, `own-voice.receipt.json` | before (`learner`), model and along (`us`) in the owner's voice; WAVs stay out of Git |
| `scripts/mix.py` | Cue sheet and sound; the times match `hf/index.html` |
| `hf/index.html` | The edit |
| `art/` | Codex drawings (PNG) and cut-outs (WebP) |

Not in Git: the simulator take, the owner's voice clips, `hf/assets/`, renders and the final MP4s.
