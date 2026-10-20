# 「自分の声、むり」 — source (work in progress)

15-second vertical short with the 3D Mimi master. Stage: previs and animatic.

```sh
cd films/mimi-jibun-no-koe/source
./fetch-fonts.sh                                               # Zen Maru Gothic
uv run --no-project --with pillow python scripts/screens.py    # phone screens
blender -b -P scripts/previs.py -- --pct 40                    # one still per key pose
uv run --no-project --with numpy --with pillow python scripts/animatic.py   # renders/animatic.mp4
```

- `scripts/shots.py`: poses, key stills and the shot timeline (captions, timing, notes).
- `scripts/previs.py`: desk set, phone with screens, cameras, posing on the Mimi rig (imports `films/mimi-3d/source/scripts/mimi.py`).
- `scripts/animatic.py`: stills on the timeline with the voice clips, placeholder SFX, captions, end card.
- `assets/voice/` (not in Git): `own.mp3` and `model.mp3`, the LP comparison clips.
