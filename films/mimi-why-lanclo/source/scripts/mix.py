"""Why Lanclo: the side cast's English chatter (Kokoro), the theme bed kept low (lower still in the reflective middle),
soft code-made SFX -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-why-lanclo/source/scripts/mix.py
Voices only in the first 19 s, so like mimi-quitter the mix is written with one static gain to -14 LUFS and a peak limiter
(the kit's dynamic loudnorm would lift the quiet second half). Bus balance and ducking as in Mix.write.
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, lowpass, pencil, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
TRY, SHUT = 4.4, 5.7
FLASH, CHIPS, CAFE, LATTE, LOOPS = 7.0, (7.5, 7.95, 8.4), 9.4, 9.8, (11.3, 11.75, 12.2, 12.6)
OTHERS, COCO, SQUINT, VS = 13.0, 15.9, 18.8, (20.5, 20.75)
REAL, PANELS = 22.4, (22.9, 23.6, 24.3)
LECT, QUOTE, CYCLE = 27.4, 29.45, (32.35, 32.7, 33.05)
RES, AETE, PILLS = 34.6, 38.4, (39.0, 39.35)
MONT = (40.4, 42.0, 43.6, 45.2, 46.8)
CLOSE, END, CTA_TAP, DUR = 48.4, 51.0, 51.6, 52.6
CALM = (22.4, 38.4)   # the reflective middle: the bed drops further

m = Mix(DUR, voice_dir=SRC / 'assets/voice')
# The discussion: everyone over each other (Mimi has no line)
for name, at, g in [('b1.wav', 0.05, 0.85), ('p1.wav', 0.9, 0.6), ('c1.wav', 1.8, 0.55),
                    ('b2.wav', 2.8, 0.6), ('p2.wav', 3.6, 0.55), ('c2.wav', 5.0, 0.5)]:
    m.voice(name, at, g)
m.sfx(pofu() * 0.4, TRY)
m.sfx(tap() * 0.4, SHUT)
# Flashback: pencil, chips, the café line on repeat
m.sfx(whoosh(0.4, 0.25), FLASH - 0.1)
m.sfx(pencil(2.0, 0.12), FLASH + 0.3)
for at in CHIPS:
    m.sfx(pop_seq(1, 0.05, base=76), at)
m.sfx(whoosh(0.3, 0.2), CAFE - 0.1)
m.sfx(pop_seq(2, 0.05, base=79), LATTE)
for at in LOOPS:
    m.sfx(tap() * 0.5, at)
# People abroad
m.sfx(whoosh(0.35, 0.25), OTHERS - 0.1)
m.voice('b3.wav', OTHERS + 0.1, 0.9)
m.voice('c3.wav', COCO + 0.05, 0.85)
m.sfx(pofu() * 0.4, SQUINT + 0.1)
for at in VS:
    m.sfx(pop_seq(1, 0.05, base=79), at)
# The real world, the lecturer, the cycle
for at in PANELS:
    m.sfx(pop_seq(1, 0.05, base=74), at)
m.sfx(whoosh(0.35, 0.2), LECT - 0.1)
m.sfx(pofu() * 0.35, QUOTE)
for i, at in enumerate(CYCLE):
    m.sfx(pop_seq(1, 0.05, base=72 + 2 * i), at)
# On purpose, the app
m.sfx(ding(0.08), AETE + 0.05)
for at in PILLS:
    m.sfx(pop_seq(1, 0.05, base=79), at)
for at in MONT:
    m.sfx(whoosh(0.25, 0.15), at - 0.05)
m.sfx(pop_seq(3, 0.05, base=79), CLOSE + 0.05)
m.bed(0.0, END)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, CALM[0] - 0.6, CALM[0], CALM[1], CALM[1] + 0.6, DUR], [1, 1, 0.55, 0.55, 1, 1])
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)

# Mix.write's buses and ducking, then one static gain to -14 LUFS and a limiter
env = lowpass(np.abs(m.v), 0.002)
duck = lowpass(1 - 0.75 * np.clip(env / (env.max() * 0.12 + 1e-9), 0, 1), 0.0008)
mix = m.v + 0.35 * lowpass(m.s, 0.35) + 0.55 * m.m * duck
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
print(out, f'(was {lufs} LUFS)')
