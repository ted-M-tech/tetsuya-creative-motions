"""Mimi shorts sound kit: voice placement, code-made SFX, the Lanclo SNS theme bed, ducking and loudness.

The bed is the Lanclo SNS theme, OpenTracks「Everyone Get Up」(Anonyment), read from library/bgm/everyone-get-up.mp3.
It is not in Git (the licence forbids passing the file on): copy it from Lanclo's Google Drive, 002.SNS/_BGM/.
Without it the code-made 100 BPM mallet bed plays instead.

An episode's mix.py builds a Mix, places its cues, and calls write():

    from sfx import Mix, tap, pofu, bell, whoosh, boing, clang
    m = Mix(15.0, voice_dir='assets/voice')
    m.voice('line.wav', at=0.2)
    m.sfx(tap(), 1.6)
    m.bed(1.3, 14.0, joy_from=6.4)
    m.end_chord(14.0)
    m.write('hf/assets/mix.wav')
"""
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 48000
THEME = Path(__file__).resolve().parent.parent / 'library/bgm/everyone-get-up.mp3'
THEME_GAIN = 0.1  # with the 0.55 music bus: about 21 dB under the narration
_rng = np.random.default_rng(7)


def t(d):
    return np.arange(int(d * SR)) / SR


def lowpass(x, k):
    y, acc = np.empty_like(x), 0.0
    k = np.broadcast_to(k, x.shape)
    for i, v in enumerate(x):
        acc += k[i] * (v - acc)
        y[i] = acc
    return y


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


def load(path, start=0.0, length=None, speed=1.0):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(path)]
    cmd += (['-t', str(length)] if length else [])
    cmd += (['-af', f'atempo={speed}'] if speed != 1.0 else []) + ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)
    f = min(int(0.02 * SR), len(x) // 4)
    if f:
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
    return x


# ---------- instruments ----------
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


# ---------- SFX ----------
def tap():
    tt = t(0.08)
    return 0.5 * np.exp(-60 * tt) * np.sin(2 * np.pi * 1900 * tt) + 0.2 * _rng.standard_normal(len(tt)) * np.exp(-90 * tt)


def pochi(vel=0.3):
    """A soft button press: a short low click with a tiny release."""
    tt = t(0.12)
    f = 760 * (1 + 0.3 * np.exp(-80 * tt))
    click = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-45 * tt)
    rel = np.zeros(len(tt))
    k = t(0.03)
    i = int(0.07 * SR)
    rel[i:i + len(k)] = 0.35 * np.sin(2 * np.pi * 1150 * k) * np.exp(-150 * k)
    return vel * (click + rel + 0.15 * _rng.standard_normal(len(tt)) * np.exp(-400 * tt))


def whoosh(d=0.35, vel=0.35):
    tt = t(d)
    return vel * lowpass(_rng.standard_normal(len(tt)), 0.05 + 0.3 * np.sin(np.pi * tt / d) ** 2) * np.sin(np.pi * tt / d) ** 1.5


def pofu():
    tt = t(0.35)
    f = 220 * np.exp(-5 * tt)
    return 0.55 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-9 * tt) + 0.15 * lowpass(_rng.standard_normal(len(tt)), 0.05) * np.exp(-12 * tt)


def boing(up=True):
    tt = t(0.3)
    f = (300 + 500 * tt / 0.3) if up else (500 - 300 * tt / 0.3)
    return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-5 * tt) * (1 + 0.3 * np.sin(2 * np.pi * 18 * tt))


def clang(vel=0.6):
    """Metal drop: inharmonic partials with a fast attack, for a falling prop."""
    tt = t(1.2)
    partials = [(523, 1.0, 4), (1288, 0.6, 6), (2210, 0.45, 9), (3470, 0.3, 12)]
    x = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-dk * tt) for f, a, dk in partials)
    hit = 0.5 * _rng.standard_normal(len(tt)) * np.exp(-60 * tt)
    return vel * (x / 2.4 + hit)


def poof():
    """Soft disappearing puff."""
    tt = t(0.4)
    return 0.4 * lowpass(_rng.standard_normal(len(tt)), 0.02 + 0.2 * (1 - tt / 0.4)) * np.exp(-6 * tt)


def freeze(vel=0.5):
    """Ice forming: a rising crackle of tiny clicks over a cold high ring."""
    tt = t(0.6)
    clicks = np.zeros(len(tt))
    for at in np.sort(_rng.uniform(0, 0.45, 40)):
        i = int(at * SR)
        k = t(0.012)
        clicks[i:i + len(k)] += _rng.uniform(0.3, 1) * np.sin(2 * np.pi * _rng.uniform(2500, 6000) * k) * np.exp(-400 * k)
    ring = 0.25 * np.sin(2 * np.pi * 2637 * tt) * np.minimum(1, tt / 0.3) * np.exp(-5 * np.maximum(0, tt - 0.3))
    return vel * (clicks * 0.6 + ring)


