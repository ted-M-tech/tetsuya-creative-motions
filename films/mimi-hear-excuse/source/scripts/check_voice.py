"""Acoustic check of the three "Excuse me" intonations (Praat via parselmouth): every 20 ms, intensity (dB) and F0 (Hz)
where voiced, then the voiced run boundaries (silences / the unvoiced k and s split ex | cuse | me) with each run's mean F0,
F0 at its start and end, and peak intensity. Used to confirm A falls, B rises and C jumps sharply with the stress on "me"
(see ../../PROCESS.md). Whisper is not used for this.

usage: uv run --no-project --with praat-parselmouth --with numpy python -I films/mimi-hear-excuse/source/scripts/check_voice.py \
         films/mimi-hear-excuse/source/assets/own-voice/us-*.wav
"""
import sys

import numpy as np
import parselmouth

for p in sys.argv[1:]:
    s = parselmouth.Sound(p)
    pt = s.to_pitch_ac(time_step=0.02, pitch_floor=50, pitch_ceiling=500)
    it = s.to_intensity(time_step=0.02)
    print(f'== {p.split("/")[-1]} {s.duration:.2f} s')
    rows, runs, cur = [], [], []
    for t in np.arange(0.0, s.duration, 0.02):
        db = it.get_value(t)
        f0 = pt.get_value_at_time(t)
        if db != db or db < 45:
            if cur:
                runs.append(cur); cur = []
            continue
        rows.append(f'{t:.2f} {db:4.0f}dB ' + (f'F0 {f0:4.0f}' if f0 == f0 else '  -'))
        if f0 == f0:
            cur.append((t, f0, db))
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    print('\n'.join(rows))
    for r in runs:
        if len(r) < 2:
            continue
        a = np.array(r)
        print(f'  voiced {a[0,0]:.2f}-{a[-1,0]:.2f}s  F0 start {a[0,1]:.0f} end {a[-1,1]:.0f} mean {a[:,1].mean():.0f} max {a[:,1].max():.0f}  peak {a[:,2].max():.0f} dB')
