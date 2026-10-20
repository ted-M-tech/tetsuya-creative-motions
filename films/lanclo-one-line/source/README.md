# Source

Every frame is drawn with pycairo and piped to ffmpeg; music and SFX are synthesised with numpy. Needs `uv` (or Python 3.11+ with pycairo, numpy, pillow) and `ffmpeg`.

```sh
cd films/lanclo-one-line/source
./fetch-fonts.sh            # Zen Maru Gothic (OFL) from google/fonts

# PV, 16:9
uv run --no-project --with numpy python scripts/audio.py renders/mix.wav
uv run --no-project --with pycairo --with numpy --with pillow python scripts/render.py renders/lanclo-one-line-16x9.mp4 --audio renders/mix.wav

# English journal short, 9:16
uv run --no-project --with numpy python scripts/journal_audio.py renders/journal-mix.wav
uv run --no-project --with pycairo --with numpy --with pillow python scripts/journal.py renders/lanclo-journal-9x16.mp4 --audio renders/journal-mix.wav

# Stills for checking a layout (half size): --scale 0.5 --still 3.0,12.5
```

| File | Role |
|---|---|
| `scripts/timeline.py` | PV beats on a "story clock"; `WARP` maps output time to it so type gets reading time while the music keeps tempo |
| `scripts/render.py` | PV picture: the line, camera, scenes, subtitles, grain. Shared drawing helpers |
| `scripts/audio.py` | PV sound: voice clips, music, SFX, ducking, loudness |
| `scripts/journal_timeline.py` / `journal.py` / `journal_audio.py` | 9:16 short; imports helpers and instruments from the PV scripts |

`assets/voice/own.mp3` and `model.mp3` (the LP comparison clips) are not in Git. Without them the PV renders with a stand-in waveform shape and no voice; the journal short does not use them. Rendered files go to `renders/` (ignored).
