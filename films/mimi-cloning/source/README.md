# Source

```sh
F=films/mimi-cloning/source
# 0. the app take (QA fixture): copy Drive 067/Cloning_assets/sim-daily-model_fixture.mov -> $F/renders/app/daily.mov, or record a fresh one:
#    until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
#    env -u PATCH LANCLO_REPO=~/Develop/native-voice-clone sh kits/mimi-short/app-capture/capture.sh $F/app-capture/ModelWalkthrough.swift \
#      DescribeUITests.swift DescribeUITests/testModelWalkthrough $F/renders/app/daily.mov; rmdir /tmp/lanclo-capture.lock
#    (and re-measure the trim in scripts/app_track.sh)
sh $F/scripts/app_track.sh                                      # hf/assets/app/app.mp4 (film 31.3-35.6)
# 1. voices: the owner's voice (paid; or copy Drive 067/Cloning_assets/own-voice/*.wav to $F/assets/own-voice/ — skip take1-low.wav)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
uv run --no-project --with numpy python $F/scripts/spans.py      # speech spans used in mix.py and index.html
uv run --no-project --with numpy python $F/scripts/mix.py        # hf/assets/mix.wav at -14 LUFS
# 2. edit
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && (cd kits/mimi-short/library && cp poses/{friend-oops,friend-shock,friend-shrink,friend-swamped,friend-puzzled,friend-amazed,friend-nod,friend-tsukkomi,presenter,perk,confident,grin,point,highfive}.webp props/bulb.webp ../../../$F/hf/assets/art/)
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-cloning               # renders/mimi-cloning-en.mp4 and renders/mimi-cloning.mp4
sh $F/scripts/sheets.sh $F/renders/mimi-cloning-en.mp4 /tmp/cloning   # contact sheet + platform-zone sheet every 1.5 s
```

| File | Role |
|---|---|
| `app-capture/ModelWalkthrough.swift` | UI test for the take (home → daily lesson → お手本 → record) |
| `scripts/app_track.sh` | Measured times on the take and the cut on the film's clock |
| `own-voice.json`, `own-voice.receipt.json` | Every English line in the owner's voice (new: `low`, `high`, `fast`; reused from #35 and #30, marked `reusedFrom`); WAVs stay out of Git |
| `scripts/spans.py` | Speech span and head/tail level of each clip |
| `scripts/mix.py` | Cue sheet and sound; the times match `hf/index.html` |
| `scripts/sheets.sh` | Review sheets (frames, platform safe zones) |
| `hf/index.html` | The edit |

Not in Git: the simulator take, the owner's voice clips, `hf/assets/`, renders and the MP4s (Drive `002.SNS/067. Cloning - Shadowing but in Your Own Voice/`).
