"""「think が sink に」 sound: Kokoro voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-think-sink/source/scripts/mix.py
Voices (not in Git, rebuild with the commands in ../README.md): assets/voice/wrong-af_heart.wav "I sink so!",
right-af_heart.wav "I think so." (stands in for Mimi's own voice with native pronunciation).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, clang, ding, pofu, poof, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
WRONG, SINK1 = 0.12, 0.45            # "I sink so!" -> the first sink lands
WRONG2, SINK2 = 1.25, 1.80           # said again, unsure -> the second sink
TAP = 2.63                           # taps Lanclo
MODEL = 3.05                         # her own voice, native "think"
PERK = 4.4
RESULT = 5.0
SAY = 7.2                            # practice: says it with the model
POOF1, POOF2, BULB = 9.1, 9.35, 9.7
JUMP = (10.3, 10.73)
PUMP = 10.95
PROUD = 12.3
END = 14.0

m = Mix(15.0, voice_dir=SRC / 'assets/voice')
m.voice('wrong-af_heart.wav', WRONG)
m.sfx(whoosh(0.35, 0.3), SINK1 - 0.33)
m.sfx(clang(), SINK1)
m.voice('wrong-af_heart.wav', WRONG2, g=0.7, speed=0.92)
m.sfx(whoosh(0.2, 0.3), SINK2 - 0.18)
m.sfx(clang(0.7), SINK2)
m.sfx(tap(), TAP)
m.voice('right-af_heart.wav', MODEL)
for i, n in enumerate([86, 90, 93, 98]):
    m.sfx(bell(n, 1.0, 0.07), PERK + i * 0.06)
m.sfx(whoosh(0.25, 0.25), RESULT)
for i in range(5):
    m.sfx(tap() * 0.35, RESULT + 0.15 + i * 0.07)
m.sfx(ding(0.12), RESULT + 0.75)
m.voice('right-af_heart.wav', SAY - 0.03, g=0.5)     # the model, under her
m.voice('right-af_heart.wav', SAY, g=0.85)
m.sfx(poof(), POOF1)
m.sfx(poof(), POOF2)
m.sfx(ding(), BULB)
m.sfx(boing(True), JUMP[0])
m.sfx(pofu() * 0.6, JUMP[1])
for i, n in enumerate([81, 85, 88]):
    m.sfx(bell(n, 0.9, 0.12), PUMP + i * 0.07)
m.voice('right-af_heart.wav', PROUD)
m.bed(1.0, END, joy_from=PERK)
m.end_chord(END)
print(m.write(SRC / 'hf/assets/mix.wav'))
