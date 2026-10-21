"""Action Button ① (Add a phrase, "Bless your heart") sound: the friend's line, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-action-add/source/scripts/mix.py
Voice in assets/voice/ (rebuild with scripts/voices.sh): af_bella says "Aww, bless your heart."
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, clang, ding, pochi, pofu, pop_seq, tap, whoosh, t  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times. The friends' two-shot runs 0-0.8 before the button.
TALK = 0.1             # the friend: "Aww, bless your heart."
SH = 0.8
PRESS = 0.15 + SH           # the paw presses the Action Button
TINY = 0.3 + SH             # a tiny Mimi pops out
OPEN = 0.65 + SH            # she pulls the dark screen open
CARDS = (1.24 + SH, 1.62 + SH)   # the three shortcuts fan out; ① comes forward
TYPE = (2.25 + SH, 3.5 + SH)      # typing "Bless your heart"
MEANING = (4.4 + SH, 5.05 + SH)  # tap Generate meaning; the meaning appears
REALISE = 6.2 + SH          # おめでたい人だね: her smile freezes
ANGRY = 7.6 + SH            # she shouts at the friend
EXAMPLE = (9.65 + SH, 10.25 + SH)
SAVE = 11.0 + SH
CARDS2 = 11.4 + SH
END = 14.9 + SH
CTA_TAP = 15.35 + SH


def scratch():
    """A record scratch: a fast falling then rising squeal over noise."""
    tt = t(0.35)
    f = 900 * np.exp(-6 * tt) + 300 * np.exp(-30 * (0.35 - tt))
    return 0.25 * np.sin(2 * np.pi * np.cumsum(f) / 48000) * np.exp(-3 * tt)


m = Mix(16.8, voice_dir=SRC / 'assets/voice')
m.voice('friend-af_bella.wav', TALK, g=0.85)
m.sfx(tap() * 0.8, PRESS)
m.sfx(boing(True), TINY)
m.sfx(bell(93, 0.6, 0.06), TINY + 0.05)
m.sfx(whoosh(0.4, 0.35), OPEN)
m.sfx(pop_seq(3, 0.05, base=76), CARDS[0])
m.sfx(pofu() * 0.5, CARDS[1])
for i in range(9):
    m.sfx(tap() * 0.3, TYPE[0] + i * (TYPE[1] - TYPE[0]) / 9)
m.sfx(tap(), MEANING[0])
m.sfx(ding(0.1), MEANING[1])
m.sfx(scratch(), REALISE)
m.sfx(clang(0.25), ANGRY)
for i in range(4):
    m.sfx(pofu() * 0.35, ANGRY + 0.35 + i * 0.3)
m.sfx(tap(), EXAMPLE[0])
m.sfx(ding(0.1), EXAMPLE[1])
m.sfx(pochi(), SAVE)
m.sfx(whoosh(0.3, 0.25), SAVE + 0.3)
m.sfx(pop_seq(3, 0.05, base=76), CARDS2)
m.sfx(bell(88, 0.7, 0.08), CARDS2 + 0.35)
for at in (11.83 + SH, 12.5 + SH, 13.45 + SH):  # taps through the in-app settings
    m.sfx(tap() * 0.5, at)
m.bed(CARDS[0], END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
