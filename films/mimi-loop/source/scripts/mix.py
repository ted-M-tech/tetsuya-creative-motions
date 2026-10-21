"""「ひとつのループ」 (mimi-loop) sound: kit SFX on the cue sheet and the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-loop/source/scripts/mix.py
No voices: every line is a speech bubble (Kokoro's Japanese voice is garbled).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
TYPING = (0.1, 0.75)                      # the question is typed
SEND = 0.85
PILE = (0.5, 0.95, 1.4, 1.85)             # the other apps drop in behind the phone
RANK = 3.0                                # the ranking board
REVEALS = [3.45 + (7 - r) * 0.85 for r in range(7, 0, -1)]   # No. 7 ... No. 1
WAKARU = 8.6
MIMI = 9.4                                # 「Lancloなら、勝手に回るよ」
COPY = 10.5
PRESS = 11.95                             # the Action Button
OPEN = 12.1
LOOP = 12.7
STOPS = (13.0, 14.7, 16.4, 18.1, 19.8, 21.5, 23.2)
STAMPED = (True, True, True, True, False, True, True)
RUN = 0.4
LAPS = ((24.9, 1.0), (25.9, 0.6))
SCORE = (24.9, 25.4, 25.9)
KEY = 26.6
NIGHT = 28.6
NUMA = 29.3
POP = 30.7
END = 32.1
CTA_TAP = 32.55
SCALE = (72, 74, 76, 77, 79, 81, 83)      # one rising note per stop

m = Mix(33.3, voice_dir=SRC / 'assets/voice')
n = 8
for i in range(n):
    m.sfx(tap() * 0.18, TYPING[0] + (TYPING[1] - TYPING[0]) * i / n)
m.sfx(whoosh(0.2, 0.2), SEND)
for at in PILE:
    m.sfx(pofu() * 0.4, at)
m.sfx(pop_seq(4, 0.05, base=74), RANK)
for i, at in enumerate(REVEALS):
    m.sfx(tap() * 0.45, at)
    m.sfx(bell(67 + i, 0.4, 0.05), at + 0.05)
m.sfx(ding(), REVEALS[-1] + 0.05)
m.sfx(boing(False), WAKARU)
m.sfx(whoosh(0.3, 0.3), MIMI)
m.sfx(boing(True), MIMI + 0.1)
m.sfx(pop_seq(3, 0.05, base=76), COPY)
m.sfx(tap() * 0.8, PRESS)
m.sfx(whoosh(0.4, 0.35), OPEN)
m.sfx(tap() * 0.5, 11.65 + 0.3)            # the Action Button stamp
m.sfx(bell(84, 0.8, 0.07), LOOP)
for i, at in enumerate(STOPS):
    if i:
        m.sfx(whoosh(0.3, 0.14), at - RUN)
    m.sfx(bell(SCALE[i], 0.7, 0.09), at)
    if STAMPED[i]:
        m.sfx(tap() * 0.5, at + 0.35)
m.sfx(whoosh(0.3, 0.14), LAPS[0][0] - RUN)
for t0, d in LAPS:
    for k in range(1, 8):
        m.sfx(tap() * 0.22, t0 + d * k / 7)
    m.sfx(whoosh(min(d, 0.6), 0.18), t0)
m.sfx(pop_seq(3, 0.05, base=79), SCORE[0])
for at in SCORE[1:]:
    m.sfx(ding(), at)
m.sfx(bell(79, 1.0, 0.07), KEY)
m.sfx(whoosh(0.5, 0.25), NIGHT)
for i in range(6):                          # swipe, swipe, swipe...
    m.sfx(whoosh(0.15, 0.1), NUMA + 0.1 + i * 0.45)
m.sfx(boing(True), POP)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
