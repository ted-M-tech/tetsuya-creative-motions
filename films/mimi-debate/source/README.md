# Source

```sh
F=films/mimi-debate/source
# 1. app take (shared simulator: hold the lock), or take it from Lanclo Drive
#    002.SNS/019. Lost an Argument in English/Debate_assets/sim-debate_fixture.mov -> $F/renders/app/debate.mov
until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done
xcrun simctl privacy "Lanclo iPhone 18 Pro QA" grant microphone com.lanclo.app
LANCLO_REPO=~/Develop/native-voice-clone PATCH=$F/app-capture/live-mic.patch sh kits/mimi-short/app-capture/capture.sh \
  $F/app-capture/DebateWalkthrough.swift DebateUITests.swift DebateUITests/testDebateWalkthrough $F/renders/app/debate.mov
rmdir /tmp/lanclo-capture.lock
sh $F/scripts/app_track.sh            # -> hf/assets/app/app.mp4 on the film's clock (times measured on the 60 fps resample, see the script)
# 2. voices (Kokoro committed; the owner's voice from Drive) and sound
sh $F/scripts/voices.sh
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # or copy the WAVs from Drive Debate_assets/own-voice/ to $F/assets/own-voice/
uv run --no-project --with numpy python $F/scripts/mix.py
# 3. edit and render
kits/mimi-short/stage.sh $F/hf
mkdir -p $F/hf/assets/art && cp films/mimi-swipe/source/art/friend-{tease,tsukkomi}.webp films/mimi-action-add/source/art/friend-oops.webp \
  films/mimi-action-review/source/art/sheepish.webp kits/mimi-short/library/poses/{stunned,droop,confident}.webp $F/hf/assets/art/
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-debate   # renders/mimi-debate-en.mp4 and renders/mimi-debate.mp4
```

| File | Role |
|---|---|
| `app-capture/DebateWalkthrough.swift` | UI test (replaces `DebateUITests.swift` in the capture checkout): 練習 → ディベート練習 → お金と幸せ → 賛成 → record, send → feedback (scroll) → 返答を録音する → record, send → final feedback |
| `app-capture/live-mic.patch` | Capture-only: `--qa-film-live-mic` makes the QA debate record with the simulator microphone (the fixture otherwise takes a silent take instantly, so no recording screen) |
| `scripts/app_track.sh` | Measured times on the 60 fps take and the cuts on the film's clock |
| `scripts/voices.sh`, `assets/voice/` | Kokoro: the friend's question (`af_bella`) |
| `own-voice.json`, `own-voice.receipt.json` | The owner's own registered Lanclo voice (Gemini gemini-3.8-flash-tts, `kits/mimi-short/scripts/ownvoice.py`): Mimi's rematch answer (accent us). The WAVs (`assets/own-voice/`) are biometric and not in Git; they are in Drive `019. Lost an Argument in English/Debate_assets/own-voice/` |
| `scripts/mix.py` | Cue sheet and sound; the times match `hf/index.html` |
| `hf/index.html` | The edit: two-shots with bubbles, copy card, phone + taps + デモデータ mask + step captions, rematch, punchline, end card; English subtitles (`.sub`, hidden by `<body class="no-subs">`) |

If the take is re-recorded, re-measure on a contact sheet of `renders/app/debate-60.mp4` and update `scripts/app_track.sh`, the tap and mask times in `hf/index.html` and `TAPS` in `scripts/mix.py`.

The take was made against Lanclo `origin/main` 57b4fc93. Not in Git: the recording, `hf/assets/`, renders.
