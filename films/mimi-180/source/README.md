# Source

```sh
F=films/mimi-180/source
# 1. app take (shared simulator: wrap in the /tmp/lanclo-capture.lock lock, see the kit README); the patch is capture-only
PATCH=$F/app-capture/really-take.patch LANCLO_REPO=~/Develop/native-voice-clone kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/ReallyWalkthrough.swift DescribeUITests.swift DescribeUITests/testReallyWalkthrough $F/renders/app/really.mov
sh $F/scripts/app_track.sh                       # -> hf/assets/app/app.mp4 on the film's clock (cuts measured in the script)
# 2. the owner's voice (paid generation; reruns skip existing clips)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # -> assets/own-voice/habit.wav (learner), fix.wav (us)
# 3. sound (word times measured in the script's docstring)
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp kits/mimi-short/library/poses/{speak-open,speak-closed,confident,stunned}.webp films/mimi-swipe/source/art/{fluster,friend-tsukkomi}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-180    # renders/mimi-180-en.mp4 and renders/mimi-180.mp4
```

Not in Git: the recordings (`renders/app/`, Drive `033. Talked for 180 Seconds/Talked180_assets/`), the voice clips `assets/own-voice/` (the owner's biometric data; Drive `Talked180_assets/own-voice/`), `hf/assets/`, renders.
App build used: native-voice-clone `5998d20d` (origin/main on 2026-10-21).
