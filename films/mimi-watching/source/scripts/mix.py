"""Mimi is always watching: a quiet horror bed (music-box lullaby, heartbeat, string cluster) for the dark scenes, kit SFX, the theme bed once the lights come on -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-watching/source/scripts/mix.py
No voices: every line is a speech bubble or caption. The owner dislikes loud SFX, so the horror bed is lowpassed and sits at about the theme bed's loudness; it cuts to silence at the light switch.
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, lowpass, note, pochi, pop_seq, t, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = 0.0             # dark room, Mimi's eyes, whispered caption
EYES = 0.9
NOTIFY = 2.3           # the reminder banner drops in
OPEN = 3.7             # she taps it
APP = 3.9              # Mimi's advice
CAPS = (3.95, 5.9, 7.1, 8.5)
SHOCK = 10.3           # "...how does she know?"
LIGHTS = 11.4          # lights on, cheerful Mimi explains
HABIT = 13.0           # your habit ("And then" 4回)
NATIVE = 14.6          # the native version
SAVE = 15.3            # bookmark tap, the phrase flies to My Notes
COPY = 16.4
DARK = 17.9            # lights dim again, the whisper
END = 20.6
CTA_TAP = 21.2
DUR = 22.0

_rng = np.random.default_rng(24)
HORROR_GAIN = 0.42  # horror bed level; set so the dark scenes sit at about the theme bed's loudness (see the record's numbers)


def music_box(m, d=2.2, vel=0.2, cents=-20.0):
    """A worn music-box tine: soft attack, a slow warble and a few cents flat, no bright partials (lowpassed later)."""
    tt = t(d)
    f = note(m) * 2 ** (cents / 1200) * (1 + 0.004 * np.sin(2 * np.pi * 4.3 * tt + _rng.uniform(0, 6.3)))
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(1, tt / 0.004) * np.exp(-2.6 * tt)
    return vel * env * (np.sin(ph) + 0.3 * np.sin(2 * ph) * np.exp(-5 * tt) + 0.08 * np.sin(3.01 * ph) * np.exp(-9 * tt))


def heartbeat(vel=0.5):
    """lub-dub: two low thumps with a little body so phones can hear it."""
    tt = t(0.6)
    x = np.zeros(len(tt))
    for at, a in ((0.0, 1.0), (0.21, 0.7)):
        k = t(0.3)
        f = 48 + 30 * np.exp(-25 * k)
        thump = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-16 * k) * np.minimum(1, k / 0.006)
        i = int(at * SR)
        x[i:i + len(k)] += a * thump
    return vel * x


def string_pad(ms, d, vel=0.1):
    """A dissonant, slightly detuned string-ish cluster (few harmonics, slow vibrato); shape it with an envelope outside."""
    tt = t(d)
    out = np.zeros(len(tt))
    for m in ms:
        for dt in (-0.004, 0.0035):
            f = note(m) * (1 + dt) * (1 + 0.003 * np.sin(2 * np.pi * 5.1 * tt + _rng.uniform(0, 6.3)))
            ph = 2 * np.pi * np.cumsum(f) / SR
            out += sum(np.sin(h * ph) / h for h in (1, 2, 3, 4))
    return vel * out / (2 * len(ms))


def horror_bed(d, melody, beats, swell, pad_notes):
    """One dark stretch: a creepy minor lullaby on a music box, a heartbeat and a string cluster that swells.
    melody: (time, midi, cents); beats: heartbeat times; swell: (times, levels) of the pad envelope."""
    x = np.zeros(int(d * SR))

    def put(y, at):
        i = int(at * SR)
        y = y[:max(0, len(x) - i)]
        x[i:i + len(y)] += y
    for at, mm, c in melody:
        put(music_box(mm, 2.4, 0.2, c), at)
        put(music_box(mm - 12, 2.4, 0.05, c - 8), at)       # a quieter octave below, a little more out of tune
    for at in beats:
        put(heartbeat(0.26), at)
    tt = np.arange(len(x)) / SR
    x += string_pad(pad_notes, d) * np.interp(tt, *swell)
    x = lowpass(lowpass(x, 0.18), 0.25)                     # ~1.5-2 kHz: dark and soft on earphones, no harsh highs
    f = int(0.03 * SR)
    x[-f:] *= np.linspace(1, 0, f)                          # cut, not fade: silence at the light switch
    return x


# Hook: 72 BPM lullaby in A minor (E C A C | B G# E -), slowing and sagging flat into SHOCK; heartbeat 66 -> 84 BPM.
B = 60 / 72
LULLABY = [76, 72, 69, 72, 71, 68, 64, None, 69, 71, 72, 71, 68, None, 64, None]
mel = [(0.5 + i * B * (1 + 0.012 * i), mm, -12 - 1.5 * i) for i, mm in enumerate(LULLABY) if mm is not None and 0.5 + i * B * (1 + 0.012 * i) < SHOCK - 0.3]
mel.append((SHOCK, 63, -30))                                # a lone, wrong note (D#) on "how does she know?"
beats, at = [], 0.9
while at < LIGHTS - 0.4:
    beats.append(at)
    at += 60 / (66 + 18 * at / LIGHTS)
HOOK_BED = horror_bed(LIGHTS - HOOK, mel, beats,
                      ([0, 1.5, 7.0, SHOCK - 0.2, LIGHTS - 0.05], [0.25, 0.35, 0.45, 1.0, 1.0]), [45, 46, 52, 63])
# The whisper at the end: the lullaby's first bar again, slower and lower, two heartbeats, the pad faint.
DARK_BED = horror_bed(END - DARK, [(0.35 + i * 1.1 * B, mm, -25 - 3 * i) for i, mm in enumerate((76, 72, 69))], [0.5, 1.45],
                      ([0, 0.4, END - DARK], [0.0, 0.45, 0.6]), [45, 46, 52])

m = Mix(DUR)
m.sfx(whoosh(0.5, 0.012), EYES - 0.2)
m.sfx(ding(0.025), NOTIFY)
m.sfx(tap() * 0.5, OPEN)
m.sfx(whoosh(0.3, 0.2), APP)
for at in CAPS:
    m.sfx(tap() * 0.25, at)
m.sfx(pochi(0.35), LIGHTS - 0.05)       # the light switch
m.sfx(pop_seq(3, 0.05, base=79), LIGHTS + 0.1)
m.sfx(whoosh(0.3, 0.2), HABIT)
m.sfx(pop_seq(2, 0.06, base=76), HABIT + 0.4)
m.sfx(whoosh(0.3, 0.2), NATIVE)
m.sfx(tap() * 0.5, SAVE)
m.sfx(pop_seq(3, 0.05, base=81), SAVE + 0.05)
m.sfx(whoosh(0.3, 0.25), COPY - 0.1)
m.sfx(pop_seq(2, 0.06, base=76), COPY + 0.05)
m.sfx(pochi(0.3), DARK)                 # lights off
m.sfx(whoosh(0.5, 0.012), DARK + 0.45)
m.bed(LIGHTS, END)
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, DARK, DARK + 0.3, END - 0.1, END + 0.1], [1, 1, 0.12, 0.12, 1])   # the bed sinks while it's dark
m.end_chord(END)
h = np.zeros(m.n)                                     # the horror bed has its own bus: the theme's dimming doesn't touch it
h[:len(HOOK_BED)] += HOOK_BED
h[int(DARK * SR):int(DARK * SR) + len(DARK_BED)] += DARK_BED
m.sfx(pochi(), CTA_TAP)
# Static loudness: the kit's Mix.write ends with a one-pass (dynamic) loudnorm, which lifted the quiet dark opening by ~15 dB
# (there is no voice to anchor it). Same bus balance as Mix.write, then one gain for the whole film to -14 LUFS and a peak limiter.
mix = 0.35 * lowpass(m.s, 0.35) + 0.55 * (m.m + HORROR_GAIN * h)
mix /= np.abs(mix).max() / 0.9
out = SRC / 'hf/assets/mix.wav'
raw = out.with_suffix('.pre.wav')
with wave.open(str(raw), 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(raw), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
lufs = float(meas[meas.rindex('I:'):].split()[1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', f'volume={-14.0 - lufs:.2f}dB,alimiter=limit=0.84:level=false', '-ar', str(SR), str(out)], check=True)
raw.unlink()
print(out)
