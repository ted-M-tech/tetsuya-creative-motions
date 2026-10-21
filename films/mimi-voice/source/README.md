# Source

```sh
F=films/mimi-voice/source
# 1. app take (shared simulator: hold the lock), first-time voice setup with fixture data
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
xcrun simctl privacy "Lanclo iPhone 18 Pro QA" grant microphone com.lanclo.app
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/first-voice.patch kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/VoiceSetupWalkthrough.swift EnrollmentRecoveryUITests.swift EnrollmentRecoveryUITests/testVoiceSetupWalkthrough $F/renders/app/setup.mov
rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/app.mp4 on the film's clock (timings measured on the 60 fps resample, see the script)
# 2. poses (already cut in art/*.webp): codex-p with prompts/01-codex-poses.txt, then kits/mimi-short/scripts/cutout.sh art/<p>.png art/<p>.webp
# 3. voices (committed) and sound
sh $F/scripts/voices.sh
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp films/mimi-action-add/source/art/friend-aww.webp films/mimi-swipe/source/art/friend-oops.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-voice   # renders/mimi-voice-en.mp4 and renders/mimi-voice.mp4
```

The take was made against Lanclo `origin/main` 03ea125d. Not in Git: the recording (Drive `015. AI Voice in 1 Minute/AIV_assets/simulator_voice-setup.mov`), `hf/assets/`, renders.
