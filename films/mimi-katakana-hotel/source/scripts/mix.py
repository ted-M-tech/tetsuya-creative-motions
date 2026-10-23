"""Katakana Traps 3 - Hotel, Guitar, Shampoo: sound -> hf/assets/mix.wav. Cue sheet: ../cues.json (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-katakana-hotel/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
060. Katakana Traps 3 - Hotel Guitar Shampoo/KT3_Hotel_assets/own-voice/). No side cast, no Kokoro.
The learner take holds the three katakana words; each is cut out (LEARNER_CLIPS) and placed with its chip, so the
pauses between them are gone. Loudness: Mix.write (-14 LUFS), then a gain into a soft limiter so the short film
lands on -14 integrated (the single-pass filter undershoots on a 16 s, voice-sparse film).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())
END = C['END']


def blip(f=880, d=0.06, vel=0.12):
    """A soft beat tick (sine, fast decay, no bell)."""
    tt = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 60) * vel


m = Mix(END, voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(3, 0.15, base=76), 0.12)               # hook: the three word chips pop in
# slip: the Friend's three katakana words, head-high (one clip each); a tick per syllable, the first one stronger
for at, (a, b), beats in zip(C['L_AT'], C['LEARNER_CLIPS'], C['LEARNER_BEATS']):
    m.voice('learner-katakana.wav', at, g=1.0, start=a, length=b - a)
    for i, t in enumerate(beats):
        m.sfx(blip(880 if i == 0 else 620, vel=0.15 if i == 0 else 0.08), at + t, g=0.5)
m.sfx(pofu() * 0.5, C['TILT'])                        # Mimi tilts her head
m.sfx(tap() * 0.4, C['SHRINK'])                       # caption
# explain: Mimi taps the beat, the model takes, big dot on syllable 2
m.sfx(whoosh(0.3, 0.3), C['EXPLAIN'])
for at, take, st, beats in zip(C['E_AT'], C['MODEL_TAKES'], C['MODEL_START'], C['MODEL_BEATS']):
    m.voice(take, at, start=st)
    for i, t in enumerate(beats):
        m.sfx(blip(990 if i == 1 else 700, vel=0.16 if i == 1 else 0.08), at + t, g=0.5)
m.sfx(pop_seq(2, 0.06, base=79), C['TIP'])
# model: back in the lobby, the Friend says all three right
m.sfx(whoosh(0.3, 0.3), C['MODEL'] - 0.1)
for at, take, st in zip(C['F_AT'], C['MODEL_TAKES'], C['MODEL_START']):
    m.voice(take, at, start=st)
m.sfx(ding(), C['F_AT'][2] + 0.55)
# challenge: "Japanese は？" for a second, a soft clock tick
m.sfx(whoosh(0.3, 0.3), C['CHALLENGE'])
for i in range(4):
    m.sfx(blip(520, vel=0.1), C['CHALLENGE'] + 0.15 + 0.22 * i, g=0.6)
# reveal: ja-pa-NESE, twice
m.sfx(pofu() * 0.6, C['REVEAL'])
for at in C['J_AT']:
    m.voice('us-japanese.wav', at, start=C['JAPANESE_START'])
    for i, t in enumerate(C['JAPANESE_BEATS']):
        m.sfx(blip(990 if i == 2 else 700, vel=0.16 if i == 2 else 0.08), at + t, g=0.5)
# cta
m.sfx(whoosh(0.3, 0.3), C['CTA'])
m.sfx(pop_seq(2, 0.06, base=79), C['CTA'] + 0.2)
m.bed(0.0, C['E'])
m.end_chord(C['E'])
m.sfx(pochi(), C['TAP'])
out = m.write(SRC / 'hf/assets/mix.wav')


def measure(p):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(p), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
                        '-f', 'null', '-'], capture_output=True, text=True)
    return json.loads(re.search(r'\{\s*"input_i".*?\}', r.stderr, re.S).group(0))


# Mix.write's single-pass loudnorm stops short of -14 on this short, voice-sparse film (true peak bound);
# lift the remainder with a plain gain into a soft limiter at -1.9 dBFS (true peak stays under -1 dBTP) (two rounds).
tmp = out.with_suffix('.tmp.wav')
for _ in range(2):
    gain = -14 - float(measure(out)['input_i'])
    if abs(gain) < 0.2:
        break
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(out), '-af',
                    f'volume={gain:.2f}dB,alimiter=limit=0.8:attack=2:release=60:level=false', '-ar', str(SR), str(tmp)], check=True)
    tmp.replace(out)
f = measure(out)
print(out, 'integrated', f['input_i'], 'LUFS, true peak', f['input_tp'], 'dBTP')
