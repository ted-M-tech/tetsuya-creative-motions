"""Katakana Traps 4 - Vitamin: sound -> hf/assets/mix.wav. Cue sheet: ../cues.json (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-katakana-vitamin/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
076. Katakana Traps 4 - Vitamin/KT4_Vitamin_assets/own-voice/). No side cast, no Kokoro.
Copied from episode 1 (films/mimi-katakana-mcdonalds); only the takes, their cuts and measured beats differ.
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
LEARNER, NATIVE = 'learner-katakana.wav', 'us-vitamin.wav'
LB, MB = C['LEARNER_BEATS'], C['MODEL_BEATS']
(LS, LL), (NS, NL) = C['LEARNER_CUT'], C['MODEL_CUT']   # placed segment [start, length]: cut at silence, >= 40 ms pre-roll


def blip(f=880, d=0.06, vel=0.12):
    """A soft beat-meter tick (sine, fast decay, no bell)."""
    tt = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 60) * vel


m = Mix(END, voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(2, 0.05, base=76), 0.05)               # hook card lands
# slip: the four-beat katakana word; a soft tick per beat as the meter fills
m.voice(LEARNER, SLIP + LS, g=1.0, start=LS, length=LL)
for b in LB:
    m.sfx(blip(660), SLIP + b, g=0.6)
m.sfx(boing(False), SORRY)                            # the pharmacist's blank "Sorry?"
m.sfx(tap() * 0.4, SHRINK + 0.2)                      # caption: not bi, VI
# explain: the learner take again over four equal dots, then the model twice over three dots (big first one)
m.sfx(whoosh(0.3, 0.3), EXPLAIN)
m.voice(LEARNER, EL, start=LS, length=LL)
for b in LB:
    m.sfx(blip(660), EL - 0.2 + b, g=0.5)
for at in (EM1, EM2):
    m.voice(NATIVE, at, start=NS, length=NL)
    for i, b in enumerate(MB):
        m.sfx(blip(990 if i == 0 else 740, vel=0.16 if i == 0 else 0.1), at - 0.2 + b, g=0.5)
m.sfx(pofu() * 0.5, EM1 - 0.3)
# model: the Friend says it right at the counter
m.sfx(whoosh(0.3, 0.3), MODEL - 0.15)
m.voice(NATIVE, MODEL + 0.1, start=NS, length=NL)
m.sfx(ding(), OK)
m.sfx(pop_seq(3, 0.05, base=76), OK + 0.15)
# cta: the comment question
m.sfx(whoosh(0.3, 0.3), CTA)
m.sfx(pop_seq(2, 0.06, base=79), CTA + 0.2)
m.bed(0.0, E)
# the pharmacy goes quiet on the blank "Sorry?" and comes back with the explanation
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, SORRY, SORRY + 0.05, EXPLAIN - 0.1, EXPLAIN + 0.2, END], [1, 1, 0.25, 0.25, 1, 1])
# this film has only two short words of voice, so the -14 LUFS post-gain lifts the bed more than in episode 1: bed 3 dB lower
# keeps the voice about 12 dB over it, as in episode 1
m.m *= 0.7
m.end_chord(E)
m.sfx(pochi(), C['TAP'])
out = m.write(SRC / 'hf/assets/mix.wav')
# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true peak bound): measure, add the missing gain
# in front of a -2.4 dB limiter (the cuts' AAC lands at about -1.6 dBTP), and measure again. The balance between voice, SFX and bed is unchanged.
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
                    f'volume={-14 - i + 0.1:.2f}dB,alimiter=limit=0.76:level=false:attack=1:release=60', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
