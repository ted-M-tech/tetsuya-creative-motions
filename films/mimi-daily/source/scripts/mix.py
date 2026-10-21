"""「積読」（デイリーレッスン） sound: Kokoro voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-daily/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh), af_heart: the lesson's sentence "Please leave the light on."
(stands in for her own voice with native pronunciation) and Mimi's take with an R for the L.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
STACK = 0.1            # books stack up, one pop each
TOPPLE = 1.4           # the tower falls
APP = 2.0              # the real app
TAP = 3.2              # taps デイリーレッスン
MODEL = 3.75           # her own voice, native
SAY = 5.75             # she says it: right for light
RESULT = 7.6           # the score
TIP = 9.6              # light: the sound to fix
JUMP = (11.85, 12.28)
END = 14.0

m = Mix(15.0, voice_dir=SRC / 'assets/voice')
m.sfx(pop_seq(4, 0.22, base=72), STACK)
m.sfx(whoosh(0.3, 0.35), TOPPLE - 0.1)
for i in range(3):
    m.sfx(pofu() * 0.7, TOPPLE + 0.18 + i * 0.09)
m.sfx(whoosh(0.25, 0.25), APP - 0.1)
m.sfx(tap(), TAP)
m.voice('model-af_heart.wav', MODEL)
m.voice('rough-af_heart.wav', SAY, g=0.85)
m.sfx(ding(0.12), RESULT + 0.1)
m.sfx(bell(86, 0.8, 0.1), TIP + 0.2)
m.sfx(boing(True), JUMP[0])
m.sfx(pofu() * 0.6, JUMP[1])
for i, n in enumerate([81, 85, 88]):
    m.sfx(bell(n, 0.9, 0.12), 12.55 + i * 0.07)
m.bed(APP, END, joy_from=RESULT)
m.end_chord(END)
print(m.write(SRC / 'hf/assets/mix.wav'))
