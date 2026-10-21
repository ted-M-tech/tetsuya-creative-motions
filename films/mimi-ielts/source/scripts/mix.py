"""IELTS one-month short sound: kit SFX, calendar tears, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-ielts/source/scripts/mix.py
No voices: lines are speech bubbles (Kokoro's Japanese voice is garbled).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
sys.path.insert(0, str(SRC / 'scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402
from tears import TEARS  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = 0.15            # 「あと1か月しかない…！」
COPY = 1.7
APP = 2.8              # the phone comes in
TAPS = (3.45, 4.35, 6.92)   # start interview, record, review
QUICK = (5.1, 5.35, 5.6, 6.0, 6.25)   # questions 2, 4, 7, 8, 9
NOTE = 6.6
MONTAGE = 9.3
MORNING = 12.45
FRIEND = 12.7
CALM = 13.9
END = 15.65
CTA_TAP = 16.25

m = Mix(16.9, voice_dir=SRC / 'assets/voice')
m.sfx(boing(False) * 0.6, HOOK)
m.sfx(pop_seq(3, 0.05, base=76), COPY)
m.sfx(whoosh(0.3, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.7, at)
for at in QUICK:
    m.sfx(tap() * 0.35, at)
m.sfx(ding(0.1), 7.0)          # the estimate and the answers appear
m.sfx(whoosh(0.3, 0.3), MONTAGE)
for i, at in enumerate(TEARS):  # each page torn off; quieter as they speed up
    m.sfx(whoosh(0.12, 0.22 if i < 8 else 0.12), at)
    if i < 8:
        m.sfx(tap() * 0.3, at)
m.sfx(bell(91, 0.8, 0.08), TEARS[-1] + 0.08)   # the test-day page
m.sfx(pofu() * 0.4, MORNING)
m.sfx(boing(True) * 0.5, FRIEND)
m.sfx(bell(88, 0.9, 0.07), CALM)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
