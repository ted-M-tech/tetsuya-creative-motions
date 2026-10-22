"""How Lanclo began: the theme bed and soft code-made SFX (footsteps, café clinks, the clock, keyboard, cheer) -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-origin/source/scripts/mix.py
No voices: every line is a speech bubble (Kokoro's Japanese voice garbles them).
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, bell, ding, lowpass, pochi, pofu, pop_seq, t, tap, whoosh  # noqa: E402

rng = np.random.default_rng(11)

# Cue sheet (seconds); hf/index.html uses the same times.
RACE, TEACHER, B1, B2, THUMB = 0.0, 2.2, 3.6, 5.8, 8.0
CAFE = 10.6
CUPS = (11.5, 12.0, 12.5, 13.0, 13.5, 14.0)
CALL = 15.0
KEYS = (15.4, 18.6)
YAY = 19.4
APP = 21.9
CARD1, CARD2 = 23.9, 25.9
SWEAT = 28.3
END = 30.5
CTA_TAP = 31.1
DUR = 32.0


def thump(vel=0.25):
    """A soft running footstep on tarmac."""
    tt = t(0.12)
    body = np.sin(2 * np.pi * 85 * tt) * np.exp(-40 * tt)
    grit = lowpass(rng.standard_normal(len(tt)), 0.08) * np.exp(-55 * tt)
    return vel * (body + 0.6 * grit)


def clink(vel=0.18):
    """A cup set down on a saucer."""
    tt = t(0.5)
    x = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-d * tt) for f, a, d in [(1870, 1, 9), (2950, 0.5, 12), (4120, 0.3, 16)])
    return vel * (x / 1.8 + 0.4 * rng.standard_normal(len(tt)) * np.exp(-200 * tt))


def ticks(d, rate, vel=0.08):
    """The clock hands whirring: fast soft ticks."""
    x = np.zeros(int(d * SR))
    for k in range(int(d * rate)):
        c = tap() * vel
        i = int(k / rate * SR)
        x[i:i + len(c)] += c[:len(x) - i]
    return x


def keyboard(d, vel=0.1):
    x = np.zeros(int(d * SR))
    at = 0.0
    while at < d - 0.05:
        tt = t(0.03)
        c = vel * rng.uniform(0.6, 1) * rng.standard_normal(len(tt)) * np.exp(-180 * tt)
        i = int(at * SR)
        x[i:i + len(c)] += c[:len(x) - i]
        at += rng.uniform(0.06, 0.16)
    return x


def crowd(d, vel=0.12, swell=True):
    """A distant crowd / a small cheer: band-limited noise with a slow flutter."""
    tt = t(d)
    n = rng.standard_normal(len(tt))
    x = lowpass(n, 0.12) - lowpass(n, 0.01)
    env = np.sin(np.pi * tt / d) if swell else np.minimum(1, tt / 0.1) * np.exp(-1.2 * tt)
    return vel * x * env * (1 + 0.3 * np.sin(2 * np.pi * 7 * tt))


m = Mix(DUR)
# The race: a far crowd, the two runners' steps (cadence 0.34 s; the teacher joins at TEACHER, half a step off)
m.sfx(crowd(2.6, 0.18), RACE)
for k in range(int((CAFE - 0.4) / 0.34)):
    m.sfx(thump(0.22), RACE + 0.1 + k * 0.34)
for k in range(int((CAFE - 0.4 - TEACHER) / 0.34)):
    m.sfx(thump(0.18), TEACHER + 0.27 + k * 0.34)
m.sfx(whoosh(0.3, 0.25), TEACHER)
for at in (B1, B2):
    m.sfx(pofu() * 0.35, at)
m.sfx(pop_seq(3, 0.06, base=79), THUMB)
# Café: the clock whirrs through three hours, cups pile up
m.sfx(whoosh(0.35, 0.3), CAFE - 0.1)
m.sfx(ticks(3.4, 14), CAFE + 0.6)
for at in CUPS:
    m.sfx(clink(), at)
# Online calls: typing, a call chime
m.sfx(whoosh(0.35, 0.3), CALL - 0.1)
m.sfx(ding(0.1), CALL + 0.1)
m.sfx(keyboard(KEYS[1] - KEYS[0]), KEYS[0])
# Done! high-five, confetti, a small cheer
m.sfx(whoosh(0.3, 0.3), YAY - 0.1)
m.sfx(bell(86, 0.6, 0.12) + bell(91, 0.6, 0.1), YAY + 0.12)
m.sfx(pop_seq(6, 0.05, base=79), YAY + 0.15)
m.sfx(crowd(1.6, 0.3, swell=False), YAY + 0.12)
# The app
m.sfx(whoosh(0.35, 0.3), APP)
m.sfx(ding(), APP + 0.4)
# Message cards
m.sfx(pop_seq(3, 0.05, base=76), CARD1 + 0.05)
m.sfx(pop_seq(3, 0.05, base=79), CARD2 + 0.05)
# "Go easy on me..."
m.sfx(pofu() * 0.6, SWEAT + 0.1)
m.bed(0.2, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
