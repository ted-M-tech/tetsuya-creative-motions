"""Pronunciation Disasters 13 - Thirteen / Thirty: sound -> hf/assets/mix.wav. Generated cue sheet (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-disaster-thirteen/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
055. Pronunciation Disasters 13 - Thirteen or Thirty/Disasters13_Thirteen_assets/own-voice/). No side cast: Mimi plays the
clerk (bubbles only, no voice).
"""
import json
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, ding, freeze, lowpass, pochi, pofu, poof, pop_seq, tap, whoosh  # noqa: E402

c = json.load(open(SRC / 'cues.json'))
R, T0, WORD, F, OL, AV, M, C, CL, CN, A, MODEL, REC, X, E, END = (c[k] for k in
    ('R', 'T0', 'WORD', 'F', 'OL', 'AV', 'M', 'C', 'CL', 'CN', 'A', 'MODEL', 'REC', 'X', 'E', 'END'))
LRN = 0.26  # learner-thirteen.wav: "Thir" vowel at 0.36 s, "tin" at 0.86 s -> WORD / WORD2 on the film clock
NAT = 0.15  # native-thirteen.wav: the line starts at about 0.22 s ("th")


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


def rustle(d=0.6, seed=3):
    """Paper tickets pouring down: soft filtered noise in many small flutters, settling."""
    n = int(d * SR)
    tt = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    noise = lowpass(rng.standard_normal(n), 0.25) * 0.5
    flutter = np.zeros(n)
    for at in rng.uniform(0, d * 0.85, 26):
        i = int(at * SR)
        k = min(n - i, int(0.04 * SR))
        flutter[i:i + k] += np.hanning(2 * k)[k:] * rng.uniform(0.4, 1)
    env = np.minimum(1, tt * 12) * np.exp(-tt * 2.2)
    return noise * lowpass(flutter, 0.02) * env * 4


m = Mix(END, voice_dir=SRC / 'assets/own-voice')
m.sfx(rustle(1.1), 0.0, g=0.5)                   # punchline first: the avalanche
m.sfx(boing(True), 0.05)
m.sfx(rewind(), R - 0.42, g=1.4)                 # rewind to the start
m.sfx(pop_seq(2, 0.05, base=76), R)              # the hook card lands
m.voice('learner-thirteen.wav', T0, g=1.0, start=LRN)   # flat "Thirtin" (a deliberate mispronunciation of "thirteen")
m.sfx(tap() * 0.4, WORD)
m.sfx(tap() * 0.4, WORD + 0.5)                   # two equal beats: no stress
m.sfx(scratch(), F, g=2.2)
m.sfx(freeze(0.45), F + 0.1)
m.sfx(pop_seq(4, 0.04, base=72), OL)             # Mimi the clerk: "Thirty tickets!"
m.sfx(rustle(0.8, 5), AV - 0.1, g=0.6)           # the avalanche
m.sfx(poof() * 0.6, AV + 0.2)                     # thud: buried
m.sfx(boing(True), M)
m.sfx(whoosh(0.3, 0.3), C)
m.voice('learner-thirteen.wav', CL, start=0.27, length=1.03)   # the card: "Thirtin" (flat); speech 0.305-1.26 s, edges <= -46 dB
m.voice('native-thirteen-word.wav', CN, start=0.31, length=1.01)  # the card: the isolated word "Thirteen." (stress on TEEN); speech 0.35-1.29 s, 40 ms pre-roll, cut after the n decays
m.sfx(pofu() * 0.5, CN - 0.35)
m.sfx(ding(), A - 0.35)
m.sfx(whoosh(0.3, 0.3), A)
m.sfx(tap() * 0.6, MODEL)
m.voice('native-thirteen.wav', MODEL + 0.1, start=NAT)
m.sfx(tap() * 0.6, REC)              # record
m.sfx(whoosh(0.3, 0.3), X - 0.15)
m.voice('native-thirteen.wav', X + 0.05, g=1.0, start=NAT)  # said right
m.sfx(pop_seq(3, 0.05, base=76), X + 1.0)
m.bed(0.0, E)
# the air freezes: the bed stops dead at the scratch and comes back with Mimi (as in the pilot)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, R - 0.45, R - 0.4, R, R + 0.3, F, F + 0.02, M, M + 0.3, END], [1, 1, 0, 0, 1, 1, 0, 0, 1, 1])
m.end_chord(E)
m.sfx(pochi(), E + 0.6)
print(m.write(SRC / 'hf/assets/mix.wav'))
