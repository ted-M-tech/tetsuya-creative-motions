"""Pronunciation Disasters 9 - Lunch / Launch: sound -> hf/assets/mix.wav. Cue sheet = cues.json (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-disaster-lunch/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
050. Pronunciation Disasters 9 - Lunch or Launch/Disasters9_Lunch_assets/own-voice/); Coco is Kokoro English (assets/voice/).
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

R, T0, F, OL, LIFT, M, C, CL, CN, A, MODEL, REC, X, E, END = 1.5, 1.75, 4.25, 4.5, 6.7, 7.45, 9.15, 9.75, 11.0, 12.3, 12.9, 14.5, 16.5, 18.9, 20.2


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


def rumble(d, vel=0.22):
    """A soft, low rocket rumble: lowpassed noise that swells, then a rising roar for the liftoff."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    x = np.random.default_rng(11).standard_normal(n)
    for k in (60, 30):
        x = np.convolve(x, np.ones(k) / k, mode='same')
    x /= np.abs(x).max() + 1e-9
    env = np.minimum(1, tt / (0.6 * d)) * np.minimum(1, (d - tt) * 4)
    return x * env * vel


m = Mix(END, voice_dir=SRC / 'assets/own-voice')
m.sfx(boing(True), 0.02)                           # punchline first
m.sfx(rewind(), 1.08, g=1.4)                       # rewind to the start
m.sfx(pop_seq(2, 0.05, base=76), 1.5)              # the hook card lands
m.voice('learner-launch.wav', T0, g=1.0)           # "Shall we have launch?" (the word starts 1.54 s in)
m.sfx(scratch(), F, g=2.2)
m.sfx(pop_seq(1, 0.05, base=72), F + 0.12)         # the space helmet goes on
m.voice('../voice/coco-af_bella.wav', OL, 0.8)      # "Launch? Roger! Three, two, one... liftoff!"
m.sfx(rumble(1.6), LIFT - 0.8)                      # the rocket warms up
m.sfx(whoosh(0.7, 0.3), LIFT)                       # liftoff
m.sfx(boing(True), M)
m.sfx(whoosh(0.3, 0.3), C)
m.voice('learner-launch.wav', CL, start=1.50, length=0.82)
m.voice('native-lunch.wav', CN, start=0.65, length=0.50)
m.sfx(pofu() * 0.5, CN - 0.35)
m.sfx(ding(), A - 0.35)
m.sfx(whoosh(0.3, 0.3), A)
m.sfx(tap() * 0.6, MODEL)
m.voice('native-lunch.wav', MODEL + 0.1)
m.sfx(tap() * 0.6, REC)              # record
m.sfx(whoosh(0.3, 0.3), X - 0.15)
m.voice('native-lunch.wav', X + 0.05, g=1.0)  # said right
m.sfx(pop_seq(3, 0.05, base=76), X + 0.2)
m.bed(0.0, E)
# the air freezes: the bed stops dead at the scratch and comes back with Mimi (as in the pilot)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, R - 0.45, R - 0.4, R, R + 0.3, F, F + 0.02, M, M + 0.3, END], [1, 1, 0, 0, 1, 1, 0, 0, 1, 1])
m.end_chord(E)
m.sfx(pochi(), E + 0.6)
print(m.write(SRC / 'hf/assets/mix.wav'))
