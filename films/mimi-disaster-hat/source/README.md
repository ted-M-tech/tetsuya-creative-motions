# Rebuild mimi-disaster-hat

From the repo root (worktree of branch `feat/mimi-disaster-hat`):

```sh
S=films/mimi-disaster-hat/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 053. Pronunciation Disasters 12 - Hat or Hut/Disasters12_Hat_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Kokoro line for Coco (committed WAV)
sh $S/scripts/art.sh                                            # cut-outs, mouth panels, library plate + poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/hat-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/hat.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.2 s; raw take in Drive Disasters12_Hat_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-hat                      # -> renders/mimi-disaster-hat-en.mp4 and renders/mimi-disaster-hat.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); both started from episode 6 (mimi-disaster-peace) and were retimed for this pair.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
