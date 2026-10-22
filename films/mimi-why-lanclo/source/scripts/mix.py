"""Why Lanclo: the side cast's English chatter (Kokoro), the theme bed kept low (lower still in the reflective middle),
soft code-made SFX -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-why-lanclo/source/scripts/mix.py
Voices only in the first 21 s, so like mimi-quitter the mix is written with one static gain to -14 LUFS and a peak limiter
(the kit's dynamic loudnorm would lift the quiet second half). Bus balance and ducking as in Mix.write.
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, lowpass, pencil, pochi, pofu, pop_seq, tap, whoosh  # noqa: F401  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
TRY, SHUT = 4.4, 5.7
FLASH, CHIPS, INTRO = 7.0, (7.5, 7.95, 8.4), 9.4
QS = (('q1.wav', 9.5), ('q2.wav', 11.0), ('q3.wav', 12.15), ('q4.wav', 13.45))
ANSWERS, FAST, BLANK = (10.5, 11.8, 12.8), 12.92, 14.25
OTHERS, COCO, SQUINT, VS = 15.0, 17.9, 20.8, (22.5, 22.75)
REAL, PANELS = 24.4, (24.9, 25.6, 26.3)
LECT, QUOTE, CYCLE = 29.4, 31.45, (34.35, 34.7, 35.05)
RES, AETE, PILLS = 36.6, 40.4, (41.0, 41.35)
MONT = (42.4, 44.0, 45.6, 47.2, 48.8)
CLOSE, END, CTA_TAP, DUR = 50.4, 53.0, 53.6, 54.6
CALM = (24.4, 40.4)   # the reflective middle: the bed drops further

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
m.sfx(whoosh(0.3, 0.2), INTRO - 0.1)
for name, at in QS:
    m.voice(name, at, 0.85)
for at in ANSWERS:
    m.sfx(pop_seq(2, 0.05, base=79), at)
m.sfx(pop_seq(8, 0.04, base=76), FAST)
m.sfx(pofu() * 0.5, BLANK)
# People abroad
m.sfx(whoosh(0.35, 0.25), OTHERS - 0.1)
m.voice('b3.wav', OTHERS + 0.25, 0.9)
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
