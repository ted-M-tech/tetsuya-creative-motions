"""Can You Hear It? 2 - Excuse Me: sound -> hf/assets/mix.wav. Times from ../cues.json (the same sheet hf/index.html uses).

usage: uv run --no-project --with numpy python films/mimi-hear-excuse/source/scripts/mix.py
All three takes are the owner's own registered Lanclo voice, accent us with a style per intonation (assets/own-voice/, not in Git:
Drive 062. Can You Hear It 2 - Excuse Me/Hear2_ExcuseMe_assets/own-voice/).
Series template: swap the takes and their CLIP trims; the beats stay hook -> play -> reveal -> rule -> ask -> end.
"""
import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, boing, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())
# Each take trimmed to its speech (silencedetect -45 dB: A 0.16-1.07 s, B 0.24-0.87 s, C 0.20-1.54 s; heads/tails kept).
CLIP = {'us-a-fall': (0.12, 1.00), 'us-b-rise': (0.19, 0.75), 'us-c-offended': (0.15, 1.42)}
A, B, CC = 'us-a-fall', 'us-b-rise', 'us-c-offended'   # A = falling, B = rising (pardon?), C = sharp rise on ME (offended: the answer)


def line(m, take, at):
    s, n = CLIP[take]
    m.voice(f'{take}.wav', at, g=1.0, start=s, length=n)


m = Mix(C['END'], voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(3, 0.06, base=72), 0.05)        # the A / B / C cards land (hook)
m.sfx(tap() * 0.5, C['play'] - 0.05)          # countdown 3
line(m, A, C['PA'])
m.sfx(tap() * 0.5, C['PB'] - 0.15)            # countdown 2
line(m, B, C['PB'])
m.sfx(tap() * 0.5, C['PC'] - 0.15)            # countdown 1
line(m, CC, C['PC'])
m.sfx(boing(True) * 0.6, C['GUESS'])          # the Friend's guess
m.sfx(whoosh(0.3, 0.3), C['reveal'])
m.sfx(pofu() * 0.7, C['RC'])                  # the answer flips over
m.sfx(boing(False) * 0.6, C['RC'] + 0.3)      # the Friend was wrong
m.sfx(whoosh(0.25, 0.3), C['TURN'])           # Mimi turns away (hmph)
m.sfx(whoosh(0.3, 0.3), C['rule'])
line(m, A, C['RL1'])
line(m, B, C['RL2'])
line(m, CC, C['RL3'])
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
