# Rebuild mimi-disaster-walk

From the repo root (worktree of branch `feat/mimi-disaster-walk`):

```sh
S=films/mimi-disaster-walk/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 049. Pronunciation Disasters 8 - Walk or Work/Disasters8_Walk_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Kokoro lines for Bruno (committed WAVs)
kits/mimi-short/stage.sh $S/hf
sh $S/scripts/art.sh                                            # cut-outs + plate + mouth panels + library poses -> hf/assets/art/
# app take (shared simulator; hold the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/walk-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/walk.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.2 s; raw take in Drive Disasters8_Walk_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav (times from cues.json)
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-walk         # -> renders/mimi-disaster-walk-en.mp4 and renders/mimi-disaster-walk.mp4
```

- `cues.json` is the cue sheet: `scripts/mix.py` reads it; `hf/index.html` has the same numbers.
- `art/ref/` holds the reference images given to codex-p (not in Git).
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
