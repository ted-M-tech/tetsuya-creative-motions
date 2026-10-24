"""Acoustic check of the ship / sheep takes (Praat via parselmouth). Every 10 ms: energy, spectral centroid (the sh is a
broad 2-6 kHz hiss), voicing (Praat cross-correlation pitch, 60-300 Hz) and F1 / F2 (Burg, 5 formants up to 5 kHz).
Then the vowel after the last sh: the voiced frames between the end of the sh and the p closure (energy drop), with its
duration and median F1 / F2. ship /ɪ/ should be short with a higher F1 and lower F2; sheep /iː/ longer, F1 low, F2 high
(spread lips, tongue high and front). Whisper is not used for this.

usage: uv run --no-project --with praat-parselmouth --with numpy python -I films/mimi-hear-ship/source/scripts/check_voice.py \
         films/mimi-hear-ship/source/assets/own-voice/us-ship.wav films/mimi-hear-ship/source/assets/own-voice/us-sheep.wav
"""
import sys

import numpy as np
import parselmouth

for p in sys.argv[1:]:
    s = parselmouth.Sound(p)
    x, sr = s.values[0], int(s.sampling_frequency)
    pt = s.to_pitch_cc(time_step=0.01, pitch_floor=60, pitch_ceiling=300)
    fm = s.to_formant_burg(time_step=0.01, max_number_of_formants=5, maximum_formant=5000)
    rows = []
    for t in np.arange(0.0, s.duration - 0.02, 0.01):
        seg = x[int(t * sr):int((t + 0.02) * sr)]
        spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
        fr = np.fft.rfftfreq(len(seg), 1 / sr)
        e = 10 * np.log10(spec.sum() + 1e-12)
        cen = (spec * fr).sum() / (spec.sum() + 1e-12)
        f0 = pt.get_value_at_time(t + 0.01)
        rows.append((t, e, cen, f0, fm.get_value_at_time(1, t + 0.01), fm.get_value_at_time(2, t + 0.01)))
    peak = max(r[1] for r in rows)
    print(p.split('/')[-1], f'{s.duration:.2f} s')
    for t, e, cen, f0, f1, f2 in rows:
        if e > peak - 35:
            print(f'{t:.2f} E{e - peak:6.1f} cen{cen:5.0f} ' + (f'F0 {f0:3.0f} F1 {f1:4.0f} F2 {f2:4.0f}' if f0 == f0 else '-'))
    # the last fricative run (centroid > 2500 Hz, loud) is the sh of ship / sheep; the vowel is every frame after it,
    # below 2500 Hz, until the energy falls 20 dB under the peak for good (the p closure). The final vowel is often
    # creaky (F0 ~70 Hz, Praat calls it unvoiced), so the vowel is found by energy and spectrum, not by the pitch track.
    fric = [i for i, r in enumerate(rows) if r[2] > 2500 and r[1] > peak - 25]
    j = fric[-1] + 1
    while rows[j][2] > 2500 or rows[j][1] < peak - 20:
        j += 1
    k = j
    while k + 2 < len(rows) and not all(rows[k + n][1] < peak - 20 for n in range(3)):
        k += 1
    vow = rows[j:k]
    mid = vow[len(vow) // 5: len(vow) - len(vow) // 5] or vow
    f1 = np.nanmedian([r[4] for r in mid]); f2 = np.nanmedian([r[5] for r in mid])
    print(f'  vowel after sh: {vow[0][0]:.2f}-{vow[-1][0] + 0.01:.2f} s = {len(vow) * 10} ms (sh ends {rows[fric[-1]][0] + 0.01:.2f}), '
          f'middle 60 %: median F1 {f1:.0f} Hz, F2 {f2:.0f} Hz, F2-F1 {f2 - f1:.0f} Hz')
