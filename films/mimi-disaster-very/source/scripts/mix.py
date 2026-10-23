"""Pronunciation Disasters 14 - Very / Berry: sound -> hf/assets/mix.wav. Generated cue sheet (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-disaster-very/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
056. Pronunciation Disasters 14 - Very or Berry/Disasters14_Very_assets/own-voice/). No side cast voice.
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, ding, freeze, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

R, T0, WORD, F, OL, M, C, CL, CN, A, MODEL, REC, X, E, END = 1.5, 2.0, 2.88, 4.2, 4.5, 6.3, 7.9, 8.5, 9.6, 10.9, 11.5, 13.1, 15.1, 17.51, 18.81
# measured (see PROCESS.md): learner-berry.wav "berry" voice bar 0.835, lip release 0.91, "much" from 1.20;
# native-very.wav "very" voiced frication from 0.665, "much" from 0.88


def rewind(d=0.42):
    """A tape rewind: a fast rising chirp over hiss."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    f = np.linspace(300, 2400, n)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 38 * tt))
    hiss = np.random.default_rng(5).standard_normal(n) * 0.12
    env = np.minimum(1, tt * 30) * np.minimum(1, (d - tt) * 30)
    return (tone * 0.35 + hiss) * env


def scratch():
    """A vinyl record scratch (the pilot's): two noisy strokes whose band sweeps down then up."""
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


m = Mix(END, voice_dir=SRC / 'assets/own-voice')
m.sfx(boing(True), 0.02)                           # punchline first
m.sfx(rewind(), 1.08, g=1.4)                     # rewind to the start
m.sfx(pop_seq(2, 0.05, base=76), 1.5)             # the hook card lands
m.voice('learner-berry.wav', T0, g=1.0)          # the b of "berry" pops at 0.91 s in the take
m.sfx(tap() * 0.5, WORD)                          # the wrong consonant lights up
m.sfx(scratch(), F, g=2.2)
m.sfx(freeze(0.45), F + 0.1)
for i in range(6):                                  # strawberries thud onto the Friend
    m.sfx(pofu() * 0.35, F + 0.32 + i * 0.12)
m.sfx(boing(True), M)
m.sfx(whoosh(0.3, 0.3), C)
m.voice('learner-berry.wav', CL, start=0.80, length=0.40)   # "berry" alone
m.voice('native-very.wav', CN, start=0.64, length=0.26)     # "very" alone
m.sfx(pofu() * 0.5, CN - 0.35)
m.sfx(ding(), A - 0.35)
m.sfx(whoosh(0.3, 0.3), A)
m.sfx(tap() * 0.6, MODEL)
m.voice('native-very.wav', MODEL + 0.1, start=0.25)
m.sfx(tap() * 0.6, REC)              # record
m.sfx(whoosh(0.3, 0.3), X - 0.15)
m.voice('native-very.wav', X + 0.05, g=1.0, start=0.25)  # said right
m.sfx(pop_seq(3, 0.05, base=76), X + 0.2)
m.bed(0.0, E)
# the air freezes: the bed stops dead at the scratch and comes back with Mimi (as in the pilot)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, R - 0.45, R - 0.4, R, R + 0.3, F, F + 0.02, M, M + 0.3, END], [1, 1, 0, 0, 1, 1, 0, 0, 1, 1])
m.end_chord(E)
m.sfx(pochi(), E + 0.6)
print(m.write(SRC / 'hf/assets/mix.wav'))
