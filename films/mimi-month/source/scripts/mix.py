"""036 「Mimiに1ヶ月見張られた結果」 sound: kit SFX and the theme bed -> hf/assets/mix.wav (no voices; bubbles carry the lines).

usage: uv run --no-project --with numpy python films/mimi-month/source/scripts/mix.py
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
DAYS = (1.5, 4.2, 6.9, 9.6, 12.1)
NOTHING = 12.5
YAY = 13.75
COPY = 15.2
END = 17.6
CTA_TAP = 18.05
DUR = 18.6

m = Mix(DUR)
m.sfx(whoosh(0.45, 0.35), 0.0)                    # the binoculars zoom in
m.sfx(boing(True), 0.45)
for i in range(10):                               # the day counter races
    m.sfx(tap() * 0.25, 0.3 + 1.0 * (i / 10) ** 0.6)
m.sfx(bell(88, 0.8, 0.08), 1.3)
for i, at in enumerate(DAYS):
    m.sfx(whoosh(0.2, 0.2), at)                   # the page flips
    m.sfx(pop_seq(2 + (i == 4), 0.05, base=76 + 2 * i), at + 0.1)
m.sfx(pofu() * 0.6, 4.4)
m.sfx(boing(False), NOTHING)
m.sfx(boing(True), YAY)
m.sfx(bell(91, 0.9, 0.08), YAY + 0.05)
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
