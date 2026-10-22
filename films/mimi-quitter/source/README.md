# Source

```sh
F=films/mimi-quitter/source
# 1. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording)
PATCH=$F/app-capture/month-streak.patch LANCLO_REPO=~/Develop/native-voice-clone kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/QuitterWalkthrough.swift MimiReportUITests.swift MimiReportUITests/testQuitterWalkthrough $F/renders/app/quitter.mov
#    or take it from Drive 029/Quitter_assets/sim-quitter_lesson_report_home-streak.mov
sh $F/scripts/app_track.sh            # -> hf/assets/app/{lesson,report,home}.mp4 and the widget artwork from the app
# 2. pose: codex-p with prompts/01-codex-poses.txt (art/friend-bozu.png), then
kits/mimi-short/scripts/cutout.sh $F/art/friend-bozu.png $F/art/cut/friend-bozu.webp
# 3. sound
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/cut/friend-bozu.webp films/mimi-loop/source/art/cut/{friend-wow,friend-nod,friend-sigh,friend-bed,friend-type}.webp \
  films/mimi-voice/source/art/friend-amazed.webp kits/mimi-short/library/poses/jump.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-quitter   # renders/mimi-quitter-en.mp4 and renders/mimi-quitter.mp4
```

The Lock Screen, Home Screen widgets and the 20:00 reminder are HTML in `hf/index.html`, drawn after `LancloWidgets.swift` and `PracticeReminder.swift`. The mask over the lesson's fixture title is `#m-les` (screen percentages). Not in Git: the recording, `hf/assets/`, renders, the theme BGM.
