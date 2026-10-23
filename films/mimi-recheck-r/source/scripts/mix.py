"""066 「治ったはずのRが…」 (The R Came Back) sound -> hf/assets/mix.wav. Cue times are shared with hf/index.html.

usage: uv run --no-project --with numpy python films/mimi-recheck-r/source/scripts/mix.py
The Friend's lines are the owner's own registered voice (assets/own-voice/, not in Git: Drive
066. The R Came Back/Recheck_R_assets/own-voice/): us-right "That's right!" (us), learner-light "That's light!" (learner style).
Horror parody, light and cute: a soft low sting and a quiet "ooh" pad instead of scary hits; the bed drops out in the dark beats.
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, mallet, pad, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds), same as hf/index.html
FL, V1, CONF, SK, SL, V2, GH, MI, A, ZOOM, LBL, LINE, X, V3, BYE, E, END = (
    2.3, 2.42, 3.05, 5.0, 6.1, 6.2, 6.95, 7.85, 9.1, 10.2, 10.55, 11.3, 14.0, 14.1, 14.95, 16.3, 17.6)

m = Mix(END, voice_dir=SRC / 'assets/own-voice')
# Hook: a soft low sting and a quiet minor "ooh" while the L creeps up
m.sfx(mallet(40, 1.4, 0.35), 0.02)
m.sfx(pad([52, 55, 59], 2.2, 0.25), 0.05)
m.sfx(whoosh(0.6, 0.25), 0.9)
# Flashback: the Friend nails "right", confetti, Mimi cheers
m.sfx(whoosh(0.3, 0.3), FL - 0.1)
m.voice('us-right.wav', V1, g=1.0, start=0.28)        # "right" at V1 + 0.32
m.sfx(pop_seq(4, 0.05, base=76), CONF)
m.sfx(boing(True), CONF + 0.25)
# Some time later (soft clock ticks)
for i in range(4):
    m.sfx(tap() * 0.35, SK + 0.15 + i * 0.22)
# The slip comes back: "That's light!", the L rises again ("ただいま〜"), Mimi with her flashlight
m.voice('learner-light.wav', V2, g=1.0, start=0.22)   # "light" at V2 + 0.49
m.sfx(whoosh(0.7, 0.3), GH)
m.sfx(pad([50, 53, 57], 1.4, 0.3), GH)
m.sfx(boing(False), GH + 0.6)
m.sfx(boing(True), MI)
# The real app
m.sfx(whoosh(0.3, 0.3), A)
m.sfx(pofu() * 0.5, LBL)
m.sfx(pop_seq(2, 0.05, base=79), LINE)
# Payoff: said right again, the L waves bye
m.sfx(whoosh(0.3, 0.3), X - 0.1)
m.voice('us-right.wav', V3, g=1.0, start=0.28)
m.sfx(pop_seq(3, 0.05, base=76), V3 + 0.6)
m.sfx(whoosh(0.5, 0.2), BYE + 0.3)
m.bed(0.0, E)
# the bed is out in the dark beats (hook, "some time later", the slip) and comes in with the bright ones
tt = np.arange(m.n) / SR
m.m *= np.interp(tt, [0, FL - 0.05, FL + 0.2, SK - 0.1, SK, MI, MI + 0.3, END], [0, 0, 1, 1, 0, 0, 1, 1])
m.end_chord(E)
m.sfx(pochi(), E + 0.6)
out = m.write(SRC / 'hf/assets/mix.wav')
# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true peak bound): measure, add the missing gain
# in front of a limiter at -2 dBFS (true peak stays under -1.5 dBTP), and measure again. The balance between voice, SFX and bed is unchanged
# (same step as films/mimi-katakana-mcdonalds).
import json as _j, re, shutil, subprocess  # noqa: E402


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
                    f'volume={-14 - i + 0.1:.2f}dB,alimiter=limit=0.79:level=false:attack=1:release=60', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
