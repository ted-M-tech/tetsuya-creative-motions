# Rebuild mimi-disaster-year

From the repo root (worktree of branch `feat/mimi-disaster-year`):

```sh
S=films/mimi-disaster-year/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 057. Pronunciation Disasters 15 - Year or Ear/Disasters15_Year_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # cut-outs, plate, reused mouth panels (mimi-disaster-beach), library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/year-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/year.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.2 s; raw take in Drive Disasters15_Year_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-year         # -> renders/mimi-disaster-year-en.mp4 and renders/mimi-disaster-year.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); both started from episode 12 (mimi-disaster-hat) with the same beats and ids.
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
