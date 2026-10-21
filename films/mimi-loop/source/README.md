# Source

```sh
F=films/mimi-loop/source
# 1. app: record the walkthrough (shared simulator: take the lock), copy the two reused takes, cut one track on the film's clock
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone kits/mimi-short/app-capture/capture.sh $F/app-capture/LoopWalkthrough.swift \
  MimiReportUITests.swift MimiReportUITests/testLoopWalkthrough $F/renders/app/loop.mov; rmdir /tmp/lanclo-capture.lock
cp "<Drive>/002.SNS/009. Unread Books - Daily Lesson/Mimi_06_Unread_Books_assets/daily-60.mp4" $F/renders/app/
ffmpeg -i "<Drive>/002.SNS/014. Swipe Review/Swipe_assets/sim-swipe-review_fixture.mov" -an -vf fps=60 -c:v libx264 -crf 14 $F/renders/app/swipe-60.mp4
sh $F/scripts/app_track.sh                       # -> hf/assets/app/app.mp4 (13.6 s from 12.9 s) and bed.mp4 (the night scene); times in the script header
# 2. poses: cut out the Codex drawings (art/*.png -> art/cut/*.webp); run-left is run.png mirrored with the near cup's L painted out
kits/mimi-short/scripts/cutout.sh $F/art/run.png $F/art/cut/run.webp   # likewise run-left, presenter, friend/{sigh,wow,type,nod,bed}
# 3. sound and edit
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/cut/*.webp kits/mimi-short/library/poses/{confident,jump,perk}.webp films/mimi-action-add/source/art/{paw,friend-oops}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-loop   # renders/mimi-loop-en.mp4 (English subtitles), renders/mimi-loop.mp4 (Japanese only)
```

The take `renders/app/loop.mov` is in Drive `018. One Loop in Lanclo/Loop_assets/` (app commit 03ea125d). The white masks over the fixtures' QA/demo labels are a table in `hf/index.html` (`MASKS`, screen percentages on the film's clock); move them if a new take shifts the layout.

Not in Git: the recordings, `hf/assets/`, renders, the theme BGM.
