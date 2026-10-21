# Rebuild mimi-disaster-coke

From the repo root (worktree of branch `feat/mimi-disaster-coke`):

```sh
S=films/mimi-disaster-coke/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 041. Pronunciation Disasters 5 - Coke or Cck/Disasters5_Coke_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Kokoro line for the other character (committed WAV)
sh $S/scripts/art.sh                                            # cut-outs + plate + library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/coke-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/coke.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (3.9 s; raw take in Drive Disasters5_Coke_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-coke                      # -> renders/mimi-disaster-coke-en.mp4 and renders/mimi-disaster-coke.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); both were generated from one beat sheet for episodes 2–6 and then kept as plain source.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
