"""069 Real Slang 2「お腹すいてイライラ＝？」 sound: three own-voice English clips, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-slang-hangry/source/scripts/mix.py
Own voice (Gemini gemini-3.8-flash-tts via kits/mimi-short/scripts/ownvoice.py; WAVs not in Git, Drive Slang2_Hangry_assets/own-voice/):
  youre.wav   "You're hangry!"                         Mimi; speech 0.21-1.79 s (silencedetect -40 dB)
  example.wav "I'm getting hangry; let's find lunch."  the Friend, the deck example; speech 0.22-2.59 s
  term.wav    "Hangry."                                the term alone, for the meaning card (isolated take)
Every clip is placed whole (no cuts inside a clip), so heads and tails are the generator's own silence.
Built from films/mimi-slang-no-cap/source/scripts/mix.py (series template): same structure and levels.
"""
import json as _j
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, lowpass, pochi, pofu, pop_seq, t, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = 0.0          # beat hook: hook card, the Friend fuming over an empty bento, the tummy growls
YOURE = 1.0         # youre.wav: speech 1.21-2.79
GAG = 3.0           # beat gag: the Friend admits it with the deck example
EXAMPLE = 3.0       # example.wav: speech 3.22-5.59
MEANING = 5.9       # beat meaning: the deck card (all rows in by 6.45)
TERM = 6.0          # term.wav
EXAMPLE2 = 7.4      # example.wav again under the lit example row: speech 7.62-9.99
APP = 10.1          # beat app: My Notes → 単語帳 → スラング・カジュアル → ユニット6 → hangry → save
TAPS = (10.95, 11.9)   # スラング・カジュアル, ユニット6
SCROLL = 12.4
SAVE = 13.45        # the bookmark tapped
SAVED = 13.5
CTA = 14.5          # beat cta: 次のスラングは？コメントで
END = 16.3          # beat end: end card, CTA tap at END + 0.6
DUR = 17.8


def growl(d=0.75, vel=0.10):
    """A soft, low tummy growl: a wobbling ~85 Hz tone, lowpassed (no bright edge)."""
    tt = t(d)
    f = 85 + 18 * np.sin(2 * np.pi * 7 * tt) + 10 * np.sin(2 * np.pi * 2.3 * tt)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.35 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 1.5
    return lowpass(x * env, 0.05) * vel


def clip_lufs(path):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    return float(_j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))['input_i'])


# A gentle dialogue compressor per clip (as in films/mimi-decks-fine v3), then per-clip gain to one loudness, so the
# three takes sit level and the master limiter barely works.
RAW_VD = SRC / 'assets/own-voice'
VD = SRC / 'hf/assets/own-voice-comp'           # derived from the biometric WAVs: inside hf/assets/, not in Git
VD.mkdir(parents=True, exist_ok=True)
NAMES = tuple(n for n in ('youre', 'example', 'term') if (RAW_VD / f'{n}.wav').exists())
if len(NAMES) < 3:
    print('WARNING: missing own-voice clips, mixed without them:', {'youre', 'example', 'term'} - set(NAMES))
for n in NAMES:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(RAW_VD / f'{n}.wav'), '-af',
                    'acompressor=threshold=-30dB:ratio=3:attack=0.5:release=120:knee=6', str(VD / f'{n}.wav')], check=True)
L = {n: clip_lufs(VD / f'{n}.wav') for n in NAMES}
TARGET = -20.0                                  # LUFS per clip after makeup (as in the series template)
G = {n: 0.9 * 10 ** ((TARGET - L[n]) / 20) for n in L}
print('clip loudness', {n: round(v, 1) for n, v in L.items()}, 'gains', {n: round(v, 3) for n, v in G.items()})

