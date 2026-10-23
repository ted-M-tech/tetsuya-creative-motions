"""Pronunciation Disasters 15 - Year / Ear: sound -> hf/assets/mix.wav. Generated cue sheet (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-disaster-year/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
057. Pronunciation Disasters 15 - Year or Ear/Disasters15_Year_assets/own-voice/). No side cast, no Kokoro.
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, ding, freeze, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

R, T0, WORD, F, OL, M, C, CL, CN, A, MODEL, REC, X, E, END = 1.5, 2.0, 3.38, 4.2, 4.5, 6.3, 7.9, 8.5, 9.6, 10.9, 11.5, 13.1, 15.1, 17.51, 18.81


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
m.voice('learner-ear.wav', T0, g=1.0)             # "Ear" lands at 1.38 s in the take (after a glottal break, no /j/)
m.sfx(tap() * 0.5, WORD)                          # the wrong vowel lights up
m.sfx(scratch(), F, g=2.2)
m.sfx(freeze(0.45), F + 0.1)
m.sfx(pofu() * 0.5, F + 0.25)                      # Mimi solemnly holds out the earmuffs
m.sfx(boing(True), M)
m.sfx(whoosh(0.3, 0.3), C)
m.voice('learner-ear.wav', CL, start=1.33, length=0.70)   # "Ear"
m.voice('native-year.wav', CN, start=0.70, length=0.42)   # "Year": the glide starts at 0.74 s (F2 up to ~2670 Hz)
m.sfx(pofu() * 0.5, CN - 0.35)
m.sfx(ding(), A - 0.35)
m.sfx(whoosh(0.3, 0.3), A)
m.sfx(tap() * 0.6, MODEL)
m.voice('native-year.wav', MODEL + 0.1)
m.sfx(tap() * 0.6, REC)              # record
m.sfx(whoosh(0.3, 0.3), X - 0.15)
m.voice('native-year.wav', X + 0.05, g=1.0)  # said right
m.sfx(pop_seq(3, 0.05, base=76), X + 0.2)
m.bed(0.0, E)
# the air freezes: the bed stops dead at the scratch and comes back with Mimi (as in the pilot)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, R - 0.45, R - 0.4, R, R + 0.3, F, F + 0.02, M, M + 0.3, END], [1, 1, 0, 0, 1, 1, 0, 0, 1, 1])
m.end_chord(E)
m.sfx(pochi(), E + 0.6)
out = m.write(SRC / 'hf/assets/mix.wav')
# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true peak bound): measure, add the missing gain
# in front of a -1.5 dBTP limiter, and measure again. The balance between voice, SFX and bed is unchanged.
import json as _j, re, shutil, subprocess  # noqa: E402


def lufs(f):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    d = _j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))
    return float(d['input_i']), float(d['input_tp'])


for _ in range(3):
    i, tp = lufs(out)
    if abs(i + 14) < 0.3:
        break
    tmp = out.with_suffix('.tmp.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(out), '-af',
                    f'volume={-14 - i + 0.1:.2f}dB,alimiter=limit=0.84:level=false:attack=1:release=60', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
