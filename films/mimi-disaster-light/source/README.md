# Rebuild mimi-disaster-light

From the repo root (worktree of branch `feat/mimi-disaster-light`):

```sh
S=films/mimi-disaster-light/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 052. Pronunciation Disasters 11 - Light or Right/Disasters11_Light_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Kokoro lines for Bruno (committed WAV)
sh $S/scripts/art.sh                                            # cut-outs + plate + library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/light-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/light.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.15 s; raw take in Drive Disasters11_Light_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-light                      # -> renders/mimi-disaster-light-en.mp4 and renders/mimi-disaster-light.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); both were copied from episode 3 (rice) and retimed by hand; times live in `cues.json`.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
