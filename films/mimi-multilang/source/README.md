# Source

```sh
F=films/mimi-multilang/source
# 1. app take (shared simulator: hold the lock): AI Voice, switch the language to Français and 한국어, fixture data
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/voice-stub.patch kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/MultilangWalkthrough.swift MeaningPracticeUITests.swift MeaningPracticeUITests/testMultilangWalkthrough $F/renders/app/voice.mov
rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/app.mp4 on the film's clock (timings measured on the 60 fps resample, see the script)
# 2. poses (already cut in art/*.webp): codex-p with prompts/01-codex-poses.txt, then kits/mimi-short/scripts/cutout.sh art/<p>.png art/<p>.webp
# 3. voices (the owner's own registered Lanclo voice; paid, generated once; clips not in Git: restore from Drive Multilang_assets/own-voice/ into $F/assets/own-voice/) and sound
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # skips clips that already exist
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-multilang   # renders/mimi-multilang-en.mp4 and renders/mimi-multilang.mp4
```

The take was made against Lanclo `origin/main` 57b4fc93 (the AI Voice screen with the 🌐 language menu in the toolbar; an earlier layout had a different screen, so re-measure `app_track.sh` after a re-take). Not in Git: the own-voice clips (Drive `Multilang_assets/own-voice/`), the recording (Drive `022. Your Voice in Every Language/Multilang_assets/simulator_voice-language.mov`), `hf/assets/`, renders.
