# Source

```sh
F=films/mimi-ielts/source
# the simulator take (shared simulator: hold the lock), app checkout cached in ~/Library/Caches/lanclo-app-capture
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone kits/mimi-short/app-capture/capture.sh $F/app-capture/MockWalkthrough.swift \
  IELTSSpeakingUITests.swift IELTSSpeakingUITests/testMockWalkthrough $F/renders/app/mock.mov; rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh                 # renders/app/mock-60.mp4 -> hf/assets/app/app.mp4 on the film's clock (cut list inside)
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/{nervous,tear,practice,calm}.webp kits/mimi-short/library/poses/{confident,point}.webp \
  films/mimi-action-add/source/art/friend-oops.webp $F/hf/assets/art/
uv run --no-project --with numpy python $F/scripts/mix.py
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-ielts   # renders/mimi-ielts-en.mp4 (English subtitles) and renders/mimi-ielts.mp4 (Japanese only)
```

Recorded against Lanclo `origin/main` 03ea125d. Not in Git: the recording (Drive `016. One Month to IELTS/IELTS_assets/simulator_ielts-mock-exam.mov`), `hf/assets/`, renders. `art/*.png` are the codex-p originals, `art/*.webp` the cutouts (`kits/mimi-short/scripts/cutout.sh`).
