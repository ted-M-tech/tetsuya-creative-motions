# Rebuild mimi-disaster-lunch

From the repo root (worktree of branch `feat/mimi-disaster-lunch`):

```sh
S=films/mimi-disaster-lunch/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 050. Pronunciation Disasters 9 - Lunch or Launch/Disasters9_Lunch_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Coco's Kokoro line (committed WAV)
sh $S/scripts/art.sh                                            # cut-outs + plate + mouth panels + library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/lunch-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/lunch.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.2 s; raw take in Drive Disasters9_Lunch_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-lunch        # -> renders/mimi-disaster-lunch-en.mp4 and renders/mimi-disaster-lunch.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`).
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
