"""Mimi eats your files: kit SFX, the phrase on the review card, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-import/source/scripts/mix.py
Japanese lines are speech bubbles only (Kokoro's Japanese voice garbles them). The one English line is the first imported phrase on the
review card: the model in the owner's own registered Lanclo voice (accent us; own-voice.json, kits/mimi-short/scripts/ownvoice.py).
"""
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, lowpass, pochi, pofu, pop_seq, t, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
CARDS = (0.3, 0.55, 0.8)      # the three scattered lists pop up
MIMI = 2.6                     # Mimi pops in
MERGE = 3.35                   # the lists fly together into one CSV file
EAT = 5.6                      # the file goes into her mouth
CHEWS = (5.8, 6.1, 6.4, 6.7, 7.0)
APP = 4.0                      # the app: the import sheet
EAT_IN = 5.3                   # cut to the munch
APP2 = 7.5                     # the app again
TAPS = (5.05, 8.6, 10.6)       # CSVファイルを選ぶ, 12件を追加, the 旅行 folder
DONE = 8.8                     # 12件を追加しました。
PHRASE = 11.95                 # the model voice on the review card
COPY = 13.3
CLOSE = 15.25
END = 16.0
LENGTH = 17.4


def munch(seed=0):
    """A soft paper crunch: a short filtered noise burst with a little grain."""
    tt = t(0.12)
    x = np.random.default_rng(seed).standard_normal(len(tt))
    x = lowpass(x, 0.25) * (1 + 0.6 * np.sign(np.sin(2 * np.pi * 38 * tt)))
    return 0.3 * x * np.exp(-28 * tt) * np.minimum(1, tt / 0.004)


def build():
    m = Mix(LENGTH, voice_dir=SRC / 'assets/voice')
    for i, at in enumerate(CARDS):
        m.sfx(pop_seq(1, 0.05, base=76 + 3 * i), at)
    m.sfx(boing(True), MIMI)
    m.sfx(whoosh(0.35, 0.3), MERGE)
    m.sfx(pop_seq(2, 0.06, base=84), MERGE + 0.4)
    m.sfx(boing(False), EAT)
    for at in CHEWS:
        m.sfx(munch(int(at * 10)), at)
    m.sfx(whoosh(0.35, 0.3), APP)
    m.sfx(whoosh(0.3, 0.3), EAT_IN)
    m.sfx(whoosh(0.35, 0.3), APP2)
    for at in TAPS:
        m.sfx(tap() * 0.6, at)
    m.sfx(ding(), DONE)
    m.sfx(bell(88, 0.7, 0.08), DONE + 0.1)
    m.voice('../own-voice/model.wav', PHRASE - 0.06, g=0.9, start=0.15)   # the owner's voice: speech 0.21-1.09 s in the clip -> 11.95-12.83
    m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.05)
    m.sfx(pofu() * 0.6, CLOSE)
    m.bed(0.0, END)
    m.end_chord(END)
    m.sfx(pochi(), END + 0.6)
    print(m.write(SRC / 'hf/assets/mix.wav'))


if __name__ == '__main__':
    build()
