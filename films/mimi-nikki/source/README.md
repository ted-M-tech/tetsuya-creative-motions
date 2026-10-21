# 「日記、3日で終わる」 — source

15-second vertical Mimi short, built on the shared [Mimi shorts kit](../../../kits/mimi-short/README.md). This folder holds only what is specific to the episode.

| Path | Role |
|---|---|
| `art/*.png` | Codex output as drawn (bozu, notebook, artist). The cut-outs live in the Mimi 2D library (`kits/mimi-short/library`) |
| `art/journal/*.jpg` | The app's journal art, one picture per day (cropped 3×2 from `films/lanclo-one-line/source/assets/journal-art.png`) |
| `assets/voice/` | Kokoro voice lines (`af_heart`): "Yesterday... I go to cafe." and "Yesterday, I went to a cafe."; rebuild with `scripts/voices.sh` |
| `scripts/shots.py` | The 10 Rive shots. Episode acts: pok (wooden fish), talk (lip-sync cached in `scripts/lipsync-rough.json`), paint, boast |
| `scripts/render.sh` | Rive shots → `renders/rive/*.mp4` → `hf/assets/shots/` |
| `scripts/mix.py` | Cue sheet and sound → `hf/assets/mix.wav` |
| `hf/` | HyperFrames edit: shots, notebook, journal UI on the phone, diary check card, the picture painting in, the picture calendar, captions, end card |

## Build

From the repository root (Node 24, uv, ffmpeg, ImageMagick, Rive CLI 1.6):

```sh
F=films/mimi-nikki/source
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py
$F/scripts/render.sh                                   # about 6 minutes
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-nikki       # renders/mimi-nikki-en.mp4 (English subtitles) and renders/mimi-nikki.mp4 (Japanese only)
```

Not in Git: `renders/`, `hf/assets/shots/`, `hf/assets/mix.wav`, `hf/assets/kit/` and the final MP4.

The cue times in `scripts/mix.py` and in `hf/index.html` must change together.
