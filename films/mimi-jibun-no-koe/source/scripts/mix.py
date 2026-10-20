"""Sound for 「自分の声、むり」: the two LP voice clips, code-made SFX and a light 100 BPM bed, ducked under the voices.

usage: uv run --no-project --with numpy python scripts/mix.py   -> hf-short/assets/mix.wav (48 kHz stereo, -14 LUFS)
"""
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR, DUR = 48000, 15.0
N = int(SR * DUR)
rng = np.random.default_rng(7)

# Cue times (s); they follow the shot timeline in shots.py / hf-short/index.html.
OWN_TAIL = (0.0, 1.0, 1.76)     # start, length, offset into own.mp3: "...if you're available"
REWIND = 1.0
TAP_REC = 1.73                  # reach shot frame 26
OWN_FULL = 2.0
POFU = 4.62
TAP_MODEL = 5.47                # hide-reach frame 22
MODEL = 5.7
PERK = 6.4
JUMP = (7.5, 8.03)              # launch, land
PUMP = 8.2
SHADOW = 9.6                    # she speaks along with the model (practice shot frame 12)
RESULT = 11.4                   # radar card pops; score lands at 12.15
END = 14.0
BED = (1.3, 14.0)


def t(d):
    return np.arange(int(d * SR)) / SR


def load(name, start=0.0, length=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(ROOT / 'assets/voice' / name)]
    cmd += (['-t', str(length)] if length else []) + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)
    f = int(0.02 * SR)
    x[:f] *= np.linspace(0, 1, f)
    x[-f:] *= np.linspace(1, 0, f)
    return x


def place(bus, x, at, g=1.0):
    i = int(at * SR)
    x = x[:max(0, N - i)]
    bus[i:i + len(x)] += g * x


def lowpass(x, k):
    y, acc = np.empty_like(x), 0.0
    k = np.broadcast_to(k, x.shape)
    for i, v in enumerate(x):
        acc += k[i] * (v - acc)
        y[i] = acc
    return y


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


def mallet(m, d=0.9, vel=0.2):
    tt = t(d)
    f = note(m)
    return vel * np.exp(-6 * tt) * np.minimum(1, tt / 0.003) * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 4 * f * tt) * np.exp(-14 * tt))


def bell(m, d=1.2, vel=0.2):
    tt = t(d)
    f = note(m)
    return vel * np.exp(-3.5 * tt) * (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-6 * tt))


def pad(ms, d, vel=0.06):
    tt = t(d)
    env = np.minimum(1, tt / 0.4) * np.minimum(1, (d - tt) / 0.4)
    return vel * env * sum(np.sin(2 * np.pi * note(m) * (1 + dt) * tt) for m in ms for dt in (-0.003, 0.003)) / (2 * len(ms))


def tap():
    tt = t(0.08)
    return 0.5 * np.exp(-60 * tt) * np.sin(2 * np.pi * 1900 * tt) + 0.2 * rng.standard_normal(len(tt)) * np.exp(-90 * tt)


def whoosh(d=0.35, vel=0.35):
    tt = t(d)
    return vel * lowpass(rng.standard_normal(len(tt)), 0.05 + 0.3 * np.sin(np.pi * tt / d) ** 2) * np.sin(np.pi * tt / d) ** 1.5


def pofu():
    tt = t(0.35)
    f = 220 * np.exp(-5 * tt)
    return 0.55 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-9 * tt) + 0.15 * lowpass(rng.standard_normal(len(tt)), 0.05) * np.exp(-12 * tt)


def boing(up=True):
    tt = t(0.3)
    f = (300 + 500 * tt / 0.3) if up else (500 - 300 * tt / 0.3)
    return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-5 * tt) * (1 + 0.3 * np.sin(2 * np.pi * 18 * tt))


def rewind_fx():
    """The tail of her take played backwards, fast, plus a whoosh."""
    x = load('own.mp3', 1.2, 0.6)[::-1]
    x = np.interp(np.linspace(0, len(x) - 1, int(0.3 * SR)), np.arange(len(x)), x)
    return 0.6 * x + whoosh(0.3, 0.4)


def bed():
    bus = np.zeros(N)
    beat = 60 / 100
    chords = [[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]]   # D Bm G A
    pattern = [0, 2, 1, 2, 0, 2, 1, 2]
    k, at = 0, BED[0]
    while at < BED[1] - 0.05:
        ch = chords[(k // 8) % 4]
        if k % 8 == 0:
            place(bus, pad([m - 12 for m in ch], min(4 * beat, BED[1] - at)), at)
        joy = at >= PERK
        place(bus, mallet(ch[pattern[k % 8]] + 12 + (12 if joy and k % 2 else 0), 0.8, 0.13 if k % 2 else 0.18), at)
        k += 1
        at += beat / 2
    for m in [74, 78, 81, 86]:                                          # end chord
        place(bus, bell(m, 2.2, 0.16), END + 0.02 * (m - 74) / 4)
    place(bus, pad([50, 57, 62, 66], DUR - END, 0.08), END)
    return bus


def main():
    voice, sfx = np.zeros(N), np.zeros(N)
    s, ln, off = OWN_TAIL
    place(voice, load('own.mp3', off, ln), s)
    place(voice, load('own.mp3', 0, 2.76), OWN_FULL)
    place(voice, load('model.mp3', 0, 1.78), MODEL)
    place(voice, load('model.mp3', 0, 1.78), SHADOW, 0.9)
    place(sfx, rewind_fx(), REWIND)
    place(sfx, tap(), TAP_REC)
    place(sfx, pofu(), POFU)
    place(sfx, tap(), TAP_MODEL)
    for i, m in enumerate([86, 90, 93, 98]):
        place(sfx, bell(m, 1.0, 0.07), PERK + i * 0.06)   # -6 dB: the model voice is the proof, keep it on top
    place(sfx, boing(True), JUMP[0])
    place(sfx, pofu() * 0.6, JUMP[1])
    for i, m in enumerate([81, 85, 88]):
        place(sfx, bell(m, 0.9, 0.12), PUMP + i * 0.07)
    place(sfx, whoosh(0.25, 0.25), RESULT)                                 # card in
    for i in range(5):                                                      # radar axes fill
        place(sfx, tap() * 0.35, RESULT + 0.15 + i * 0.07)
    for i, m in enumerate([86, 90]):                                        # score lands
        place(sfx, bell(m, 0.9, 0.12), RESULT + 0.75 + i * 0.07)
    music = bed()
    env = lowpass(np.abs(voice), 0.002)
    duck = lowpass(1 - 0.75 * np.clip(env / (env.max() * 0.12), 0, 1), 0.0008)
    mix = voice + 0.6 * sfx + 0.55 * music * duck
    mix /= np.abs(mix).max() / 0.9
    out = ROOT / 'hf-short/assets/mix.wav'
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix('.raw.wav')
    with wave.open(str(raw), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), str(out)], check=True)
    raw.unlink()
    print(out)


if __name__ == '__main__':
    main()
