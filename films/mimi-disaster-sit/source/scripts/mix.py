"""Pronunciation Disasters 1 - Sit / Sh*t: sound -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-disaster-sit/source/scripts/mix.py
Voices: the owner's registered Lanclo voice (assets/own-voice/, not in Git; rebuild with scripts/ownvoice.py + own-voice.json):
  learner-shit-2.wav  "Please sh*t down." (the Japanese friend, before)   native-sit.wav  "Please sit down." (the model)
The record scratch is made here; everything else is the kit's SFX and the theme bed (silent while the air is frozen).
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, ding, freeze, lowpass, pochi, pofu, pop_seq, shatter, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
# v3: a 1.5 s flash-forward hook (Mimi's punchline over the frozen guest), then rewind; the story keeps its v2 cue times
# through T(): +1.5 s, and everything from the card on 0.8 s earlier (Mimi's beat is shorter: the hook already showed it).
OFF = 1.5


def T(t):
    return round(t + OFF if t < 6.3 else t - 0.8 + OFF, 3)


FF_REWIND = 1.2        # flash-forward ends: rewind to the lobby
DUR = 18.7
LINE = T(0.25)  # "Please sh*t down." (speech 0.55-2.66, "sh*t" at 1.53)
SCRATCH = T(2.75)  # record scratch, the music stops, the guest freezes
MIMI = T(4.25)  # Mimi pops up, horrified
CARD = T(6.3)  # the sit / sh*t card
LEARNER2 = T(6.55)  # the friend's take again (right column)
NATIVE = T(9.15)  # the model (left column)
APP = T(11.0)  # the real app
MODEL_TAP = T(11.6)  # お手本 in the app: the model in your own voice
REC_TAP = T(13.0)  # record
SIT = T(15.1)  # back in the lobby: "Please sit down." and the guest sits
END = T(16.7)
CTA_TAP = T(17.3)


def scratch():
    """A vinyl record scratch: two noisy strokes whose band sweeps down then up."""
    out = []
    for d, f0, f1 in ((0.16, 3000, 700), (0.2, 600, 2600)):
        n = int(d * SR)
        tt = np.arange(n) / SR
        f = np.linspace(f0, f1, n)
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5
        noise = np.random.default_rng(7).standard_normal(n) * 0.35
        env = np.sin(np.pi * tt / d) ** 0.7
        out.append((tone + noise * tone) * env)
    gap = np.zeros(int(0.03 * SR))
    return np.concatenate([out[0], gap, out[1]]) * 0.8


m = Mix(DUR, voice_dir=SRC / 'assets/own-voice')
# flash-forward hook (0-1.5): Mimi's punchline over the frozen guest, then a rewind
m.sfx(freeze(0.4), 0.0)
m.sfx(boing(True), 0.05)
m.sfx(pop_seq(2, 0.05, base=76), 0.1)               # the hook line lands
m.sfx(whoosh(0.3, 0.35)[::-1], FF_REWIND)          # rewind
m.sfx(pop_seq(2, 0.05, base=72), OFF + 0.05)        # the setup card
m.voice('learner-shit-2.wav', LINE, g=1.0)
m.sfx(tap() * 0.5, LINE + 1.28)                   # the censor star
m.sfx(scratch(), SCRATCH, g=2.2)
m.sfx(freeze(0.45), SCRATCH + 0.25)
m.sfx(boing(True), MIMI)
m.sfx(whoosh(0.3, 0.3), CARD)
m.sfx(pop_seq(2, 0.06, base=72), CARD + 0.1)
m.voice('learner-shit-2.wav', LEARNER2, g=1.0)
m.sfx(tap() * 0.4, LEARNER2 + 2.5)                # the cross
m.voice('native-sit.wav', NATIVE, g=1.0)
m.sfx(ding(), NATIVE + 1.4)                       # the tick
m.sfx(whoosh(0.35, 0.3), APP - 0.1)
m.sfx(tap() * 0.6, MODEL_TAP)
m.voice('native-sit.wav', MODEL_TAP + 0.1, g=0.95)
m.sfx(tap() * 0.6, REC_TAP)
m.sfx(whoosh(0.3, 0.3), SIT - 0.15)
m.voice('native-sit.wav', SIT + 0.05, g=1.0)
m.sfx(shatter(0.35), SIT + 0.02)                  # the ice is gone
m.sfx(pofu() * 0.6, SIT + 1.3)                    # he sits
m.bed(OFF, END)
# the air freezes: the bed stops dead at the scratch and comes back with Mimi
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, SCRATCH, SCRATCH + 0.02, MIMI, MIMI + 0.3, DUR], [1, 1, 0, 0, 1, 1])
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
