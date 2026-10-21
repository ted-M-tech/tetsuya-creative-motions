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

# App intro short, 9:16 (needs the non-Git inputs below)
sh scripts/intro_vo.sh      # cuts assets/voice/vo-intro/Mimi.m4a into v1..v10 at 1.2x
swift scripts/greetings.swift   # only if the greetings change; assets/greet/ is committed
uv run --no-project --with pycairo --with numpy --with pillow python scripts/intro_audio.py renders/intro-mix.wav
uv run --no-project --with pycairo --with numpy --with pillow python scripts/intro.py renders/lanclo-intro-9x16.mp4 --audio renders/intro-mix.wav

# Stills for checking a layout (half size): --scale 0.5 --still 3.0,12.5
```

| File | Role |
|---|---|
| `scripts/timeline.py` | PV beats on a "story clock"; `WARP` maps output time to it so type gets reading time while the music keeps tempo |
| `scripts/render.py` | PV picture: the line, camera, scenes, subtitles, grain. Shared drawing helpers |
| `scripts/audio.py` | PV sound: voice clips, music, SFX, ducking, loudness |
| `scripts/journal_timeline.py` / `journal.py` / `journal_audio.py` | 9:16 short; imports helpers and instruments from the PV scripts |
| `scripts/intro_timeline.py` / `intro.py` / `intro_audio.py` | 9:16 app intro ([shorts/intro](../shorts/intro/README.md)): narration line starts, beats, picture, sound |
| `scripts/intro_vo.sh` | Cuts the narration take into ten lines at 1.2x (cut points from silencedetect) |
| `scripts/greetings.swift` | Renders the 17 greetings to `assets/greet/` with CoreText (PIL here cannot shape Devanagari, Bengali, Thai) |

Not in Git, for the intro: the narration take `assets/voice/vo-intro/Mimi.m4a` (Lanclo's Google Drive, `002.SNS/010. App Introduction/Mimi.m4a`) and the theme BGM `kits/mimi-short/library/bgm/everyone-get-up.mp3` (Drive `002.SNS/_BGM/Everyone_Get_Up.mp3`; without it the code-made bed plays).

`assets/voice/own.mp3` and `model.mp3` (the LP comparison clips) are not in Git. Without them the PV renders with a stand-in waveform shape and no voice; the journal short does not use them. Rendered files go to `renders/` (ignored).
