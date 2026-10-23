"""Speech span of each own-voice clip: first/last 10 ms frame within 38 dB of the clip peak, plus head/tail levels.

usage: uv run --no-project --with numpy python films/mimi-cloning/source/scripts/spans.py
"""
import wave
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent.parent / 'assets/own-voice'
for f in sorted(D.glob('*.wav')):
    with wave.open(str(f)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(1)
    n = sr // 100
    rms = np.sqrt(np.mean(x[:len(x) // n * n].reshape(-1, n) ** 2, 1)) + 1e-9
    db = 20 * np.log10(rms / rms.max())
    on = np.where(db > -38)[0]
    head, tail = db[:2].max(), db[-2:].max()
    print(f'{f.stem:8s} dur {len(x)/sr:.2f}  speech {on[0]/100:.2f}-{(on[-1]+1)/100:.2f}  head {head:.0f} dB tail {tail:.0f} dB')
