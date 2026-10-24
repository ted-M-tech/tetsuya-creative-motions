"""Cloning: Shadowing, but in Your Own Voice — sound -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-cloning/source/scripts/mix.py
Every English line is the owner's registered voice (own-voice.json via kits/mimi-short/scripts/ownvoice.py,
assets/own-voice/, not in Git; Drive Cloning_assets/own-voice/). Speech spans below come from scripts/spans.py
(first/last 10 ms frame within 38 dB of the clip peak); every clip is placed whole, never cut.
"""
import json as _j
import re
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, mallet, pencil, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times. (v2: first half tightened from 18.7 s to 13.3 s)
HOOK = 0.0
H_MODEL = 0.1       # model (us) "Please leave the light on."  speech 0.11-1.61 -> 0.21-1.71
H_BEFORE = 0.35     # the Friend chasing it (learner)              speech 0.25-2.70 -> 0.60-3.05
BAD = 1.4           # ズレズレ…
VIDS = 2.4          # YouTube / Netflix, many times (the learner's tail runs under the card entry)
HARD = 3.5          # でも、難しかった…
R3 = 4.4            # 3: voice quality
LOW = 4.5           # low  "Leave the light on."  speech 0.27-2.06 -> 4.77-6.56
HIGH = 6.45         # high                        speech 0.18-1.07 -> 6.63-7.52
R2 = 7.6            # 2: rhythm
FAST1 = 7.7         # fast  speech 0.27-1.06 -> 7.97-8.76
FAST2 = 8.65        #                        -> 8.92-9.71 (the linked spelling appears)
R1 = 9.8            # 1: accent
US = 9.85           # us-short "I can't park the car."  speech 0.28-1.78 -> 10.13-11.63
UK = 11.45          # uk-short                          speech 0.21-1.84 -> 11.66-13.29
CONCL = 13.3        # finding a model that fits you is the hardest part
IDEA = 14.6         # AI can make voices now
IDEA2 = 15.9        # ...pronunciation practice?
NAME = 17.2         # SHADOWING
STRIKE = 17.55      # struck through
WRITE = 17.8        # rewritten into CLONING
ORIGIN = 19.3       # LANguage CLOning -> Lanclo
MERGE = 19.95
PROUD = 21.3        # 僕が勝手に名付けたんだ
RES = 23.0          # research card
BARS = 23.3
RATIO = 24.2        # 約1.3倍
WOW = 25.0          # すごい！
SURE = 26.6         # たしかに…
APP = 28.3
TAP = 29.1          # お手本 tapped
A_MODEL = 29.15     # model (us) speech -> 29.26-30.76
APP2 = 30.9         # これがクローニング
USE = 32.6          # 使ってみよう！
END = 34.0
CTA_TAP = 34.6
DUR = 35.6

m = Mix(DUR, voice_dir=SRC / 'assets/own-voice')
v = lambda name: f'{name}.wav'

# hook: the model runs ahead, the Friend lags behind
m.sfx(whoosh(0.3, 0.3), HOOK)
m.voice(v('model'), H_MODEL, g=0.8)
m.voice(v('before'), H_BEFORE, g=0.7)
m.sfx(boing(False), BAD)
# YouTube / Netflix cards pile up, then droop
m.sfx(whoosh(0.3, 0.3), VIDS - 0.05)
m.sfx(pop_seq(2, 0.2, base=72), VIDS + 0.1)
m.sfx(pofu() * 0.5, HARD)
# countdown 3 -> 2 -> 1
for at in (R3, R2, R1):
    m.sfx(whoosh(0.3, 0.3), at - 0.05)
    m.sfx(mallet(55, 0.6, 0.2), at + 0.02)
m.voice(v('low'), LOW, g=0.8)
m.voice(v('high'), HIGH, g=0.75)
m.voice(v('fast'), FAST1, g=0.85)
m.voice(v('fast'), FAST2, g=0.85)
m.voice(v('us-short'), US, g=0.8)
m.voice(v('uk-short'), UK, g=0.8)
m.sfx(pofu() * 0.5, CONCL)
# the idea: a soft low mallet pair, not a bell
m.sfx(whoosh(0.3, 0.3), IDEA - 0.05)
m.sfx(pop_seq(4, 0.12, base=67), IDEA + 0.2)
m.sfx(mallet(60, 0.7, 0.18), IDEA2)
m.sfx(mallet(67, 0.7, 0.16), IDEA2 + 0.09)
# SHADOWING -> CLONING: strike and rewrite, a short sting
m.sfx(whoosh(0.3, 0.3), NAME - 0.05)
m.sfx(pencil(0.25, 0.2), STRIKE)
m.sfx(pencil(0.35, 0.18), WRITE)
m.sfx(pop_seq(3, 0.06, base=72), WRITE + 0.4)
m.sfx(mallet(62, 0.9, 0.2), WRITE + 0.45)
m.sfx(mallet(69, 0.9, 0.16), WRITE + 0.5)
m.sfx(whoosh(0.25, 0.25), ORIGIN - 0.05)
m.sfx(pop_seq(2, 0.1, base=74), ORIGIN + 0.3)
m.sfx(mallet(65, 0.9, 0.2), MERGE + 0.25)
m.sfx(mallet(72, 0.9, 0.15), MERGE + 0.3)
m.sfx(pop_seq(2, 0.08, base=76), PROUD + 0.1)
# research card
m.sfx(whoosh(0.3, 0.3), RES - 0.05)
m.sfx(pop_seq(2, 0.35, base=67), BARS)
m.sfx(mallet(64, 0.8, 0.2), RATIO)
m.sfx(pop_seq(3, 0.05, base=74), WOW)
m.sfx(pofu() * 0.4, SURE)
# real app
m.sfx(whoosh(0.3, 0.3), APP - 0.05)
m.sfx(tap() * 0.6, TAP)
m.voice(v('model'), A_MODEL, g=0.85)
m.sfx(pop_seq(3, 0.05, base=76), APP2)
m.sfx(whoosh(0.3, 0.3), USE - 0.05)
m.sfx(pop_seq(4, 0.06, base=79), USE + 0.1)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
out = m.write(SRC / 'hf/assets/mix.wav')


# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true peak bound): measure, add the missing gain
# in front of a -2.4 dB limiter (the cuts' AAC lands at about -1.6 dBTP), and measure again. The balance between voice, SFX
# and bed is unchanged. (Same step as films/mimi-katakana-mcdonalds/source/scripts/mix.py.)
def lufs(f):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    d = _j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))
    return float(d['input_i']), float(d['input_tp'])


for _ in range(3):
    i, tp = lufs(out)
    if abs(i + 14) < 0.3:
        break
    tmp = out.with_suffix('.tmp.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(out), '-af',
                    f'volume={-14 - i + 0.1:.2f}dB,alimiter=limit=0.76:level=false:attack=1:release=60', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
