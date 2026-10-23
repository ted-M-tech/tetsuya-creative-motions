# Praat source-filter vowel edit for the learner take (learner-sex.wav): raise F1 / lower F2 inside [a,b] s and splice it back.
# usage: uv run --no-project --with praat-parselmouth --with numpy python vowel_shift.py in.wav out.wav a b F1ratio F2ratio
import sys, numpy as np, parselmouth
from parselmouth.praat import call
src, out, a, b, r1, r2 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
s = parselmouth.Sound(src)
sr = s.sampling_frequency
s11 = call(s, "Resample", 11000, 50)
lpc = call(s11, "To LPC (burg)", 10, 0.025, 0.005, 50)
srcsig = call([s11, lpc], "Filter (inverse)")
fmt = call(s11, "To Formant (burg)", 0.005, 5, 5500, 0.025, 50)
grid = call(fmt, "Down to FormantGrid")
for k, r in ((1, r1), (2, r2)):
    call(grid, "Remove formant points between", k, a, b)
    for t in np.arange(a, b, 0.005):
        v = call(fmt, "Get value at time", k, t, "hertz", "linear")
        if v == v: call(grid, "Add formant point", k, t, v * r)
new = call([srcsig, grid], "Filter")
new = call(new, "Resample", sr, 50)
o = s.values[0].copy(); n = new.values[0][:len(o)]
# match level inside the vowel
ia, ib = int(a*sr), int(b*sr)
g = np.sqrt(np.mean(o[ia:ib]**2) / (np.mean(n[ia:ib]**2) + 1e-12))
n = n * g
w = np.zeros(len(o)); fade = int(0.015*sr)
w[ia:ib] = 1; w[ia-fade:ia] = np.linspace(0,1,fade); w[ib:ib+fade] = np.linspace(1,0,fade)
y = o*(1-w) + n*w
# keep high band (frication) from original: only the voiced region is replaced, so fine
parselmouth.Sound(y, sr).save(out, "WAV")
print("gain", g)
