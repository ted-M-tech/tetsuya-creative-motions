"""I Stopped Shadowing Native Speakers sound -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-no-shadowing/source/scripts/mix.py
The native stranger: Kokoro (scripts/voices.sh, assets/voice/). Mimi and the model: the owner's registered voice
(own-voice.json via kits/mimi-short/scripts/ownvoice.py, assets/own-voice/, not in Git): before = learner, model and along = us.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
TOSS = 0.0          # the stranger's tape flies away (ポイッ)
BEFORE = 1.6
STRANGER = 1.75     # "Please leave the light on." (speech 0-1.22 s in the clip)
LEARNER = 1.95      # Mimi chasing it, learner accent (speech 0.26-2.69 s) -> 2.21-4.64
BAD = 3.4           # ズレズレ…
COPY = 5.6
APP = 6.6
TAP = 7.6           # お手本 tapped
MODEL_APP = 7.7     # the model plays in the app
AFTER = 10.6
MODEL = 10.75       # the model (speech 0.24-1.58 s) -> 10.99-12.33
ALONG = 10.95       # Mimi along, 0.2 s behind (speech 0.24-1.73 s) -> 11.19-12.68
GOOD = 12.3
CLOSE = 14.6
END = 15.9
CTA_TAP = 16.5
DUR = 17.2

m = Mix(DUR, voice_dir=SRC / 'assets/voice')
own = lambda name: f'../own-voice/{name}.wav'

m.sfx(whoosh(0.4, 0.4), TOSS)
m.sfx(pofu() * 0.5, TOSS + 0.15)
m.sfx(whoosh(0.3, 0.3), BEFORE - 0.05)
m.voice('light-am_michael.wav', STRANGER, g=0.8)
m.voice(own('before'), LEARNER, g=0.8)
m.sfx(boing(False), BAD)
m.sfx(whoosh(0.3, 0.3), COPY)
m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.1)
m.sfx(whoosh(0.3, 0.3), APP)
m.sfx(tap() * 0.6, TAP)
m.voice(own('model'), MODEL_APP, start=0.2)
m.sfx(whoosh(0.3, 0.3), AFTER - 0.05)
m.voice(own('model'), MODEL, g=0.7)
m.voice(own('along'), ALONG, g=0.7)
m.sfx(ding(), GOOD + 0.4)
m.sfx(pop_seq(4, 0.06, base=79), GOOD + 0.5)
m.sfx(whoosh(0.35, 0.35), CLOSE)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
