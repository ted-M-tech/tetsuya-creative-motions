"""029 「3日坊主の私が、1ヶ月続いた理由」 sound: kit SFX and the theme bed -> hf/assets/mix.wav (no voices; bubbles carry the lines).

usage: uv run --no-project --with numpy python films/mimi-quitter/source/scripts/mix.py
Like mimi-watching, a voiceless film is written with one static gain to -14 LUFS (the kit's dynamic loudnorm lifts quiet parts).
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, bell, boing, ding, lowpass, mokugyo, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
STAMP3 = 0.12
SLASH = 0.62
THIRTY = 0.78
DAYS = (1.75, 2.4, 3.05, 3.7)
PHONE = 4.4
HOME = 6.0
TAP_W = 7.25
LESSON = 7.7
NIGHT = 9.4
NOTIF = 10.0
TAP_N = 10.75
CURIOUS = 10.7
STREAK = 14.0
COPY = 15.8
END = 17.9
CTA_TAP = 18.35
DUR = 19.0

m = Mix(DUR)
for i in range(3):
    m.sfx(mokugyo(0.5) * 0.5, 0.0 + i * 0.2)        # the monk's temple block
m.sfx(pofu() * 0.7, STAMP3)
m.sfx(whoosh(0.2, 0.3), SLASH)
m.sfx(boing(True), THIRTY)
m.sfx(bell(88, 0.8, 0.08), THIRTY + 0.03)
for i, at in enumerate(DAYS):
    m.sfx(tap() * 0.5, at)
m.sfx(boing(False), DAYS[3])
m.sfx(whoosh(0.35, 0.3), PHONE)
m.sfx(whoosh(0.25, 0.25), HOME)
m.sfx(tap() * 0.7, TAP_W)
m.sfx(pop_seq(3, 0.05, base=76), LESSON)
m.sfx(ding(0.12), NOTIF)
m.sfx(boing(True), CURIOUS)
m.sfx(tap() * 0.7, TAP_N)
m.sfx(pop_seq(4, 0.06, base=79), STREAK)
m.sfx(bell(91, 0.9, 0.08), STREAK + 0.2)
m.sfx(pop_seq(3, 0.05, base=76), COPY)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)

# Static loudness (same bus balance as Mix.write, no voice): one gain to -14 LUFS and a peak limiter.
mix = 0.35 * lowpass(m.s, 0.35) + 0.55 * m.m
mix /= np.abs(mix).max() / 0.9
out = SRC / 'hf/assets/mix.wav'
out.parent.mkdir(parents=True, exist_ok=True)
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
