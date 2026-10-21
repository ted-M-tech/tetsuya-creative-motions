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
APP_TAPS = (0.35, 0.8, 1.25, 1.7, 2.15)   # each app starts... and stops 0.45 s later
SIGH = 2.6                                 # 「勉強が続かない…」
MIMI = 4.0                                 # 「それ、全部ひとつで回るよ」
COPY = (5.15, 5.7)                         # the scattered words, then they line up
LOOP = 6.3                                 # the ring and Lanclo appear
STOPS = (6.8, 9.2, 11.6, 14.4, 17.0, 19.4, 21.8)
RUN = 0.45
LAPS = ((24.0, 1.4), (25.4, 1.0), (26.4, 0.6))
SCORE = (24.1, 25.4, 26.4)
WOW = 27.05
END = 29.0
CTA_TAP = 29.45
SCALE = (72, 74, 76, 77, 79, 81, 83)       # one rising note per stop

m = Mix(30.2, voice_dir=SRC / 'assets/voice')
for at in APP_TAPS:
    m.sfx(tap() * 0.5, at)
    m.sfx(pofu() * 0.35, at + 0.45)
m.sfx(boing(False), SIGH)
m.sfx(whoosh(0.3, 0.3), MIMI)
m.sfx(boing(True), MIMI + 0.12)
m.sfx(pop_seq(5, 0.04, base=76), COPY[0])
m.sfx(ding(), COPY[1])
m.sfx(whoosh(0.4, 0.35), LOOP)
m.sfx(bell(84, 0.8, 0.07), LOOP + 0.2)
for i, at in enumerate(STOPS):
    if i:
        m.sfx(whoosh(0.3, 0.14), at - RUN)
    m.sfx(bell(SCALE[i], 0.7, 0.09), at)
    m.sfx(tap() * 0.35, at)
m.sfx(whoosh(0.3, 0.14), LAPS[0][0] - RUN)
for t0, d in LAPS:
    for n in range(1, 8):
        m.sfx(tap() * 0.22, t0 + d * n / 7)
    m.sfx(whoosh(min(d, 0.6), 0.18), t0)
for at in SCORE[1:]:
    m.sfx(ding(), at)
m.sfx(pop_seq(3, 0.05, base=79), SCORE[0])
m.sfx(boing(True), WOW)
m.sfx(pop_seq(3, 0.05, base=76), WOW + 0.1)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
