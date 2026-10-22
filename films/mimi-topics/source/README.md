# Source

```sh
F=films/mimi-topics/source
# 1. app take (shared simulator: wrap in the /tmp/lanclo-capture.lock lock, see the kit README)
LANCLO_REPO=~/Develop/native-voice-clone kits/mimi-short/app-capture/capture.sh $F/app-capture/TopicsWalkthrough.swift \
  SituationUITests.swift SituationUITests/testTopicsWalkthrough $F/renders/app/topics.mov
sh $F/scripts/app_track.sh                       # -> hf/assets/app/app.mp4 on the film's clock (cuts measured in the script)
# 2. the owner's voice (paid generation; reruns skip existing clips)
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # -> assets/own-voice/light.wav
# 3. sound
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp films/mimi-action-review/source/art/sheepish.webp kits/mimi-short/library/poses/{stunned,point,speak-open,speak-closed,confident}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-topics  # renders/mimi-topics-en.mp4 and renders/mimi-topics.mp4
```

Not in Git: the recordings (`renders/app/`, Drive `031. AI Chat Never Knows What to Talk About/Topics_assets/`), the voice clip `assets/own-voice/light.wav` (the owner's biometric data; Drive `Topics_assets/own-voice/`), `hf/assets/`, renders. App build used: native-voice-clone `5998d20d` (origin/main on 2026-10-21).