m = Mix(DUR, voice_dir=VD)
# hook: the tummy growls, Mimi points
m.sfx(pop_seq(1, 0.05, base=79), HOOK + 0.05)
m.sfx(growl(), HOOK + 0.15)
m.sfx(whoosh(0.2, 0.15), YOURE + 0.1)
m.voice('youre.wav', YOURE, g=G['youre'])
# gag: the Friend admits it
m.sfx(whoosh(0.25, 0.2), GAG)
m.voice('example.wav', EXAMPLE, g=G['example'])
m.sfx(growl(0.6, 0.07), GAG + 2.0)
# meaning: card rows (all in within 0.55 s)
m.sfx(whoosh(0.3, 0.3), MEANING)
m.sfx(pop_seq(3, 0.17, base=76), MEANING + 0.2)
if 'term' in G:
    m.voice('term.wav', TERM, g=G['term'])
m.voice('example.wav', EXAMPLE2, g=G['example'])
# app
m.sfx(whoosh(0.35, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(whoosh(0.25, 0.2), SCROLL)
m.sfx(tap() * 0.6, SAVE)
m.sfx(ding(), SAVED)
# cta
m.sfx(whoosh(0.3, 0.3), CTA)
m.sfx(pop_seq(2, 0.06, base=79), CTA + 0.2)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)
# Static mix: the same bus balance and ducking as Mix.write, but no dynamic loudnorm (its single pass lifted the voiceless
# app beat to the voice's level, as in films/mimi-decks-fine v2). One gain for the whole film toward -14 LUFS integrated,
# capped so the BGM-only app beat stays at or under BED_RMS and the limiter takes at most GR_MAX dB off the loudest peak.
BED_RMS = -26.0
GR_MAX = 4.0
env = lowpass(np.abs(m.v), 0.002)
duck = lowpass(1 - 0.75 * np.clip(env / (env.max() * 0.12 + 1e-9), 0, 1), 0.0008)
mix = m.v + 0.35 * lowpass(m.s, 0.35) + 0.55 * m.m * duck
mix /= np.abs(mix).max() / 0.9
out = SRC / 'hf/assets/mix.wav'
out.parent.mkdir(parents=True, exist_ok=True)


def save(x, path):
    import wave
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.stack([x, x], 1).clip(-1, 1) * 32767).astype(np.int16).tobytes())


def lufs(f):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    d = _j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))
    return float(d['input_i']), float(d['input_tp'])


def rms(x, a, b):
    seg = x[int(a * SR):int(b * SR)]
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12)


raw = out.with_suffix('.raw.wav')
save(mix, raw)
i0, _ = lufs(raw)
bed = rms(mix, APP + 0.4, CTA - 0.2)               # the voiceless app beat (whooshes and taps included)
peak = 20 * np.log10(np.abs(mix).max())
gain = min(-14.0 - i0, BED_RMS - bed, 20 * np.log10(0.76) + GR_MAX - peak)
for _ in range(3):                                  # the limiter takes a little loudness back: top up, inside the same caps
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af',
                    f'volume={gain:.2f}dB,alimiter=limit=0.76:level=false:attack=1:release=60', '-ar', str(SR), str(out)], check=True)
    i, tp = lufs(out)
    if abs(i + 14) < 0.3:
        break
    gain = min(gain + (-14.0 - i) + 0.1, BED_RMS - bed, 20 * np.log10(0.76) + GR_MAX - peak)
gr = max(0.0, peak + gain - 20 * np.log10(0.76))
raw.unlink()
i, tp = lufs(out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP; limiter GR max %.1f dB; gain %.1f dB (to -14: %.1f, bed cap: %.1f, GR cap: %.1f)' % (
    i, tp, gr, gain, -14.0 - i0, BED_RMS - bed, 20 * np.log10(0.76) + GR_MAX - peak),
    '| app-beat RMS %.1f dBFS, youre RMS %.1f, example RMS %.1f, example2 RMS %.1f dBFS' % (
    bed + gain, rms(mix, 1.21, 2.79) + gain, rms(mix, 3.22, 5.59) + gain, rms(mix, 7.62, 9.99) + gain))
