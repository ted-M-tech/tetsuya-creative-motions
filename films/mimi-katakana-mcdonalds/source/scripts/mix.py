"""Katakana Traps 1 - McDonald's: sound -> hf/assets/mix.wav. Cue sheet: ../cues.json (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-katakana-mcdonalds/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
058. Katakana Traps 1 - McDonalds/KT1_McDonalds_assets/own-voice/). No side cast, no Kokoro.
Series: episodes 2+ copy this file, swap the two takes and their measured beats in cues.json.
"""
import json
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())
SLIP, SORRY, SHRINK, EXPLAIN, EL, EM1, EM2, MODEL, OK, CTA, E, END = (
    C[k] for k in ('SLIP', 'SORRY', 'SHRINK', 'EXPLAIN', 'EL', 'EM1', 'EM2', 'MODEL', 'OK', 'CTA', 'E', 'END'))
LEARNER, NATIVE = 'learner-katakana.wav', 'us-mcdonalds.wav'
LB, MB = C['LEARNER_BEATS'], C['MODEL_BEATS']


def blip(f=880, d=0.06, vel=0.12):
    """A soft beat-meter tick (sine, fast decay, no bell)."""
    tt = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 60) * vel


m = Mix(END, voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(2, 0.05, base=76), 0.05)               # hook card lands
# slip: the six-beat katakana word; a soft tick per beat as the meter fills
m.voice(LEARNER, SLIP, g=1.0)
for b in LB:
    m.sfx(blip(660), SLIP + b, g=0.6)
m.sfx(boing(False), SORRY)                            # the clerk's blank "Sorry?"
m.sfx(tap() * 0.4, SHRINK + 0.2)                      # caption: 6 beats vs 3 syllables
# explain: the learner take again over six equal dots, then the model twice over three dots (big middle one)
m.sfx(whoosh(0.3, 0.3), EXPLAIN)
m.voice(LEARNER, EL, start=0.2)
for b in LB:
    m.sfx(blip(660), EL - 0.2 + b, g=0.5)
for at in (EM1, EM2):
    m.voice(NATIVE, at, start=0.2)
    for i, b in enumerate(MB):
        m.sfx(blip(990 if i == 1 else 740, vel=0.16 if i == 1 else 0.1), at - 0.2 + b, g=0.5)
m.sfx(pofu() * 0.5, EM1 - 0.3)
# model: the Friend says it right at the counter
m.sfx(whoosh(0.3, 0.3), MODEL - 0.15)
m.voice(NATIVE, MODEL + 0.1, start=0.2)
m.sfx(ding(), OK)
m.sfx(pop_seq(3, 0.05, base=76), OK + 0.15)
# cta: the comment question
m.sfx(whoosh(0.3, 0.3), CTA)
m.sfx(pop_seq(2, 0.06, base=79), CTA + 0.2)
m.bed(0.0, E)
# the counter goes quiet on the blank "Sorry?" and comes back with the explanation
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, SORRY, SORRY + 0.05, EXPLAIN - 0.1, EXPLAIN + 0.2, END], [1, 1, 0.25, 0.25, 1, 1])
m.end_chord(E)
m.sfx(pochi(), C['TAP'])
print(m.write(SRC / 'hf/assets/mix.wav'))
