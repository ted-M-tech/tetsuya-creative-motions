# Source

```sh
F=films/mimi-disaster-sit/source
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json      # assets/own-voice/*.wav (paid; not in Git; also in Drive Disasters1_Sit_assets/own-voice/)
# the app take (shared simulator: hold the lock)
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/sit-lesson.patch sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/SitWalkthrough.swift DescribeUITests.swift DescribeUITests/testSitWalkthrough $F/renders/app/sit.mov; rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh                                         # -> hf/assets/app/app.mp4 (11.0-15.1 on the film clock)
uv run --no-project --with numpy python $F/scripts/mix.py          # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art $F/hf/assets/kit/poses && cp $F/art/*.webp $F/hf/assets/art/ && cp kits/mimi-short/library/poses/{point,perk}.webp $F/hf/assets/kit/poses/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-disaster-sit             # renders/mimi-disaster-sit-en.mp4 and renders/mimi-disaster-sit.mp4
```

| File | Role |
|---|---|
| `own-voice.json` / `own-voice.receipt.json` | Lines and receipt (no voice ID). Used: `learner-shit-2` (friend, "Please sh*t down."), `native-sit` (model). `learner-shit` was the first take (s/sh unclear), unused |
| `art/` | Codex output (`*.png`) and cut-outs (`*.webp`); `lobby.webp` is the plate |
| `app-capture/` | Walkthrough UI test and the capture-only fixture patch |
| `scripts/mix.py` | Cue sheet + sound; times shared with `hf/index.html` |
| `hf/index.html` | The edit (series template: see ../README.md) |

Not in Git: voice WAVs, the recording, `hf/assets/`, renders, the BGM (`kits/mimi-short/library/bgm/`).
