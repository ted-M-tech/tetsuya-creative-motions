"""Action Button ③ (Today's lesson, morning in bed) sound: mum's voice, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-action-lesson/source/scripts/mix.py
No voices: mum's call is a speech bubble (the Kokoro Japanese take was garbled; kept in assets/voice/ for reference).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
PRESS = 0.95           # the paw presses the Action Button
TINY = 1.1             # a tiny Mimi pops out
OPEN = 1.45            # she pulls the dark screen open
COPY = (2.04, 2.65)    # the copy card, ③ lights up
RECORD = 5.6           # she taps record
MOM = 8.4              # mum calls from downstairs
PROUD = 9.8
CARDS2 = 12.2
END = 15.7
CTA_TAP = 16.15

m = Mix(16.8, voice_dir=SRC / 'assets/voice')
m.sfx(tap() * 0.4, 0.2)
m.sfx(tap() * 0.8, PRESS)
m.sfx(boing(True), TINY)
m.sfx(bell(93, 0.6, 0.06), TINY + 0.05)
m.sfx(whoosh(0.4, 0.35), OPEN)
m.sfx(pop_seq(3, 0.05, base=76), COPY[0])
m.sfx(pofu() * 0.5, COPY[1])
m.sfx(tap() * 0.6, RECORD)
m.sfx(bell(81, 0.6, 0.05), RECORD + 0.1)
# no spoken line: Kokoro's only Japanese voice garbled it; the bubble and subtitle carry it
m.sfx(boing(True), MOM + 0.05)
m.sfx(pofu() * 0.5, MOM + 0.6)
m.sfx(pop_seq(3, 0.06, base=79), PROUD)
m.sfx(pop_seq(3, 0.05, base=76), CARDS2)
m.sfx(bell(88, 0.7, 0.08), CARDS2 + 0.35)
for at in (12.63, 13.3, 14.25):  # taps through the in-app settings
    m.sfx(tap() * 0.5, at)
m.bed(COPY[0], END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
