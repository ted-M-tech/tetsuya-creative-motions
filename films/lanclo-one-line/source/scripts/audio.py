"""Mix the two LP voice clips, code-made music and SFX.  usage: audio.py OUT.wav"""
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from timeline import *  # noqa: E402,F403

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / 'assets'
SR = 48000
N = int(OUT_DURATION * SR)
rng = np.random.default_rng(3)


def load(path, length=None):
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path)] + (['-t', str(length)] if length else []) + \
          ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()
    f = int(0.03 * SR)
    x[-f:] *= np.linspace(1, 0, f)
    return x


def place(bus, x, t, gain=1.0, story=True):
    """t is on the story clock unless story=False (already output time)."""
    i = int((to_out(t) if story else t) * SR)
    x = x[:max(0, N - i)]
    bus[i:i + len(x)] += x * gain


def tsec(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, k):
    """One-pole lowpass; k may be an array (time-varying)."""
    y = np.empty_like(x)
    acc = 0.0
    k = np.broadcast_to(k, x.shape)
    for i in range(len(x)):
        acc += k[i] * (x[i] - acc)
        y[i] = acc
    return y


def note(f):
    return 440 * 2 ** ((f - 69) / 12)


# ---------- instruments ----------
def mallet(midi, d=1.2, vel=1.0):
    t = tsec(d)
    f = note(midi)
    env = np.exp(-5.5 * t) * np.minimum(1, t / 0.003)
    return vel * env * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-14 * t))


def bell(midi, d=1.8, vel=1.0):
    t = tsec(d)
    f = note(midi)
    env = np.exp(-3.2 * t) * np.minimum(1, t / 0.002)
    return vel * env * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-6 * t)
                        + 0.2 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-10 * t))


def pad(midis, d, vel=0.12):
    t = tsec(d)
    env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    out = sum(np.sin(2 * np.pi * note(m) * (1 + det) * t) for m in midis for det in (-0.003, 0, 0.003))
    return vel * env * out / (3 * len(midis))


def sub(midi, d, vel=0.5):
    t = tsec(d)
    return vel * np.sin(2 * np.pi * note(midi) * t) * np.exp(-2.2 * t) * np.minimum(1, t / 0.01)


def kick():
    t = tsec(0.4)
    f = 45 + 80 * np.exp(-30 * t)
    return 0.9 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-9 * t)


def noise(d):
    return rng.standard_normal(int(d * SR)).astype(np.float64)


def clap():
    n = noise(0.18)
    n = n - lowpass(n, 0.15)
    return 0.35 * n * np.exp(-28 * tsec(0.18))


def shaker():
    n = noise(0.07)
    n = n - lowpass(n, 0.5)
    return 0.12 * n * np.sin(np.pi * tsec(0.07) / 0.07)


def whoosh(d=0.7, vel=0.35):
    t = tsec(d)
    n = noise(d)
    k = 0.02 + 0.25 * np.sin(np.pi * t / d) ** 2
    return vel * lowpass(n, k) * np.sin(np.pi * t / d) ** 1.5


def pop(midi=84, vel=0.35):
    t = tsec(0.14)
    f = note(midi) * (1 + 0.5 * np.exp(-40 * t))
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-30 * t)


def impact(vel=1.0):
    t = tsec(1.2)
    body = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-12 * t)) / SR) * np.exp(-3.5 * t)
    n = noise(1.2)
    return vel * (0.9 * body + 0.25 * lowpass(n, 0.08) * np.exp(-10 * t))


# ---------- music: 100 BPM, D major ----------
BEAT = 60 / 100
CHORDS = [(62, [62, 66, 69, 74]), (59, [59, 62, 66, 71]), (55, [55, 59, 62, 67]), (57, [57, 61, 64, 69])]  # D Bm G A


