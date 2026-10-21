"""「日記、3日で終わる」 sound: Kokoro voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-nikki/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh), all af_heart: Mimi's rough diary "Yesterday... I go to cafe."
and the corrected line "Yesterday, I went to a cafe." (stands in for her own voice with native pronunciation).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, mokugyo, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
POK = (0.12, 0.42, 0.72)   # the monk taps the wooden fish
DESK = 1.0
TAP = 2.83                 # taps the journal mic
ROUGH = 3.2                # she talks about her day
RESULT = 4.9               # the diary check card
MODEL = 6.72               # the corrected diary in her own voice
PERK = 8.4
SAY = 9.0                  # reads along with the model
CAL = 10.9                 # the calendar fills: day 4..7
JUMP = (11.0, 11.43)
PUMP = 11.65
END = 14.0

m = Mix(15.0, voice_dir=SRC / 'assets/voice')
for at in POK:
    m.sfx(mokugyo(), at)
m.sfx(whoosh(0.25, 0.25), DESK - 0.12)
m.sfx(tap(), TAP)
m.voice('rough-af_heart.wav', ROUGH)
m.sfx(whoosh(0.25, 0.25), RESULT)
for i in range(5):
    m.sfx(tap() * 0.35, RESULT + 0.15 + i * 0.07)
m.sfx(ding(0.12), RESULT + 0.75)
m.voice('model-af_heart.wav', MODEL)
for i, n in enumerate([86, 90, 93, 98]):
    m.sfx(bell(n, 1.0, 0.07), PERK + i * 0.06)
m.voice('model-af_heart.wav', SAY - 0.03, g=0.5)
m.voice('model-af_heart.wav', SAY, g=0.85)
m.sfx(pop_seq(4, 0.18), CAL + 0.25)
m.sfx(boing(True), JUMP[0])
m.sfx(pofu() * 0.6, JUMP[1])
for i, n in enumerate([81, 85, 88]):
    m.sfx(bell(n, 0.9, 0.12), PUMP + i * 0.07)
m.sfx(ding(), 12.85)
m.bed(DESK, END, joy_from=PERK)
m.end_chord(END)
print(m.write(SRC / 'hf/assets/mix.wav'))
