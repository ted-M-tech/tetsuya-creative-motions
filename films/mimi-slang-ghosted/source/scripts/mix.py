"""070 Real Slang 3「既読スルー、英語で？」 sound: four own-voice English clips, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-slang-ghosted/source/scripts/mix.py
Own voice (Gemini gemini-3.8-flash-tts via kits/mimi-short/scripts/ownvoice.py; WAVs not in Git, Drive Slang3_Ghosted_assets/own-voice/):
  ghosted.wav "You got ghosted."                              Mimi, teasing the Friend
  huh.wav     "Ghosted...?"                                   the Friend, wondering about a real ghost
  ghost.wav   "Ghost."                                        the term alone, for the meaning card (isolated take)
  example.wav "I didn't mean to ghost you; my phone broke."   the deck example (slang-casual/08.json)
Every clip is placed whole (no cuts inside a clip), so heads and tails are the generator's own silence.
Series template: films/mimi-slang-no-cap/source/scripts/mix.py (same structure, static mix, -14 LUFS).
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
from sfx import SR, Mix, ding, lowpass, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = 0.0          # beat hook: hook card + the read chat with no reply
GHOSTED = 1.0       # ghosted.wav (Mimi)
GAG = 3.0           # beat gag: a little ghost floats out of the chat
HUH = 3.15          # huh.wav (the Friend)
MEANING = 5.0       # beat meaning: the deck card (ghost / leave sb on read), every row in by 5.85
GHOST = 5.1         # ghost.wav
EXAMPLE = 5.9       # example.wav under the example row
APP = 9.4           # beat app: スラング・カジュアル units → ユニット8 → ghost → save
TAPS = (10.3,)      # ユニット8
SCROLL = 10.95      # the real scroll to the card
SAVE = 12.3         # the bookmark tapped
SAVED = 12.45
CTA = 13.8          # beat cta: 次のスラングは？コメントで
END = 15.6          # beat end: end card, CTA tap at END + 0.6
DUR = 17.1


def clip_lufs(path):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    return float(_j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))['input_i'])


# A gentle dialogue compressor per clip (as in films/mimi-decks-fine v3), then per-clip gain to one loudness, so the
# three takes sit level and the master limiter barely works.
RAW_VD = SRC / 'assets/own-voice'
VD = SRC / 'hf/assets/own-voice-comp'           # derived from the biometric WAVs: inside hf/assets/, not in Git
VD.mkdir(parents=True, exist_ok=True)
NAMES = [n for n in ('ghosted', 'huh', 'ghost', 'example') if (RAW_VD / f'{n}.wav').exists()]
MISSING = sorted({'ghosted', 'huh', 'ghost', 'example'} - set(NAMES))
if MISSING:
    print('WARNING: own-voice clips missing, mixed without them (provisional):', MISSING)
for n in NAMES:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(RAW_VD / f'{n}.wav'), '-af',
                    'acompressor=threshold=-30dB:ratio=3:attack=0.5:release=120:knee=6', str(VD / f'{n}.wav')], check=True)
L = {n: clip_lufs(VD / f'{n}.wav') for n in NAMES}
TARGET = -20.0                                  # LUFS per clip after makeup
G = {n: 0.9 * 10 ** ((TARGET - L[n]) / 20) for n in L}
print('clip loudness', {n: round(v, 1) for n, v in L.items()}, 'gains', {n: round(v, 3) for n, v in G.items()})

m = Mix(DUR, voice_dir=VD)
_voice = m.voice
def voice(name, at, g):                        # a missing clip (provisional mix) is skipped
    if name[:-4] in NAMES:
        _voice(name, at, g=g)
# hook: the read chat pops; the typing dots stop; Mimi teases
m.sfx(pop_seq(1, 0.05, base=79), HOOK + 0.05)
m.sfx(pofu() * 0.35, 0.85)
voice('ghosted.wav', GHOSTED, g=G.get('ghosted'))
# gag: the ghost floats up out of the chat
m.sfx(whoosh(0.3, 0.25), GAG)
voice('huh.wav', HUH, g=G.get('huh'))
# meaning: card rows (all in within 0.9 s)
m.sfx(whoosh(0.3, 0.3), MEANING)
voice('ghost.wav', GHOST, g=G.get('ghost'))
m.sfx(pop_seq(1, 0.05, base=76), 5.45)
m.sfx(pop_seq(1, 0.05, base=76), 5.85)
voice('example.wav', EXAMPLE, g=G.get('example'))
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
    '| app-beat RMS %.1f dBFS' % (bed + gain))
