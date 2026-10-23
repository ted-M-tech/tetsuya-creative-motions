"""064 How Do You Say It? 2 - Otsukaresama: sound -> hf/assets/mix.wav (-14 LUFS, true peak <= -1.5 dBTP).

usage: uv run --no-project --with numpy python films/mimi-say-otsukare/source/scripts/mix.py
Voices: the owner's registered Lanclo voice (assets/own-voice/, not in Git; rebuild with kits/mimi-short/scripts/ownvoice.py + own-voice.json):
  friend-you-are-tired.wav  "You are tired!" (the Friend, learner)
  see-you-tomorrow.wav      "See you tomorrow!" (card row 1, us)
  thanks-for-today.wav      "Thanks for today!" (card row 2, us)
  good-work-today.wav       "Good work today!" (card row 3, us; the app's real candidate)
The beat ids and times are the same as hf/index.html.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, ding, freeze, pochi, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())   # the cue sheet, shared with hf/index.html (scripts/cues.py fills it in)
HOOK, LINE, PUZZLED, AMI, APP = 0.0, C['LINE'], C['PUZZLED'], C['AMI'], C['APP']
CARD, PAYOFF, END, DUR = C['CARD'], C['PAYOFF'], C['END'], C['DUR']

m = Mix(DUR, voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(2, 0.05, base=76), HOOK + 0.08)        # the hook line lands
m.voice('friend-you-are-tired.wav', LINE, g=1.0, start=0.22, length=1.45)
m.sfx(freeze(0.4) * 0.6, PUZZLED)                    # the air cools: that was not a greeting
m.sfx(boing(False), PUZZLED + 0.05)
m.sfx(whoosh(0.35, 0.3), APP - 0.08)
for at in C['TYPE']:
    m.sfx(tap() * 0.35, at)
m.sfx(tap() * 0.6, C['CREATE'])
m.sfx(pop_seq(2, 0.05, base=74), C['CHOICES'])
m.sfx(tap() * 0.6, C['PICK'])
m.sfx(pop_seq(3, 0.05, base=76), C['RESULT'])
m.sfx(tap() * 0.6, C['SAVE'])
m.sfx(ding(0.1), C['SAVE'] + 0.25)
m.sfx(whoosh(0.3, 0.3), CARD - 0.05)
for i, (row, clip, start, length) in enumerate([('ROW1', 'see-you-tomorrow.wav', 0.15, 0.9), ('ROW2', 'thanks-for-today.wav', 0.22, 0.9),
                                                 ('ROW3', 'good-work-today.wav', 0.22, 1.1)]):
    m.sfx(pop_seq(2, 0.05, base=72 + 2 * i), C[row] - 0.15)
    m.voice(clip, C[row], g=1.0, start=start, length=length)
m.sfx(whoosh(0.3, 0.3), PAYOFF - 0.05)
m.sfx(boing(True), PAYOFF + 0.1)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)
out = SRC / 'hf/assets/mix.wav'
m.write(out)


# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true peak bound): measure, add the missing gain
# in front of a limiter (-2.4 dBFS sample peak, so the true peak stays <= -1.5 dBTP), and measure again. The balance between voice, SFX and bed is unchanged
# (the same step as films/mimi-katakana-mcdonalds/source/scripts/mix.py).
def lufs(f):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    d = json.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))
    return float(d['input_i']), float(d['input_tp'])


for _ in range(4):
    i, tp = lufs(out)
    if abs(i + 14) < 0.3 and tp <= -1.5:
        break
    tmp = out.with_suffix('.tmp.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(out), '-af',
                    f'volume={-14 - i + 0.1:.2f}dB,alimiter=limit=0.76:level=false:attack=1:release=60', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
