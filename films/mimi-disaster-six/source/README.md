# Rebuild mimi-disaster-six

From the repo root (worktree of branch `feat/mimi-disaster-six`):

```sh
S=films/mimi-disaster-six/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). learner-sex.wav is take 1 with its vowel edited:
#   uv run --no-project --with praat-parselmouth --with numpy python $S/scripts/vowel_shift.py <take1.wav> $S/assets/own-voice/learner-sex.wav 1.795 1.872 1.35 0.92
#   Or copy from Drive 048. Pronunciation Disasters 7 - Six or Sx/Disasters7_Six_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/voices.sh                                         # Kokoro line for Pippa (committed WAV)
sh $S/scripts/art.sh                                            # cut-outs + plate + library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/six-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/six.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.2 s; raw take in Drive Disasters7_Six_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-six                      # -> renders/mimi-disaster-six-en.mp4 and renders/mimi-disaster-six.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); copied from episode 6 (mimi-disaster-peace) and edited.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
