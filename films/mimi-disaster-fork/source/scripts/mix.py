"""Pronunciation Disasters 10 - Fork / F*ck: sound -> hf/assets/mix.wav. Cue sheet shared with hf/index.html (cues.json).

usage: uv run --no-project --with numpy python films/mimi-disaster-fork/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
051. Pronunciation Disasters 10 - Fork or Fck/Disasters10_Fork_assets/own-voice/); the waiter (Pippa) is Kokoro English (assets/voice/).
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, clang, ding, freeze, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

R, T0, T1, WORD, F, OL, M, C, CL, CN, A, MODEL, X, E, END = 1.5, 1.75, 2.85, 4.0, 4.5, 4.8, 6.3, 7.95, 8.55, 9.85, 11.05, 11.65, 14.95, 17.25, 18.55


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
m.sfx(rewind(), 1.08, g=1.4)                       # rewind to the start
m.sfx(pop_seq(2, 0.05, base=76), 1.5)              # the hook card lands
# the slip (take 3): "Excuse me," at T0, then "can I get a f*ck?" at T1 (the 0.43 s pause in the take shortened to 0.3 s)
m.voice('learner-fuck.wav', T0, g=1.0, start=0.20, length=1.05)
m.voice('learner-fuck.wav', T1, g=1.0, start=1.55, length=1.65)
m.sfx(tap() * 0.5, WORD)                           # the censor star
m.sfx(scratch(), F, g=2.2)
m.sfx(clang(0.3), F + 0.42)                        # the tray hits the floor (soft)
m.sfx(freeze(0.45), F + 0.25)
m.voice('../voice/waiter-af_nicole.wav', OL, 0.8)
m.sfx(boing(True), M)
m.sfx(whoosh(0.3, 0.3), C)
m.voice('learner-fuck.wav', CL, start=2.25, length=0.95)   # "get a f*ck?"
m.voice('native-fork.wav', CN, start=1.10, length=0.85)     # "get a fork?"
m.sfx(pofu() * 0.5, CN - 0.35)
m.sfx(ding(), A - 0.35)
m.sfx(whoosh(0.3, 0.3), A)
m.sfx(tap() * 0.6, MODEL)
m.voice('native-fork.wav', MODEL + 0.1)
m.sfx(tap() * 0.6, MODEL + 1.5)                    # record
m.sfx(whoosh(0.3, 0.3), X - 0.15)
m.voice('native-fork.wav', X + 0.05, g=1.0)        # said right
m.sfx(pop_seq(3, 0.05, base=76), X + 1.5)          # the fork arrives
m.bed(0.0, E)
# the air freezes: the bed stops dead at the scratch and comes back with Mimi (as in the pilot)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, R - 0.45, R - 0.4, R, R + 0.3, F, F + 0.02, M, M + 0.3, END], [1, 1, 0, 0, 1, 1, 0, 0, 1, 1])
m.end_chord(E)
m.sfx(pochi(), E + 0.6)
print(m.write(SRC / 'hf/assets/mix.wav'))
