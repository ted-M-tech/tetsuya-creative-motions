"""Can You Hear It? 1 - Can or Can't: sound -> hf/assets/mix.wav. Times from ../cues.json (the same sheet hf/index.html uses).

usage: uv run --no-project --with numpy python films/mimi-hear-can/source/scripts/mix.py
Both lines are the owner's own registered Lanclo voice, accent us (assets/own-voice/, not in Git: Drive
061. Can You Hear It 1 - Can or Cant/Hear1_Can_assets/own-voice/).
Series template: swap ANSWERS (which take plays as A / B) and the line clips; the beats stay hook -> play -> reveal -> rule -> ask -> end.
"""
import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, boing, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

C = json.loads((SRC / 'cues.json').read_text())
# Each take trimmed to its speech (measured: us-cant speech 0.32-1.40 s, us-can 0.22-0.98 s; heads/tails kept).
CLIP = {'us-cant': (0.28, 1.20), 'us-can': (0.18, 0.88)}
A, B = 'us-cant', 'us-can'   # the quiz order: A = "I can't swim.", B = "I can swim." (the answer to "which is can?" is B)


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
line(m, 'us-can', C['RL1'])
line(m, 'us-cant', C['RL2'])
m.sfx(pop_seq(2, 0.05, base=76), C['RULE_HIT'])
m.sfx(whoosh(0.3, 0.3), C['ask'])
m.sfx(pop_seq(3, 0.05, base=74), C['ask'] + 0.15)
m.bed(0.0, C['end'])
m.end_chord(C['end'])
m.sfx(pochi(), C['TAP'])
print(m.write(SRC / 'hf/assets/mix.wav'))