def music():
    """Runs on output time so the tempo grid stays steady."""
    bus = np.zeros(N)
    BREATH_O, LAND_O, GROOVE_O = to_out(BREATH), to_out(MIMI_LAND), to_out(WHOOSHES[1]) + 0.6
    bar = 4 * BEAT
    t = 0.0
    idx = 0
    while t < BREATH_O:
        root, ch = CHORDS[(idx // 2) % 4]
        d = min(bar, BREATH_O - t)
        place(bus, pad([m - 12 for m in ch[:3]], d + 0.4), t, story=False)
        place(bus, sub(root - 24, d, 0.45), t, story=False)
        for k in range(8):  # mallet 8ths
            tt = t + k * BEAT / 2
            if tt >= BREATH_O:
                break
            pattern = [0, 2, 1, 3, 2, 1, 3, 2]
            place(bus, mallet(ch[pattern[k]] + 12, 0.9, 0.16 if k % 2 else 0.22), tt, story=False)
        t += bar
        idx += 1
    # groove from the radar onwards
    t = GROOVE_O
    while t < BREATH_O - 0.05:
        b = round((t - GROOVE_O) / BEAT)
        place(bus, kick(), t, 0.55, story=False)
        if b % 2 == 1:
            place(bus, clap(), t, 0.8, story=False)
        place(bus, shaker(), t + BEAT / 2, story=False)
        t += BEAT
    # breath: reversed swell into the landing
    sw = bell(74, 1.0, 0.5)[::-1] + pad([62, 66, 69], 1.0, 0.25)[::-1]
    place(bus, sw[-int((LAND_O - BREATH_O) * SR):], BREATH_O, story=False)
    # full chord + low hit ringing under the end card
    place(bus, pad([50, 57, 62, 66, 69], OUT_DURATION - LAND_O, 0.22), LAND_O, story=False)
    for i, m in enumerate([62, 66, 69, 74]):
        place(bus, mallet(m + 12, 2.5, 0.2), LAND_O + i * 0.02, story=False)
    place(bus, sub(38, 3.0, 0.7), LAND_O, story=False)
    return bus


def sfx():
    bus = np.zeros(N)
    place(bus, whoosh(0.25, 0.4), 0.0)
    place(bus, impact(0.9), HOOK_LAND)
    place(bus, whoosh(0.5, 0.18), LOGO_LINE[0])
    place(bus, pop(88, 0.25), LOGO_LINE[1])
    place(bus, whoosh(0.5, 0.25), MIMI_HOP[0] + 0.1)
    for w in WHOOSHES:
        place(bus, whoosh(0.8, 0.3), w)
    place(bus, pop(79, 0.3), CARD_IN[0] + 0.15)
    place(bus, pop(83, 0.25), MODEL_START - 0.3)
    place(bus, whoosh(0.6, 0.15), MERGE[0])
    place(bus, pop(81, 0.25), PENT[1])
    for i in range(5):
        place(bus, pop(84 + i * 2, 0.12), PENT[0] + i * 0.12)
    place(bus, pop(76, 0.3), FILL[0] + 0.2)
    place(bus, pop(79, 0.3), NEXT_CARD[0])
    place(bus, pop(86, 0.2), NEXT_SENTENCE)
    for i, m in enumerate([76, 83]):  # Mimi's small "yes"
        place(bus, bell(m + 12, 1.4, 0.22), MIMI_SUCCESS + i * 0.09)
    for i, t in enumerate(NODES):
        place(bus, pop(81 + [0, 2, 4, 7][i], 0.35), t)
        place(bus, bell(81 + [0, 2, 4, 7][i] + 12, 1.0, 0.08), t)
    place(bus, pop(84, 0.2), TAG[0])
    place(bus, pop(88, 0.2), TAG[1])
    place(bus, impact(0.8), MIMI_LAND)
    for i, m in enumerate([74, 78, 81, 86]):  # completion fanfare, the sonic button
        place(bus, bell(m + 12, 2.2, 0.22), FANFARE + i * 0.09)
    place(bus, pop(79, 0.25), END_CARD)
    return bus


def voice():
    """No narration: only the two LP comparison clips."""
    bus = np.zeros(N)
    for name, start, length in (('own.mp3', OWN_START, OWN_LEN), ('model.mp3', MODEL_START, MODEL_LEN)):
        path = A / 'voice' / name
        if path.exists():
            place(bus, load(path, length), start, 0.9)
        else:
            print(f'missing assets/voice/{name}: rendering without it', file=sys.stderr)
    return bus


def main():
    v, m, s = voice(), music(), sfx()
    env = lowpass(np.abs(v), 0.002)
    duck = 1 - 0.78 * np.clip(env / (env.max() * 0.15 + 1e-9), 0, 1)  # about -13 dB under every word
    duck = lowpass(duck, 0.0008)
    mix = v * 1.0 + m * 0.55 * duck + s * 0.6
    mix /= np.abs(mix).max() / 0.9
    raw = Path(sys.argv[1]).with_suffix('.raw.wav')
    raw.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    import wave
    with wave.open(str(raw), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                    '-ar', str(SR), sys.argv[1]], check=True)
    raw.unlink()


if __name__ == '__main__':
    main()
