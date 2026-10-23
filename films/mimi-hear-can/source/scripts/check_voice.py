"""Acoustic check of the can / can't takes (Praat via parselmouth): every 20 ms, energy, share of energy above 4 kHz
(the s of "swim" and the k aspiration) and F0, F1, F2 where voiced. Used to confirm "can" is reduced and short and
"can't" keeps a long, open /ae/ (see ../../PROCESS.md). Whisper is not used for this.

usage: uv run --no-project --with praat-parselmouth --with numpy python -I films/mimi-hear-can/source/scripts/check_voice.py \
         films/mimi-hear-can/source/assets/own-voice/us-can.wav films/mimi-hear-can/source/assets/own-voice/us-cant.wav
"""
import sys

import numpy as np
import parselmouth

for p in sys.argv[1:]:
    s = parselmouth.Sound(p)
    x, sr = s.values[0], int(s.sampling_frequency)
    pt = s.to_pitch_ac(time_step=0.02, pitch_floor=40, pitch_ceiling=300)
    fm = s.to_formant_burg(time_step=0.02)
    print(p.split('/')[-1], f'{s.duration:.2f} s')
    for t in np.arange(0.2, s.duration - 0.05, 0.02):
        seg = x[int(t * sr):int((t + 0.02) * sr)]
        spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        fr = np.fft.rfftfreq(len(seg), 1 / sr)
        e = 10 * np.log10(spec.sum() + 1e-12)
        if e < -10:
            continue
        f0 = pt.get_value_at_time(t + 0.01)
        voiced = f0 == f0
        f1, f2 = (fm.get_value_at_time(1, t + 0.01), fm.get_value_at_time(2, t + 0.01)) if voiced else (np.nan, np.nan)
        print(f'{t:.2f} E{e:5.1f} hf{spec[fr > 4000].sum() / (spec.sum() + 1e-12):.2f} '
              + (f'F0 {f0:3.0f} F1 {f1:4.0f} F2 {f2:4.0f}' if voiced else 'unvoiced'))
