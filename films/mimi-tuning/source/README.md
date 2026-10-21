# Source

```sh
F=films/mimi-tuning/source
# 1. app take (shared simulator: hold the lock): 声の調整 with fixture data, then the generated-preview list
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/british-preview.patch kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/TuningWalkthrough.swift EnrollmentRecoveryUITests.swift EnrollmentRecoveryUITests/testTuningWalkthrough $F/renders/app/tuning.mov
rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/app.mp4 on the film's clock (timings measured on the 60 fps resample, see the script)
# 2. poses (already cut in art/*.webp): codex-p with prompts/01-codex-poses.txt (images: mimi-jibun-no-koe master.png, success.png,
#    mimi-voice mimi-phone.webp, mimi-tease.webp), then kits/mimi-short/scripts/cutout.sh art/<p>.png art/<p>.webp
# 3. voices (committed) and sound
sh $F/scripts/voices.sh
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp films/mimi-swipe/source/art/friend-tsukkomi.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-tuning   # renders/mimi-tuning-en.mp4 and renders/mimi-tuning.mp4
```

The take was made against Lanclo `origin/main` 57b4fc93. 「試聴音声を作る」 is never pressed (it calls the voice provider); the English voices are Kokoro stand-ins. Not in Git: the recording (Drive `023. Voice Tuning/Tuning_assets/simulator_voice-tuning.mov`), `hf/assets/`, renders.
