"""I fed my flashcards to Mimi: kit SFX, the model on the review card, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-flashcards/source/scripts/mix.py
Japanese lines are speech bubbles only. The one English line is the first card the app showed in review, "look forward to":
the model in the owner's own registered Lanclo voice (Gemini gemini-3.8-flash-tts, accent us; own-voice.json,
kits/mimi-short/scripts/ownvoice.py; WAV not in Git, kept in Drive Flashcards_assets/own-voice/).
Measured (silencedetect -40 dB): model speech 0.28-1.15 s; whisper: "Look forward to."
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, ding, lowpass, pochi, pofu, pop_seq, t, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK_CARDS = [0.2 * i for i in range(7)]   # flashcards into the mouth
S1, S2, S3 = 1.7, 3.9, 7.4                  # the three steps
S1_TAPS = (S1 + 0.45, S1 + 1.0, S1 + 1.65)  # ••• -> 書き出し -> CSV
S2_EDITS = (S2 + 0.75, S2 + 1.35, S2 + 2.0)  # term, meaning, tags
FILE = S3 + 0.8                              # 単語帳.csv pops out
APP1 = 8.6
TAPS = (9.65, 13.2, 15.2)                    # CSVファイルを選ぶ, 10件を追加, the 単語帳 folder
EAT = 9.9
APP2 = 12.1
DONE = 13.4
MODEL = 16.6                                 # model voice, trimmed 0.15 s: speech 16.73-17.60
CLOSE = 18.2
END = 19.7
LENGTH = 21.1


def munch(seed=0):
    """A soft paper crunch: a short filtered noise burst with a little grain."""
    tt = t(0.12)
    x = np.random.default_rng(seed).standard_normal(len(tt))
    x = lowpass(x, 0.25) * (1 + 0.6 * np.sign(np.sin(2 * np.pi * 38 * tt)))
    return 0.3 * x * np.exp(-28 * tt) * np.minimum(1, tt / 0.004)


m = Mix(LENGTH, voice_dir=SRC / 'assets/own-voice')
for i, at in enumerate(HOOK_CARDS):
    m.sfx(munch(i) * 0.8, at + 0.3)
m.sfx(whoosh(0.3, 0.3), S1)
for at in S1_TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(whoosh(0.3, 0.3), S2)
for at in S2_EDITS:
    m.sfx(pop_seq(1, 0.05, base=81), at)
m.sfx(pop_seq(2, 0.05, base=79), S3)
m.sfx(pofu() * 0.7, FILE)
m.sfx(whoosh(0.35, 0.3), APP1)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
for i, at in enumerate(np.arange(EAT + 0.35, EAT + 2.0, 0.3)):
    m.sfx(munch(10 + i), at)
m.sfx(whoosh(0.35, 0.3), APP2)
m.sfx(ding(), DONE)
m.voice('model.wav', MODEL, g=0.9, start=0.15)
m.sfx(pop_seq(3, 0.05, base=79), CLOSE)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)
print(m.write(SRC / 'hf/assets/mix.wav'))
