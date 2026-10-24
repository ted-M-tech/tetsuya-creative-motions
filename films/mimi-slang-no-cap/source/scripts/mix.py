"""068 Real Slang 1「"No cap" = 帽子なし？」 sound: three own-voice English clips, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-slang-no-cap/source/scripts/mix.py
Own voice (Gemini gemini-3.8-flash-tts via kits/mimi-short/scripts/ownvoice.py; WAVs not in Git, Drive Slang1_NoCap_assets/own-voice/):
  claim.wav "No cap, I practiced that move fifty times."  Mimi, the deck example; speech 0.22-2.89 s (silencedetect -40 dB)
  huh.wav   "Cap...?"                                      the Friend, looking for a hat; speech 0.21-0.76 s
  nocap.wav "No cap."                                      the term alone, for the meaning card; speech 0.27-0.84 s
Every clip is placed whole (no cuts inside a clip), so heads and tails are the generator's own silence.
Series template (Real Slang): keep the beat ids and this structure; swap the three clips and the times below (hf/index.html uses the same).
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
HOOK = 0.0          # beat hook: hook card + the cap with a cross; Mimi brags
CLAIM = 0.25        # claim.wav: speech 0.47-3.14
GAG = 3.4           # beat gag: the Friend looks for a hat
HUH = 3.45          # huh.wav: speech 3.66-4.21
MEANING = 5.3       # beat meaning: the deck card (no cap / cap)
NOCAP = 5.4         # nocap.wav: speech 5.67-6.24
EXAMPLE = 6.75      # claim.wav again under the example row: speech 6.97-9.64
APP = 9.7           # beat app: My Notes → 単語帳 → スラング・カジュアル → ユニット3 → no cap → save
TAPS = (10.55, 11.45)   # スラング・カジュアル, ユニット3
SCROLL = 12.0
SAVE = 12.95        # the bookmark tapped
SAVED = 13.1
CTA = 14.1          # beat cta: 次のスラングは？コメントで
END = 15.9          # beat end: end card, CTA tap at END + 0.6
DUR = 17.4


def clip_lufs(path):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    return float(_j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))['input_i'])


# A gentle dialogue compressor per clip (as in films/mimi-decks-fine v3), then per-clip gain to one loudness, so the
# three takes sit level and the master limiter barely works.
RAW_VD = SRC / 'assets/own-voice'
VD = SRC / 'hf/assets/own-voice-comp'           # derived from the biometric WAVs: inside hf/assets/, not in Git
VD.mkdir(parents=True, exist_ok=True)
NAMES = ('claim', 'huh', 'nocap')
for n in NAMES:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(RAW_VD / f'{n}.wav'), '-af',
                    'acompressor=threshold=-30dB:ratio=3:attack=0.5:release=120:knee=6', str(VD / f'{n}.wav')], check=True)
L = {n: clip_lufs(VD / f'{n}.wav') for n in NAMES}
TARGET = -20.0                                  # LUFS per clip after makeup: the raw takes measure -19.5 (claim), -25.0 (huh), -21.2 (nocap)
G = {n: 0.9 * 10 ** ((TARGET - L[n]) / 20) for n in L}
print('clip loudness', {n: round(v, 1) for n, v in L.items()}, 'gains', {n: round(v, 3) for n, v in G.items()})

m = Mix(DUR, voice_dir=VD)
# hook: the cap pops with its cross, Mimi brags
m.sfx(pop_seq(1, 0.05, base=79), HOOK + 0.05)
m.voice('claim.wav', CLAIM, g=G['claim'])
# gag: the Friend pats his head, looking for the hat
m.sfx(whoosh(0.25, 0.2), GAG)
m.voice('huh.wav', HUH, g=G['huh'])
m.sfx(pofu() * 0.4, GAG + 1.1)
# meaning: card rows
m.sfx(whoosh(0.3, 0.3), MEANING)
m.voice('nocap.wav', NOCAP, g=G['nocap'])
m.sfx(pop_seq(1, 0.05, base=76), 6.6)
m.voice('claim.wav', EXAMPLE, g=G['claim'])
m.sfx(pop_seq(1, 0.05, base=76), 8.1)
m.sfx(pop_seq(1, 0.05, base=79), 8.9)
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
    '| app-beat RMS %.1f dBFS, claim RMS %.1f, nocap RMS %.1f, example RMS %.1f dBFS' % (
    bed + gain, rms(mix, 0.5, 3.1) + gain, rms(mix, 5.67, 6.24) + gain, rms(mix, 6.97, 9.64) + gain))
