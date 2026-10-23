# Rebuild mimi-disaster-fork

From the repo root (worktree of branch `feat/mimi-disaster-fork`):

```sh
S=films/mimi-disaster-fork/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 051. Pronunciation Disasters 10 - Fork or Fck/Disasters10_Fork_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Kokoro line for the other character (committed WAV)
sh $S/scripts/art.sh                                            # cut-outs + plate + library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/fork-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/fork.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (3.9 s; raw take in Drive Disasters10_Fork_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-fork                      # -> renders/mimi-disaster-fork-en.mp4 and renders/mimi-disaster-fork.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); copied from episode 5 (mimi-disaster-coke) and retimed for the longer line "Excuse me, can I get a f*ck?" (the learner take is placed in two pieces, `T0` and `T1`, to shorten its pause).
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
