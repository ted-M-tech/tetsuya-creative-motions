# Rebuild mimi-disaster-election

From the repo root (worktree of branch `feat/mimi-disaster-election`):

```sh
S=films/mimi-disaster-election/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 040. Pronunciation Disasters 4 - Election or Erection/Disasters4_Election_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Kokoro line for the other character (committed WAV)
sh $S/scripts/art.sh                                            # cut-outs + plate + library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/election-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/election.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.1 s; raw take in Drive Disasters4_Election_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-election                      # -> renders/mimi-disaster-election-en.mp4 and renders/mimi-disaster-election.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); both were generated from one beat sheet for episodes 2–6 and then kept as plain source.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
