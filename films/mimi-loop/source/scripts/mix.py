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
TYPING = (0.0, 0.25)                      # the question is typed
SEND = 0.3
PILE = (0.02, 0.2, 0.38, 0.56)            # the other apps drop in behind the phone
HISTORY = 1.5                             # the same question in the history
RANK = 2.5                                # the ranking board
REVEALS = [2.8 + (7 - r) * 0.88 for r in range(7, 0, -1)]   # No. 7 ... No. 1
WAKARU = 8.2
MIMI = 9.0                                # 「Lancloなら、全部まとめて回るよ」
COPY = 9.8
LOOP = 10.5
STOPS = (10.75, 12.45, 14.15, 15.85, 17.55, 19.25, 20.95)
STAMPED = (True, True, True, False, True, True, True)
PRESS = 17.67                             # the Action Button (⑤)
OPEN = 17.82
RUN = 0.35
LAP = (22.65, 0.95)
SCORE = (22.65, 23.45)
KEY = 23.65
NIGHT = 25.6
NUMA = 26.0
POP = 27.6
END = 29.0
CTA_TAP = 29.45
SCALE = (72, 74, 76, 77, 79, 81, 83)      # one rising note per stop

m = Mix(30.2, voice_dir=SRC / 'assets/voice')
for i in range(5):
    m.sfx(tap() * 0.18, TYPING[0] + (TYPING[1] - TYPING[0]) * i / 5)
m.sfx(whoosh(0.2, 0.2), SEND)
for at in PILE:
    m.sfx(pofu() * 0.35, at)
m.sfx(boing(False), HISTORY)
m.sfx(pop_seq(4, 0.05, base=74), RANK)
for i, at in enumerate(REVEALS):
    m.sfx(tap() * 0.45, at)
    m.sfx(bell(67 + i, 0.4, 0.05), at + 0.05)
m.sfx(ding(), REVEALS[-1] + 0.05)
m.sfx(boing(False), WAKARU)
m.sfx(whoosh(0.3, 0.3), MIMI)
m.sfx(boing(True), MIMI + 0.05)
m.sfx(pop_seq(3, 0.05, base=76), COPY)
m.sfx(bell(84, 0.8, 0.07), LOOP)
for i, at in enumerate(STOPS):
    if i:
        m.sfx(whoosh(0.3, 0.14), at - RUN)
    m.sfx(bell(SCALE[i], 0.7, 0.09), at)
    if STAMPED[i]:
        m.sfx(tap() * 0.5, at + 0.3)
m.sfx(tap() * 0.8, PRESS)
m.sfx(whoosh(0.35, 0.3), OPEN)
m.sfx(whoosh(0.3, 0.14), LAP[0] - RUN)
for k in range(1, 8):
    m.sfx(tap() * 0.22, LAP[0] + LAP[1] * k / 7)
m.sfx(whoosh(0.6, 0.18), LAP[0])
m.sfx(pop_seq(3, 0.05, base=79), SCORE[0])
m.sfx(ding(), SCORE[1])
m.sfx(bell(79, 1.0, 0.07), KEY)
m.sfx(whoosh(0.5, 0.25), NIGHT)
for i in range(6):                          # swipe, swipe, swipe...
    m.sfx(whoosh(0.15, 0.1), NUMA + 0.1 + i * 0.45)
m.sfx(boing(True), POP)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
