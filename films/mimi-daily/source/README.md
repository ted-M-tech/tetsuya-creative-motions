# 「積読」 — source

15-second vertical Mimi short with the real Lanclo daily lesson, built on the shared [Mimi shorts kit](../../../kits/mimi-short/README.md).

| Path | Role |
|---|---|
| `app-capture/DemoWalkthrough.swift` | UI test (`DescribeUITests/testDailyWalkthrough`): launch in Japanese → home → daily lesson → model → record → swipe to the scores → next, with pauses for the edit |
| `app-capture/cut.sh` | Records the walkthrough with `kits/mimi-short/app-capture/capture.sh` (only if the take is missing) and cuts four clips (home, lesson, rec, tip) |
| `art/books.png`, `art/cut/books.webp` | The book tower prop (Codex), cut out; copied to `hf/assets/books.webp` |
| `art/plain.webp` | Flat plate in the page colour, so the Mimi shots can be scaled and moved without an edge |
| `own-voice.json`, `own-voice.receipt.json` | The owner's registered Lanclo voice (`kits/mimi-short/scripts/ownvoice.py`): `model` "Please leave the light on." (`us`) and `rough` "Please leave the right on." (`learner`). The WAVs go to `assets/own-voice/` and are not in Git (Drive `Mimi_06_Unread_Books_assets/own-voice/`); `scripts/lipsync-rough.json` keeps the mouth pattern |
| `scripts/shots.py`, `render.sh`, `mix.py` | Mimi shots (droop, point, listen, speak, think, jump, success), render, sound |
| `hf/` | Edit: books grow and topple, Mimi wrapper, phone frame with the app clips and zooms, white masks over the fixture's QA text, tap ripples, tip card, captions, tags, end card |

## Build

```sh
F=films/mimi-daily/source
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # or copy the WAVs from Drive into $F/assets/own-voice/
$F/app-capture/cut.sh                                  # first run records the app (needs the native-voice-clone checkout and Xcode)
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py
$F/scripts/render.sh
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-daily       # renders/mimi-daily-en.mp4 (English subtitles) and renders/mimi-daily.mp4 (Japanese only)
```

Not in Git: the app recording (`renders/app/daily.mov` and `daily-60.mp4`, kept in Lanclo's Google Drive under 002.SNS/009. Unread Books - Daily Lesson/Mimi_06_Unread_Books_assets with the cut clips), `hf/assets/app/`, Mimi shots, mix, staged kit and the final MP4.

The fixture cannot score a second take ("発音を採点できませんでした"), so all clips come from before the retry. A new recording can shift by a few hundred ms: check a contact sheet (`ffmpeg -i daily-60.mp4 -vf "fps=2,scale=110:-1,tile=11x4"`) and adjust the times in `app-capture/cut.sh`. The white masks in `hf/index.html` are placed for these clips; move them if the layout changes.
