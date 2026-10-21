# Source

```sh
F=films/mimi-freespeech/source
# 1. app take (shared simulator: hold the lock), Describe a photo with QA fixture data, then cut the two clips
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
LANCLO_REPO=~/Develop/native-voice-clone $F/app-capture/cut.sh   # records renders/app/describe.mov only if missing (FreeSpeechWalkthrough.swift)
rmdir /tmp/lanclo-capture.lock
#    -> hf/assets/app/photo.mp4, result.mp4 (times in app-capture/cut.sh, read by frame number on the 60 fps resample)
# 2. poses (already cut in art/*.webp): codex-p with prompts/01-codex-poses.txt, then kits/mimi-short/scripts/cutout.sh art/<p>.png art/<p>.webp
# 3. voices (committed) and sound
sh $F/scripts/voices.sh
uv run --no-project --with numpy python $F/scripts/mix.py
# 4. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp $F/art/*.webp $F/art/cafe-photo.png $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-freespeech   # renders/mimi-freespeech-en.mp4 and renders/mimi-freespeech.mp4
```

| Path | Role |
|---|---|
| `app-capture/FreeSpeechWalkthrough.swift` | UI test (replaces DescribeUITests.swift in the capture checkout): deep link to the café photo, record (fixture take), send, hold on the feedback, scroll |
| `app-capture/cut.sh` | Records if the take is missing, cuts `photo` (36.4–38.45 s) and `result` (53.1–56.05 s) |
| `art/` | New poses (PNG from Codex, cut WebP) and the app's café photo |
| `assets/voice/` | Kokoro: Mimi's English (af_heart), the friend's French (ff_siwis) |
| `scripts/voices.sh`, `scripts/mix.py` | Voices; cue sheet and mix |
| `hf/index.html` | Edit: hook card, phone with the clips, mask, rings, the fast-forwarded clock, friend scenes, message card, end card, English subtitles |

The take was made against Lanclo `origin/main` e33cd888. Not in Git: the recording (Drive `021. Keep Talking for 3 Minutes/FreeSpeech_assets/simulator_free-speech-describe.mov`, with the two clips), `hf/assets/`, renders.
