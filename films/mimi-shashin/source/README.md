# 「写真で英語」 — source

15-second vertical Mimi short with the real Lanclo app, built on the shared [Mimi shorts kit](../../../kits/mimi-short/README.md).

| Path | Role |
|---|---|
| `app-capture/DemoWalkthrough.swift` | UI test that walks through 写真描写 (practice tab → photo list → cafe photo → record → send → scroll the feedback) with pauses for the edit |
| `app-capture/cut.sh` | Records the walkthrough with `kits/mimi-short/app-capture/capture.sh` (only if the take is missing) and cuts the six clips |
| `art/plain.webp` | Flat plate in the page colour, so the Mimi shots can be scaled and moved without an edge |
| `art/cafe-photo.png` | The app's cafe photo, taken from the recording, for the hook |
| `assets/voice/` | Kokoro (`af_heart`): "People is sitting... at a cafe." and the app's better sentence; `scripts/voices.sh` |
| `scripts/shots.py`, `render.sh`, `mix.py` | Mimi shots (speak, point, think, listen, jump, success), render, sound |
| `hf/` | Edit: Mimi wrapper, phone frame with the app clips and zooms, tap ripples, correction card, captions, tags, end card |

## Build

```sh
F=films/mimi-shashin/source
$F/app-capture/cut.sh                                  # first run records the app (needs the native-voice-clone checkout and Xcode)
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py
$F/scripts/render.sh
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
cd $F/hf && npx --yes hyperframes@0.8.181 check && npx --yes hyperframes@0.8.181 render --output ../renders/mimi-shashin.mp4 --fps 60
```

Not in Git: the app recording (`renders/app/describe.mov`, kept in Lanclo's Google Drive under 002.SNS/008. English from a Photo/Mimi_05_English_from_a_Photo_2026-10-20_assets with the cut clips), `hf/assets/app/`, Mimi shots, mix, staged kit and the final MP4.

A new recording can shift by a few hundred ms: check a contact sheet (`ffmpeg -i describe-60.mp4 -vf "fps=2,scale=110:-1,tile=14x4"`) and adjust the times in `app-capture/cut.sh`.
