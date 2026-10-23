"""065「I'm fine, thank you. しか言えない」 sound: the Friend's two English lines in the owner's voice, kit SFX, the theme bed
-> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-decks-fine/source/scripts/mix.py
Mimi's "How's it going?" is a speech bubble only (one voice for both bunnies would sound like one person talking to himself).
Own voice (Gemini gemini-3.8-flash-tts via kits/mimi-short/scripts/ownvoice.py; WAVs not in Git, Drive Decks_ImFine_assets/own-voice/):
  fine.wav   "I'm fine, thank you. And you?"  robotic textbook style; speech 0.27-3.20 s (silencedetect -40 dB)
  casual.wav "All good! What's new?"          relaxed US; speech 0.21-1.59 s
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
ASK = 0.1          # Mimi's bubble "How's it going?"
FINE = 0.45        # fine.wav placed here: speech 0.72-3.65
YAWN = 3.8
APP = 5.5
TAPS = (6.7, 7.9, 10.25)   # スラング・カジュアル, ユニット4, the bookmark
SCROLL = 9.0
CARD = 10.0
SAVED = 10.7
RETRY = 12.2
ASK2 = 12.3
CASUAL = 12.75     # casual.wav: speech 12.96-14.34
FIVE = 14.9
END = 16.5
DUR = 18.0



def clip_lufs(path):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    return float(_j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))['input_i'])


# Level-match the two own-voice clips by per-clip gain (the louder one comes down to the quieter one), so neither needs
# the limiter: v2 had fine at -13.4 and casual at -9.9 LUFS in the film.
# Speech has a high crest factor (peaks about 15 dB over its RMS), so with the bed at BED_RMS the master limiter had to
# shave ~7 dB off the voice peaks. Instead each clip gets a gentle dialogue compressor (ratio 3, 0.5 ms attack, soft knee) before it is
# placed; the master limiter then only touches the loudest peak by at most GR_MAX.
RAW_VD = SRC / 'assets/own-voice'
VD = SRC / 'hf/assets/own-voice-comp'           # derived from the biometric WAVs: inside hf/assets/, not in Git
VD.mkdir(parents=True, exist_ok=True)
for n in ('fine', 'casual'):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(RAW_VD / f'{n}.wav'), '-af',
                    'acompressor=threshold=-30dB:ratio=3:attack=0.5:release=120:knee=6', str(VD / f'{n}.wav')], check=True)
L = {n: clip_lufs(VD / f'{n}.wav') for n in ('fine', 'casual')}
TARGET = min(clip_lufs(RAW_VD / f'{n}.wav') for n in L)   # the quieter raw clip's loudness (fine, about -21 LUFS)
G = {n: 0.9 * 10 ** ((TARGET - L[n]) / 20) for n in L}     # makeup per clip: both land at TARGET
print('clip loudness', {n: round(v, 1) for n, v in L.items()}, 'gains', {n: round(v, 3) for n, v in G.items()})

m = Mix(DUR, voice_dir=VD)
m.sfx(pop_seq(1, 0.05, base=79), ASK)
m.voice('fine.wav', FINE, g=G['fine'])
m.sfx(pofu() * 0.5, YAWN)
m.sfx(whoosh(0.35, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(whoosh(0.25, 0.2), SCROLL)
m.sfx(ding(), SAVED)
m.sfx(whoosh(0.3, 0.3), RETRY)
m.sfx(pop_seq(1, 0.05, base=79), ASK2)
m.voice('casual.wav', CASUAL, g=G['casual'])
m.sfx(tap() * 0.8, FIVE + 0.05)
m.sfx(pop_seq(3, 0.05, base=79), FIVE + 0.15)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)
# Static mix (same bus balance and ducking as Mix.write, but no dynamic loudnorm: its single pass lifted the voiceless
# app beat to about -14.5 LUFS). One gain for the whole film: -14 LUFS integrated, but never more than puts the
# un-ducked bed (the voiceless app beat) at BED_RMS; then a limiter keeps the true peak under -1.5 dBTP.
BED_RMS = -26.0  # dBFS RMS of the BGM-only stretch, as in the other films' bed
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


def rms_db(x, a, b):
    seg = x[int(a * SR):int(b * SR)]
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12)


# Commander review (2026-10-23): keep the bed quiet; reach -14 only if the bed stays at its cap. The voice lines have a high
# crest factor, so with the bed at BED_RMS the film lands near -17 LUFS integrated: the quieter result is kept on purpose.
raw = out.with_suffix('.raw.wav')
save(mix, raw)
i0, _ = lufs(raw)
bed = rms_db(mix, 6.0, 10.0)                       # the voiceless app beat (whooshes and taps included)
GR_MAX = 2.0                                       # limiter gain reduction allowed on the loudest peak (dB)
peak = 20 * np.log10(np.abs(mix).max())
gain = min(-14.0 - i0, BED_RMS - bed, 20 * np.log10(0.8) + GR_MAX - peak)
gr = max(0.0, peak + gain - 20 * np.log10(0.8))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af',
                f'volume={gain:.2f}dB,alimiter=limit=0.8:level=false:attack=1:release=60', '-ar', str(SR), str(out)], check=True)
raw.unlink()
i, tp = lufs(out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP; limiter GR max %.1f dB; gain %.1f dB (to -14: %.1f, bed cap: %.1f); app-beat RMS %.1f dBFS, voice RMS %.1f / %.1f dBFS' % (
    i, tp, gr, gain, -14.0 - i0, BED_RMS - bed, bed + gain, rms_db(mix, 0.75, 3.6) + gain, rms_db(mix, 12.95, 14.35) + gain))
