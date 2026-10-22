# Source

```sh
F=films/mimi-month/source
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording). month-days.patch is capture-only and adds
#    --qa-mimi-day N to the --qa-mimi fixture: the report of day N (N-1 days after today) with that day's example diary lines and ranking.
PATCH=$F/app-capture/month-days.patch LANCLO_REPO=~/Develop/native-voice-clone kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/MonthWalkthrough.swift MimiReportUITests.swift MimiReportUITests/testMonthWalkthrough $F/renders/app/month.mov
#    or take it from Drive 036/Month_assets/sim-month_mimi-report_day1-30_example-data.mov
sh $F/scripts/app_track.sh            # -> hf/assets/app/d1.mp4 d7.mp4 d14.mp4 d21.mp4 d30.mp4
# 2. poses: codex-p with prompts/01-codex-poses.txt (art/*.png), then
for p in mimi-binoculars mimi-notes; do kits/mimi-short/scripts/cutout.sh $F/art/$p.png $F/art/cut/$p.webp; done
# 3. sound
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/cut/*.webp films/mimi-watching/source/art/cut/friend-shock.webp films/mimi-swipe/source/art/friend-tsukkomi.webp \
  films/mimi-loop/source/art/cut/friend-wow.webp kits/mimi-short/library/poses/{point,droop}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-month   # renders/mimi-month-en.mp4 and renders/mimi-month.mp4
```

The patch touches three files (`MimiReportQA.swift`, `MimiReportView.swift`, `VisualQAData.swift`); `kits/mimi-short/app-capture/apply-patch.py` applies multi-file patches. The day-1 clip starts after the scroll that hides the fixture's「デモデータ」label. Not in Git: the recording, `hf/assets/`, renders, the theme BGM.
