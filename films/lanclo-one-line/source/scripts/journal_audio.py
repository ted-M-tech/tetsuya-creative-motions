"""Code-made music and SFX for the English journal short.  usage: journal_audio.py OUT.wav"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from audio import SR, BEAT, CHORDS, mallet, bell, pad, sub, kick, clap, shaker, whoosh, pop, impact, noise, lowpass  # noqa: E402
from journal_timeline import *  # noqa: E402,F403

N = int(DURATION * SR)


def place(bus, x, t, gain=1.0):
    i = int(t * SR)
    x = x[:max(0, N - i)]
    bus[i:i + len(x)] += x * gain


def scribble(d, seed):
    """Pencil on paper: band-passed noise in short strokes."""
    r = np.random.default_rng(seed)
    n = r.standard_normal(int(d * SR))
    n = lowpass(n, 0.35) - lowpass(n, 0.04)
    t = np.arange(len(n)) / SR
    strokes = np.clip(np.sin(2 * np.pi * 3.3 * t + r.uniform(0, 6)) * 1.4, 0, 1) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t))
    return 0.22 * n * strokes


def music():
    bus = np.zeros(N)
    breath = MOVE5[0] + 0.3
    bar = 4 * BEAT
    t, idx = 0.0, 0
    while t < breath:
        root, ch = CHORDS[(idx // 2) % 4]
        d = min(bar, breath - t)
        place(bus, pad([m - 12 for m in ch[:3]], d + 0.4), t)
        place(bus, sub(root - 24, d, 0.45), t)
        for k in range(8):
            tt = t + k * BEAT / 2
            if tt >= breath:
                break
            place(bus, mallet(ch[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12, 0.9, 0.16 if k % 2 else 0.22), tt)
        t += bar
        idx += 1
    t = MOVE2[0] + 0.6  # groove from the feedback onwards
    while t < breath - 0.05:
        b = round((t - MOVE2[0] - 0.6) / BEAT)
        place(bus, kick(), t, 0.55)
        if b % 2 == 1:
            place(bus, clap(), t, 0.8)
        place(bus, shaker(), t + BEAT / 2)
        t += BEAT
    sw = bell(74, 1.0, 0.5)[::-1] + pad([62, 66, 69], 1.0, 0.25)[::-1]
    place(bus, sw[-int((MIMI_LAND - breath) * SR):], breath)
    place(bus, pad([50, 57, 62, 66, 69], DURATION - MIMI_LAND, 0.22), MIMI_LAND)
    for i, m in enumerate([62, 66, 69, 74]):
        place(bus, mallet(m + 12, 2.5, 0.2), MIMI_LAND + i * 0.02)
    place(bus, sub(38, 3.0, 0.7), MIMI_LAND)
    return bus


def sfx():
    bus = np.zeros(N)
    place(bus, whoosh(0.25, 0.4), 0.0)
    place(bus, impact(0.9), HOOK_LAND)
    place(bus, pop(84, 0.25), QUESTION_IN)
    place(bus, pop(88, 0.3), TITLE_IN)
    place(bus, whoosh(0.5, 0.25), MIMI_HOP[0] + 0.1)
    for w in WHOOSHES:
        place(bus, whoosh(0.8, 0.3), w)
    for i, m in enumerate([81, 88]):  # recording starts
        place(bus, bell(m + 12, 1.0, 0.18), MIC_ON + i * 0.08)
    for i in range(9):  # words land
        place(bus, pop(90 + (i % 3) * 2, 0.07), REC[0] + 0.2 + i * 0.27)
    place(bus, pop(76, 0.3), CARD2_IN[0] + 0.1)
    place(bus, whoosh(0.25, 0.2), STRIKE)
    place(bus, pop(86, 0.3), WENT)
    place(bus, bell(98, 0.8, 0.12), WENT + 0.05)
    for i in range(5):
        place(bus, pop(81 + [0, 2, 4, 7, 9][i], 0.25), SCORES + i * SCORE_GAP)
    place(bus, pop(88, 0.2), TIP)
    place(bus, scribble(DRAW[1] - DRAW[0], 2), DRAW[0])
    for i, m in enumerate([86, 90, 93]):  # colour washes in
        place(bus, bell(m + 12, 1.2, 0.1), TINT[0] + i * 0.1)
    place(bus, pop(83, 0.25), CAPTION)
    for i in range(8):
        place(bus, pop(84 + i, 0.18), PAST + i * PAST_GAP)
    place(bus, impact(0.35), CELL_LAND)
    for i, m in enumerate([76, 83, 88]):
        place(bus, bell(m + 12, 1.4, 0.2), CELL_LAND + i * 0.08)
    place(bus, impact(0.8), MIMI_LAND)
    for i, m in enumerate([74, 78, 81, 86]):
        place(bus, bell(m + 12, 2.2, 0.22), FANFARE + i * 0.09)
    place(bus, pop(79, 0.25), END_CARD)
    return bus


def main():
    mix = music() * 0.55 + sfx() * 0.6
    mix /= np.abs(mix).max() / 0.9
    raw = Path(sys.argv[1]).with_suffix('.raw.wav')
    raw.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(raw), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                    '-ar', str(SR), sys.argv[1]], check=True)
    raw.unlink()


if __name__ == '__main__':
    main()
