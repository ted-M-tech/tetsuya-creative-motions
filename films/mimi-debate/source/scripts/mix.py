"""Lost an argument in English: the English lines, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-debate/source/scripts/mix.py
The friend's question is Kokoro af_bella (assets/voice/, scripts/voices.sh; used twice). Mimi's rematch answer is the owner's own
registered Lanclo voice (assets/own-voice/, own-voice.json, kits/mimi-short/scripts/ownvoice.py; not in Git). Japanese lines are speech bubbles only (Kokoro's Japanese voice garbles them).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
ASK = 0.15             # "Dog person or cat person?"
UM = 1.45              # え、えっと……
DROOP = 2.0
COPY = 2.5
APP = 3.4
TAPS = (4.10, 5.05, 5.23, 6.58, 9.85, 10.88)
FEEDBACK = 6.63
OPPONENT = 7.83
REMATCH = 11.0
ASK2 = 11.1
ANSWER = 12.85
UM2 = 16.9
PUNCH = 17.55
END = 19.1
CTA_TAP = 19.7
DUR = 20.5

m = Mix(DUR, voice_dir=SRC / 'assets/voice')
m.voice('ask-af_bella.wav', ASK, g=0.9)
m.sfx(pop_seq(2, 0.06, base=72), UM)
m.sfx(pofu() * 0.7, DROOP)
m.sfx(whoosh(0.3, 0.3), COPY - 0.1)
m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.05)
m.sfx(whoosh(0.35, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(ding(), FEEDBACK + 0.05)
m.sfx(pop_seq(2, 0.06, base=74), OPPONENT)
m.sfx(boing(True), REMATCH)
m.voice('ask-af_bella.wav', ASK2, g=0.9)
m.voice('../own-voice/answer.wav', ANSWER - 0.09, g=0.95, start=0.2)   # the owner's voice: speech from 0.29 s in the clip, 'How about you?' 3.59-4.16 -> 16.15-16.72
m.sfx(pop_seq(4, 0.05, base=79), ANSWER)
m.sfx(pop_seq(2, 0.06, base=72), UM2)
m.sfx(pofu() * 0.6, PUNCH)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
