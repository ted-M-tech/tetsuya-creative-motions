"""Katakana Traps 2 - Mansion: sound -> hf/assets/mix.wav. Cue sheet: ../cues.json (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-katakana-mansion/source/scripts/mix.py
The four lines are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
059. Katakana Traps 2 - Mansion/KT2_Mansion_assets/own-voice/). No side cast, no Kokoro.
Mimi's "Wow, you're rich!" is a bubble only (no voice).
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, pochi, pofu, poof, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())
SLIP, RICH, PANIC, EXPLAIN, EM1, EM2, MODEL, Q1, Q2, CTA, DEFL, E, END = (
    C[k] for k in ('SLIP', 'RICH', 'PANIC', 'EXPLAIN', 'EM1', 'EM2', 'MODEL', 'Q1', 'Q2', 'CTA', 'DEFL', 'E', 'END'))
TRIM = C['TRIM']


def say(m, name, at):
    m.voice(name + '.wav', at, start=TRIM[name])


m = Mix(END, voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(2, 0.05, base=76), 0.05)                # hook card + the castle bubble
# slip: the Friend says it; Mimi's starry "Wow, you're rich!" (bubble only); the Friend panics
say(m, 'learner-mansion', SLIP)
m.sfx(pop_seq(3, 0.05, base=79), RICH)
m.sfx(boing(False) * 0.6, PANIC)
# explain: the meaning card, the model twice
m.sfx(whoosh(0.3, 0.3), EXPLAIN)
m.sfx(tap() * 0.4, EM1 - 0.4)
say(m, 'us-apartment', EM1)
say(m, 'us-apartment', EM2)
# model: the quick-fire card
m.sfx(whoosh(0.3, 0.3), MODEL)
for at, name in ((Q1, 'us-outlet'), (Q2, 'us-complaint')):
    m.sfx(tap() * 0.4, at - 0.15)
    say(m, name, at)
# cta: the comment question, then the castle deflates
m.sfx(whoosh(0.3, 0.3), CTA)
m.sfx(pop_seq(2, 0.06, base=79), CTA + 0.2)
m.sfx(pofu() * 0.35, DEFL)
m.sfx(boing(False) * 0.45, DEFL + 0.15)
m.sfx(poof() * 0.25, DEFL + 0.55)
m.bed(0.0, E)
# the street goes quiet on the panic and comes back with the explanation
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, PANIC, PANIC + 0.05, EXPLAIN - 0.1, EXPLAIN + 0.2, END], [1, 1, 0.3, 0.3, 1, 1])
m.end_chord(E)
m.sfx(pochi(), C['TAP'])
out = m.write(SRC / 'hf/assets/mix.wav')


# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true-peak bound): measure, add the missing gain
# in front of a -1.5 dBTP limiter, and measure again (same fix as episode 1). The voice / SFX / bed balance is unchanged.
def lufs(f):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    d = json.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))
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
