# Rebuild mimi-disaster-thirteen

From the repo root (worktree of branch `feat/mimi-disaster-thirteen`):

```sh
S=films/mimi-disaster-thirteen/source
python3 kits/mimi-short/scripts/ownvoice.py $S/own-voice.json   # owner's voice (paid; skips existing). Or copy from Drive 055. Pronunciation Disasters 13 - Thirteen or Thirty/Disasters13_Thirteen_assets/own-voice/ into $S/assets/own-voice/
sh $S/scripts/art.sh                                            # cut-outs, booth plate + counter front, library poses -> hf/assets/art/
# app take (shared simulator; wrap in the lock /tmp/lanclo-capture.lock):
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$S/app-capture/thirteen-lesson.patch kits/mimi-short/app-capture/capture.sh \
  $S/app-capture/Walkthrough.swift DescribeUITests.swift DescribeUITests/testWalkthrough $S/renders/app/thirteen.mov
sh $S/scripts/app_track.sh                                      # -> hf/assets/app/app.mp4 (4.1 s; raw take in Drive Disasters13_Thirteen_assets/)
uv run --no-project --with numpy python $S/scripts/mix.py       # -> hf/assets/mix.wav
kits/mimi-short/stage.sh $S/hf
kits/mimi-short/render-cuts.sh $S/hf mimi-disaster-thirteen                      # -> renders/mimi-disaster-thirteen-en.mp4 and renders/mimi-disaster-thirteen.mp4
```

- `hf/index.html` and `scripts/mix.py` share the cue sheet (`cues.json`); both started from episode 12 (mimi-disaster-hat) and were retimed for this pair; the mouth card became a stress card (HTML/SVG).
- Not in Git: `assets/own-voice/` (biometric), `hf/assets/`, `renders/`, the BGM.
