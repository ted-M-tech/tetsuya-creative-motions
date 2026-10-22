# 「think が sink に」 — source

15-second vertical Mimi short, built on the shared [Mimi shorts kit](../../../kits/mimi-short/README.md). This folder holds only what is specific to the episode.

| Path | Role |
|---|---|
| `art/*.png` | Codex output as drawn (confident, stunned, sink, bulb). The cut-outs live in the Mimi 2D library (`kits/mimi-short/library/poses`, `props`) |
| `own-voice.json`, `own-voice.receipt.json` | Mimi's two lines in the owner's own registered Lanclo voice ("I sink so!" learner accent, "I think so." General American). `kits/mimi-short/scripts/ownvoice.py` writes them to `assets/own-voice/` (not in Git; copies in Drive `Mimi_02_Think_Becomes_Sink_assets/own-voice/`) |
| `scripts/shots.py` | The 11 Rive shots: pose, act, length. Episode acts: boast, stun, say (lip-sync from the voice line, cached in `scripts/lipsync-right.json`) |
| `scripts/render.sh` | Rive shots → `renders/rive/*.mp4` → `hf/assets/shots/` |
| `scripts/mix.py` | Cue sheet and sound → `hf/assets/mix.wav` |
| `hf/` | HyperFrames edit: shots, falling sinks, puffs, bulb, phone UI, captions, tags, radar card, end card |

## Build

From the repository root (Node 24, uv, ffmpeg, ImageMagick, Rive CLI 1.6):

```sh
F=films/mimi-think-sink/source
python3 kits/mimi-short/scripts/ownvoice.py $F/own-voice.json   # or copy the WAVs from Drive Mimi_02_Think_Becomes_Sink_assets/own-voice/ into $F/assets/own-voice/
uv run --no-project --with scipy --with pillow --with numpy python $F/scripts/shots.py
$F/scripts/render.sh                                   # about 6 minutes
uv run --no-project --with numpy python $F/scripts/mix.py
kits/mimi-short/stage.sh $F/hf
(cd $F/hf && npx --yes hyperframes@0.8.181 check)
kits/mimi-short/render-cuts.sh $F/hf mimi-think-sink       # renders/mimi-think-sink-en.mp4 (English subtitles) and renders/mimi-think-sink.mp4 (Japanese only)
```

Not in Git: `renders/`, `hf/assets/shots/`, `hf/assets/mix.wav`, `hf/assets/kit/` (all rebuilt by the steps above) and the final MP4 (published on the gallery).

The cue times in `scripts/mix.py` and in `hf/index.html` must change together.