def shatter(vel=0.55):
    """Ice breaking: a bright noise burst and scattered glassy pings."""
    tt = t(0.9)
    burst = _rng.standard_normal(len(tt)) * np.exp(-25 * tt)
    burst -= lowpass(burst, 0.15)
    pings = np.zeros(len(tt))
    k = t(0.4)
    for f, d in zip(_rng.uniform(2000, 5000, 8), _rng.uniform(0.02, 0.4, 8)):
        i = int(d * SR)
        pings[i:i + len(k)] += 0.3 * np.sin(2 * np.pi * f * k) * np.exp(-12 * k)
    return vel * (0.7 * burst + pings)


def mokugyo(vel=0.6):
    """Wooden fish drum: a hollow knock (pok)."""
    tt = t(0.25)
    f = 620 * (1 + 0.08 * np.exp(-60 * tt))
    knock = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-28 * tt) + 0.4 * np.sin(2 * np.pi * 1240 * tt) * np.exp(-45 * tt)
    return vel * (knock + 0.3 * _rng.standard_normal(len(tt)) * np.exp(-300 * tt))


def pop_seq(n, gap, base=79, vel=0.16):
    """n small rising pops, gap seconds apart (cells filling, items appearing)."""
    x = np.zeros(int((n * gap + 0.6) * SR))
    for i in range(n):
        k = mallet(base + [0, 2, 4, 7, 9, 12][i % 6], 0.5, vel)
        j = int(i * gap * SR)
        x[j:j + len(k)] += k
    return x


def pencil(d=1.0, vel=0.18):
    """Pencil or brush strokes: band-limited scratchy noise in short strokes."""
    tt = t(d)
    x = _rng.standard_normal(len(tt))
    x = lowpass(x, 0.35) - lowpass(x, 0.05)
    strokes = np.clip(np.sin(2 * np.pi * 3.2 * tt), 0, None) ** 0.6
    return vel * x * strokes


def ding(vel=0.14):
    gap = int(0.07 * SR)
    a, b = bell(86, 0.9, vel), bell(90, 0.9, vel)
    return np.pad(a, (0, gap)) + np.pad(b, (gap, 0))


# ---------- mix ----------
class Mix:
    def __init__(self, duration, voice_dir='assets/voice'):
        self.n = int(SR * duration)
        self.duration = duration
        self.voice_dir = Path(voice_dir)
        self.v = np.zeros(self.n)
        self.s = np.zeros(self.n)
        self.m = np.zeros(self.n)

    def _place(self, bus, x, at, g=1.0):
        i = int(at * SR)
        x = x[:max(0, self.n - i)]
        bus[i:i + len(x)] += g * x

    def voice(self, name, at, g=0.9, start=0.0, length=None, speed=1.0, muffle=False):
        """muffle: heard through something (inside ice, behind a door)."""
        x = load(self.voice_dir / name, start, length, speed)
        self._place(self.v, lowpass(x, 0.06) * 1.6 if muffle else x, at, g)

    def sfx(self, x, at, g=1.0):
        self._place(self.s, x, at, g)

    def bed(self, start, end, joy_from=None):
        """The theme from start, eased in, running on to the end of the film (end_chord fades it out).
        Without the theme file: a 100 BPM D-major mallet arpeggio over a pad, an octave lift on off-beats from joy_from."""
        if THEME.exists():
            x = load(THEME, 0.0, self.duration - start)
            f = int(0.4 * SR)
            x[:f] *= np.linspace(0, 1, f)
            self._place(self.m, x, start, THEME_GAIN)
            self.themed = True
            return
        beat = 60 / 100
        chords = [[62, 66, 69], [59, 62, 66], [55, 59, 62], [57, 61, 64]]
        pattern = [0, 2, 1, 2, 0, 2, 1, 2]
        k, at = 0, start
        while at < end - 0.05:
            ch = chords[(k // 8) % 4]
            if k % 8 == 0:
                self._place(self.m, pad([m - 12 for m in ch], min(4 * beat, end - at)), at)
            lift = 12 if joy_from is not None and at >= joy_from and k % 2 else 0
            self._place(self.m, mallet(ch[pattern[k % 8]] + 12 + lift, 0.8, 0.13 if k % 2 else 0.18), at)
            k += 1
            at += beat / 2

    def end_chord(self, at):
        if getattr(self, 'themed', False):  # the theme carries on and fades out over the end card
            tt = np.arange(self.n) / SR
            self.m *= np.interp(tt, [0, at, self.duration], [1, 1, 0])
            return
        for i, m in enumerate([74, 78, 81, 86]):
            self._place(self.m, bell(m, 2.2, 0.16), at + 0.02 * i)
        self._place(self.m, pad([50, 57, 62, 66], max(0.5, self.duration - at), 0.08), at)

    def write(self, out, lufs=-14):
        env = lowpass(np.abs(self.v), 0.002)
        duck = lowpass(1 - 0.75 * np.clip(env / (env.max() * 0.12 + 1e-9), 0, 1), 0.0008)
        # SFX quieter and softened (a one-pole lowpass, ~3 kHz): high bells were piercing on earphones
        mix = self.v + 0.35 * lowpass(self.s, 0.35) + 0.55 * self.m * duck
        mix /= np.abs(mix).max() / 0.9
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        raw = out.with_suffix('.raw.wav')
        with wave.open(str(raw), 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', f'loudnorm=I={lufs}:TP=-1.5:LRA=11', '-ar', str(SR), str(out)], check=True)
        raw.unlink()
        return out
