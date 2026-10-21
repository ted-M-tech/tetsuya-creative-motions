"""Swipe review sound: soft SFX, the theme bed, the CTA pochi -> hf/assets/mix.wav. No voices (speech bubbles only).

usage: uv run --no-project --with numpy python films/mimi-swipe/source/scripts/mix.py
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, clang, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
FLICKS = (0.15, 0.45, 0.75)         # hook: cards flick off Mimi's phone
TEASE = 0.95                       # the friend: マッチングアプリじゃん！
DENY = 2.3                         # Mimi: ちがうって！
COPY = 3.9                         # 英語の復習も、スワイプで。
DRAGS = (5.16, 6.92, 8.33, 9.55)   # the real app: right, left, right, up (scripts/app_track.sh)
FLY = (6.28, 7.88, 8.93, 10.51)     # each card is let go
DATE = 14.25                       # じゃあ、デートしてくる！
CURVE = 11.95                      # 忘れかけたころに、また出てくる。 (forgetting-curve card)
CURVE_DOTS = (12.47, 12.71, 13.11, 13.75) # review dots pop on the curve
TSUKKOMI = 15.75                   # そっちもやってるんかい！
END = 16.85
CTA_TAP = END + 0.45

m = Mix(17.95)
for at in FLICKS:
    m.sfx(whoosh(0.22, 0.16), at)
m.sfx(pofu() * 0.45, TEASE)
m.sfx(pofu() * 0.5, DENY)
m.sfx(tap() * 0.5, DENY + 0.08)
m.sfx(pop_seq(3, 0.05, base=76), COPY)
for at in DRAGS:
    m.sfx(tap() * 0.35, at)
for at in FLY:
    m.sfx(whoosh(0.3, 0.22), at)
m.sfx(pop_seq(2, 0.05, base=76), CURVE)
for i, at in enumerate(CURVE_DOTS):
    m.sfx(bell(79 + 2 * i, 0.4, 0.035), at)
m.sfx(bell(84, 0.6, 0.05), DATE + 0.1)
m.sfx(clang(0.2), TSUKKOMI)
m.sfx(pofu() * 0.4, TSUKKOMI + 0.05)
m.sfx(whoosh(0.35, 0.2), TSUKKOMI + 0.6)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
