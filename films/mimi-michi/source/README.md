# 「道を聞かれて固まる」 — source

15-second vertical Mimi short, built on the shared [Mimi shorts kit](../../../kits/mimi-short/README.md). This folder holds only what is specific to the episode.

| Path | Role |
|---|---|
| `art/*.png` | Codex output as drawn (street, point, ice). The cut-outs and the framed street plate live in the Mimi 2D library (`kits/mimi-short/library`) |
| `assets/voice/` | Kokoro voice lines: the passer-by (`bm_george`) asks and thanks; Mimi's "Uh..." and the answer (`af_heart`). Rebuild with `scripts/voices.sh` |
| `scripts/shots.py` | The 9 Rive shots (street plate for the street, desk for the rest). Episode acts: freeze, say (lip-sync cached in `scripts/lipsync-answer.json`), direct |
| `scripts/render.sh` | Rive shots → `renders/rive/*.mp4` → `hf/assets/shots/` |
| `scripts/mix.py` | Cue sheet and sound → `hf/assets/mix.wav` |
| `hf/` | HyperFrames edit: shots, ice forming and shattering, speech bubbles, phone UI, captions, tags, radar card, end card |

## Build

From the repository root (Node 24, uv, ffmpeg, ImageMagick, Rive CLI 1.6):

```sh
F=films/mimi-michi/source
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py
$F/scripts/render.sh                                   # about 6 minutes
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-michi       # renders/mimi-michi-en.mp4 (English subtitles) and renders/mimi-michi.mp4 (Japanese only)
```

Not in Git: `renders/`, `hf/assets/shots/`, `hf/assets/mix.wav`, `hf/assets/kit/` and the final MP4.

The street plate was framed from `art/street.png` so the feet point (480, 1330) lands on the pavement: `magick art/street.png -crop 1080x1220+0+700 +repage -resize 1700x1920 -crop 1080x1920+620+0 +repage street.webp`.

The cue times in `scripts/mix.py` and in `hf/index.html` must change together.
