"""Mimi is always watching: a soft horror drone and hiss for the dark scenes, kit SFX, the theme bed once the lights come on -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-watching/source/scripts/mix.py
No voices: every line is a speech bubble or caption. The owner dislikes loud SFX, so the "horror" is a low, quiet drone with a little hiss.
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, lowpass, pochi, pofu, pop_seq, t, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = 0.0             # dark room, Mimi's eyes, whispered caption
EYES = 0.9
NOTIFY = 2.3           # the reminder banner drops in
OPEN = 3.7             # she taps it
APP = 3.9              # Mimi's advice
CAPS = (3.95, 5.9, 7.1, 8.5)
SHOCK = 10.3           # "...how does she know?"
LIGHTS = 11.4          # lights on, cheerful Mimi
COPY = 13.3
SKIP = 14.9            # "...so the days I skip, too?"
SMILE = 15.6
DARK = 16.1            # lights go dark again
END = 17.0
CTA_TAP = 17.6
DUR = 18.4

_rng = np.random.default_rng(24)


def drone(d, vel=0.22):
    """A low, slowly beating drone with a breath of filtered hiss: eerie, never loud."""
    tt = t(d)
    env = np.minimum(1, tt / 0.5) * np.minimum(1, (d - tt) / 0.6)
    tone = sum(a * np.sin(2 * np.pi * f * tt) for f, a in ((110, 1.0), (110.7, 0.8), (164.8, 0.45), (233.1, 0.18)))
    tone *= 1 + 0.25 * np.sin(2 * np.pi * 0.35 * tt)
    hiss = lowpass(_rng.standard_normal(len(tt)), 0.08) - lowpass(_rng.standard_normal(len(tt)), 0.01)
    return vel * env * (tone / 2.4 + 0.5 * hiss)


m = Mix(DUR)
m.sfx(drone(SHOCK + 1.2, 0.012), HOOK)          # a faint room tone under every dark scene
m.sfx(drone(2.5, 0.015), HOOK)
m.sfx(whoosh(0.5, 0.012), EYES - 0.2)
m.sfx(ding(0.025), NOTIFY)
m.sfx(tap() * 0.5, OPEN)
m.sfx(whoosh(0.3, 0.2), APP)
for at in CAPS:
    m.sfx(tap() * 0.25, at)
m.sfx(drone(1.3, 0.02), SHOCK - 0.1)
m.sfx(pochi(0.35), LIGHTS - 0.05)       # the light switch
m.sfx(pop_seq(3, 0.05, base=79), LIGHTS + 0.1)
m.sfx(whoosh(0.3, 0.25), COPY - 0.1)
m.sfx(pop_seq(2, 0.06, base=76), COPY + 0.05)
m.sfx(pofu() * 0.4, SKIP)
m.sfx(pochi(0.3), DARK)                 # lights off
m.sfx(drone(1.0, 0.02), DARK)
m.bed(LIGHTS, END)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, DARK, DARK + 0.3, END - 0.1, END + 0.1], [1, 1, 0.15, 0.15, 1])   # the bed sinks while it's dark
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
# Static loudness: the kit's Mix.write ends with a one-pass (dynamic) loudnorm, which lifted the quiet dark opening by ~15 dB
# (there is no voice to anchor it). Same bus balance as Mix.write, then one gain for the whole film to -14 LUFS and a peak limiter.
mix = 0.35 * lowpass(m.s, 0.35) + 0.55 * m.m
mix /= np.abs(mix).max() / 0.9
out = SRC / 'hf/assets/mix.wav'
raw = out.with_suffix('.pre.wav')
with wave.open(str(raw), 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(raw), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
lufs = float(meas[meas.rindex('I:'):].split()[1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', f'volume={-14.0 - lufs:.2f}dB,alimiter=limit=0.84:level=false', '-ar', str(SR), str(out)], check=True)
raw.unlink()
print(out)
