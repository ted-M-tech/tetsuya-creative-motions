"""Can You Hear It? 3 - Ship or Sheep: sound -> hf/assets/mix.wav. Times from ../cues.json (the same sheet hf/index.html uses).

usage: uv run --no-project --with numpy python films/mimi-hear-ship/source/scripts/mix.py
Both lines are the owner's own registered Lanclo voice, accent us (assets/own-voice/, not in Git: Drive
078. Can You Hear It 3 - Ship or Sheep/Hear3_Ship_assets/own-voice/). Template: films/mimi-hear-can (episode 1).
Series template: swap ANSWERS (which take plays as A / B) and the line clips; the beats stay hook -> play -> reveal -> rule -> ask -> end.
"""
import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())
# Each take trimmed to its speech at real silence (silencedetect -40 dB: us-ship speech 0.26-1.02 s, p release ~0.97;
# us-sheep 0.22-1.27 s, p release ~1.16; >= 40 ms pre-roll, heads / tails <= -38 dB vs the clip peak, see PROCESS.md).
CLIP = {'us-ship': (0.20, 0.92), 'us-sheep': (0.17, 1.20)}
A, B = 'us-sheep', 'us-ship'   # the quiz order: A = "I saw a sheep.", B = "I saw a ship." (the answer to "which is sheep?" is A)


def line(m, take, at):
    s, n = CLIP[take]
    m.voice(f'{take}.wav', at, g=1.0, start=s, length=n)


m = Mix(C['END'], voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(2, 0.06, base=72), 0.05)        # the A / B cards land (hook)
m.sfx(tap() * 0.5, C['play'] - 0.05)          # countdown 3
line(m, A, C['PA'])
m.sfx(tap() * 0.5, C['PB'] - 0.15)            # countdown 2
line(m, B, C['PB'])
m.sfx(tap() * 0.5, C['GUESS'] - 0.2)          # countdown 1
m.sfx(boing(True) * 0.6, C['GUESS'])          # the Friend's guess
m.sfx(whoosh(0.3, 0.3), C['reveal'])
m.sfx(pofu() * 0.7, C['RB'])                  # the answer flips over
m.sfx(boing(False) * 0.6, C['RB'] + 0.3)      # the Friend was wrong
m.sfx(whoosh(0.3, 0.3), C['rule'])
line(m, 'us-ship', C['RL1'])
line(m, 'us-sheep', C['RL2'])
m.sfx(pop_seq(2, 0.05, base=76), C['RULE_HIT'])
m.sfx(whoosh(0.3, 0.3), C['ask'])
m.sfx(pop_seq(3, 0.05, base=74), C['ask'] + 0.15)
m.bed(0.0, C['end'])
m.end_chord(C['end'])
m.sfx(pochi(), C['TAP'])
# the limiter below squeezes the voice peaks (about 2-3 dB); lower the bed and SFX by the same amount first so the
# voice / bed / SFX balance after the limiter matches the kit's (measured: 2026-10-23, see PROCESS.md)
m.m *= 10 ** (-3.0 / 20)
m.s *= 10 ** (-3.0 / 20)
out = m.write(SRC / 'hf/assets/mix.wav')
# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true peak bound): measure, add the missing gain
# in front of a 4x-oversampled limiter (true peak <= -1.5 dBTP), and measure again (as films/mimi-katakana-mcdonalds). The voice / SFX / bed balance is unchanged.
import re, shutil, subprocess  # noqa: E402


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
                    f'aresample=192000,volume={-14 - i + 0.1:.2f}dB,alimiter=limit=0.8:level=false:attack=1:release=60,aresample={SR}', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
