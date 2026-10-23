# Source

```sh
F=films/mimi-recheck-r/source
# 1. the Friend's lines in the owner's own voice (paid; skips existing). Or copy from Drive 066. The R Came Back/Recheck_R_assets/own-voice/ into $F/assets/own-voice/
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json
# 2. app take (shared simulator: hold /tmp/lanclo-capture.lock while recording), or take it from Drive Recheck_R_assets/recheck-overview-take.mov
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/recheck-row.patch kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/Walkthrough.swift LessonLevelUITests.swift LessonLevelUITests/testRecheckWalkthrough $F/renders/app/recheck.mov; rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/app.mp4
# 3. art (no new poses), sound, edit, render
sh $F/scripts/art.sh
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-recheck-r   # renders/mimi-recheck-r-en.mp4 and renders/mimi-recheck-r.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (constants at the top of each).
- The capture-only patch gives the fixture's Open slot the shape `lessonSlots()` gives a due re-check (`packages/core/src/weaknessRanking.ts`: `fill('open', due, true)`), so the real `LessonReasonChip` renders 「/ɹ/ (right) · 再確認」. It is never committed to the app.
- The ghost "L" is SVG in `hf/index.html`.
- Not in Git: `assets/own-voice/` (biometric), the recording, `hf/assets/`, renders, the theme BGM.
