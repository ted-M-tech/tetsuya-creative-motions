"""Pronunciation Hacks 1 - Check It Out: sound -> hf/assets/mix.wav. Cue sheet: ../cues.json (same times as hf/index.html).

usage: uv run --no-project --with numpy python films/mimi-hack-check-it-out/source/scripts/mix.py
The learner / model takes are the owner's own registered Lanclo voice (assets/own-voice/, not in Git: Drive
072. Pronunciation Hacks 1 - Check It Out/Hacks1_CheckItOut_assets/own-voice/). No side cast, no Kokoro.
Series: episodes 2+ copy this file and cues.json, swap the takes (TAKES: start/length cut at measured silence) and word times.
"""
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, pencil, pochi, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())
T = C['TAKES']
LEARNER, CHECK, PICK = 'learner-robot.wav', 'us-check-it-out.wav', 'us-pick-it-up.wav'
VOICE_DIR = SRC / 'assets/own-voice'


def blip(f=880, d=0.06, vel=0.12):
    """A soft word tick (sine, fast decay, no bell)."""
    tt = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * f * tt) * np.exp(-tt * 60) * vel


def say(m, name, at, g=1.0):
    """Place a take cut at its measured silences; check the first/last 10 ms are quiet (no chopped word)."""
    start, length = T[name]
    with wave.open(str(VOICE_DIR / name)) as f:  # the raw take (load() fades its edges, which would hide a chop)
        sr = f.getframerate()
        f.setpos(int(start * sr))
        x = np.frombuffer(f.readframes(int(length * sr)), np.int16).astype(float)
    w = int(0.01 * sr)
    peak = np.abs(x).max()
    for edge, seg in (('head', x[:w]), ('tail', x[-w:])):
        db = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) / peak + 1e-12)
        assert db <= -38, f'{name} {edge} at {db:.1f} dB vs peak: cut is inside a word'
        print(f'{name} @ {at:.2f} {edge} {db:.1f} dB vs peak')
    m.voice(name, at, g=g, start=start, length=length)


m = Mix(C['END'], voice_dir=VOICE_DIR)
# hook: the card lands with the smooth model "Check it out!" (= チェケラ)
m.sfx(pop_seq(2, 0.05, base=76), 0.02)
say(m, CHECK, C['HOOK_V'])
# slip: the Friend reads word by word, a stiff tick on each word; the pauses are real silence in the take
m.sfx(whoosh(0.3, 0.25), C['SLIP'] - 0.1)
say(m, LEARNER, C['LV'])
for w in C['LEARNER_WORDS']:
    m.sfx(blip(520, vel=0.1), C['LV'] + w, g=0.6)
m.sfx(tap() * 0.4, C['ROBOT'])
# tip: the link arcs are drawn (pencil), then the model; the second phrase the same way
m.sfx(whoosh(0.3, 0.3), C['TIP'])
for a in ('ARC1', 'ARC2', 'ARC3', 'ARC4'):
    m.sfx(pencil(0.22, 0.12), C[a])
say(m, CHECK, C['M1'])
m.sfx(whoosh(0.25, 0.2), C['MODEL'])
say(m, PICK, C['M2'])
# fix: the Friend says it smoothly (the model take again), high five
m.sfx(whoosh(0.3, 0.3), C['FIX'] - 0.1)
say(m, CHECK, C['FV'])
m.sfx(ding(), C['HIGH'])
m.sfx(pop_seq(3, 0.05, base=76), C['HIGH'] + 0.15)
# cta: the next tip
m.sfx(whoosh(0.3, 0.3), C['CTA'])
m.sfx(pop_seq(2, 0.06, base=79), C['CTA'] + 0.2)
m.bed(0.0, C['E'])
# the bed dips under the robot reading so the pauses are heard as gaps
tt = np.arange(m.n) / SR
LV, LE = C['LV'], C['LV'] + T[LEARNER][1]
m.m *= np.interp(tt, [0, LV - 0.1, LV + 0.1, LE, LE + 0.3, C['END']], [1, 1, 0.35, 0.35, 1, 1])
m.end_chord(C['E'])
m.sfx(pochi(), C['TAP'])
out = m.write(SRC / 'hf/assets/mix.wav')


# loudnorm's single pass stops short of -14 on a short, voice-sparse film: measure, add the missing gain in front of a
# -2.4 dB limiter (overshooting the step, as the limiter eats part of it; the cuts' AAC lands at about -1.6 dBTP), and measure again. The balance between voice, SFX and bed is unchanged.
def lufs(f):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    d = json.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))
    return float(d['input_i']), float(d['input_tp'])


for _ in range(6):  # the limiter eats part of each step; a few passes converge
    i, tp = lufs(out)
    print("pass", i, tp)
    if abs(i + 14) < 0.3:
        break
    tmp = out.with_suffix('.tmp.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(out), '-af',
                    f'volume={(-14 - i) * 1.8 + 0.1:.2f}dB,alimiter=limit=0.76:level=false:attack=1:release=60', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
