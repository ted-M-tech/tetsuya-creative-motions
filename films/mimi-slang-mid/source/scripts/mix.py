"""071 Real Slang 4「"It's mid"って褒められてる？」 sound: three own-voice English clips, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-slang-mid/source/scripts/mix.py
Own voice (Gemini gemini-3.8-flash-tts via kits/mimi-short/scripts/ownvoice.py; WAVs not in Git, Drive Slang4_Mid_assets/own-voice/):
  verdict.wav "It's... mid."   Mimi, after tasting; speech 0.35-1.03 ("It's...") and 2.01-2.98 ("mid") (silencedetect -40 dB).
                               The 0.98 s pause is shortened by splitting the take inside that silence (at 1.25 and 1.85 s,
                               >= 160 ms from either word), never inside a word; head/tail of every placed piece checked <= -38 dB.
  thanks.wav  "Mid? Thanks!"   the Friend, taking it as praise
  mid.wav     "Mid."           the term alone, for the meaning card
thanks.wav and mid.wav are placed whole. Lines missing on disk (quota) are skipped so the edit still builds.
Template: films/mimi-slang-no-cap/source/scripts/mix.py (same structure and master).
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
HOOK = 0.0          # beat hook: hook card; the Friend serves, Mimi chews
VERDICT_A = 0.5     # verdict.wav 0-1.25 s ("It's...": speech 0.85-1.53)
VERDICT_B = 1.75    # verdict.wav 1.85 s-end ("mid": speech 1.91-2.88)
GAG = 3.2           # beat gag: the Friend takes it as praise
THANKS = 3.15       # thanks.wav
MEANING = 5.0       # beat meaning: the deck card; the Friend deflates
MID = 5.0           # mid.wav
SAD = 6.3           # 褒めてなかった… bubble
APP = 8.4           # beat app: My Notes → 単語帳 → スラング・カジュアル → ユニット2 → mid → save
TAPS = (9.25, 10.15)   # スラング・カジュアル, ユニット2
SCROLL = 10.7
SAVE = 11.65        # the bookmark tapped
SAVED = 11.8
CTA = 12.8          # beat cta: 次のスラングは？コメントで
END = 14.4          # beat end: end card, CTA tap at END + 0.6
DUR = 15.9


def clip_lufs(path):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    return float(_j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))['input_i'])


# A gentle dialogue compressor per clip (as in films/mimi-decks-fine v3), then per-clip gain to one loudness, so the
# three takes sit level and the master limiter barely works.
RAW_VD = SRC / 'assets/own-voice'
VD = SRC / 'hf/assets/own-voice-comp'           # derived from the biometric WAVs: inside hf/assets/, not in Git
VD.mkdir(parents=True, exist_ok=True)
NAMES = tuple(n for n in ('verdict', 'thanks', 'mid') if (RAW_VD / f'{n}.wav').exists())
print('own-voice lines present:', NAMES)
for n in NAMES:
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(RAW_VD / f'{n}.wav'), '-af',
                    'acompressor=threshold=-30dB:ratio=3:attack=0.5:release=120:knee=6', str(VD / f'{n}.wav')], check=True)
L = {n: clip_lufs(VD / f'{n}.wav') for n in NAMES}
TARGET = -20.0                                  # LUFS per clip after makeup
G = {n: 0.9 * 10 ** ((TARGET - L[n]) / 20) for n in L}
# verdict: two pieces split inside the long pause (real silence), each checked at head and tail
def edge_db(path):
    import wave
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float).reshape(-1, w.getnchannels())[:, 0]
        n = int(0.01 * w.getframerate())
    pk = np.abs(x).max() + 1e-9
    f = lambda seg: 20 * np.log10(np.sqrt(np.mean(seg ** 2)) / pk + 1e-12)
    return f(x[:n]), f(x[-n:])


for piece, a, b in (('verdict-a', 0.0, 1.25), ('verdict-b', 1.85, None)):
    trim = f'atrim=start={a}' + (f':end={b}' if b else '')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(VD / 'verdict.wav'), '-af', trim + ',asetpts=PTS-STARTPTS', str(VD / f'{piece}.wav')], check=True)
    h, t = edge_db(VD / f'{piece}.wav')
    print(piece, 'head %.1f dB tail %.1f dB vs peak' % (h, t))
    assert h <= -38 and t <= -38, piece
print('clip loudness', {n: round(v, 1) for n, v in L.items()}, 'gains', {n: round(v, 3) for n, v in G.items()})

m = Mix(DUR, voice_dir=VD)
# hook: the hook card pops, Mimi chews and gives the verdict
m.sfx(pop_seq(1, 0.05, base=79), HOOK + 0.05)
m.voice('verdict-a.wav', VERDICT_A, g=G['verdict'])
m.voice('verdict-b.wav', VERDICT_B, g=G['verdict'])
# gag: the Friend is delighted
m.sfx(whoosh(0.25, 0.2), GAG)
if 'thanks' in G:
    m.voice('thanks.wav', THANKS, g=G['thanks'])
# meaning: card rows, the Friend deflates
m.sfx(whoosh(0.3, 0.3), MEANING)
if 'mid' in G:
    m.voice('mid.wav', MID, g=G['mid'])
m.sfx(pop_seq(1, 0.05, base=76), 5.45)
m.sfx(pofu() * 0.4, 5.7)
m.sfx(pop_seq(1, 0.05, base=72), SAD)
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
    '| app-beat RMS %.1f dBFS, verdict RMS %.1f dBFS' % (bed + gain, rms(mix, 0.85, 2.88) + gain))
