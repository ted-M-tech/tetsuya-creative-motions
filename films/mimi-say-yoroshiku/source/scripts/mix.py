"""063 How Do You Say It? 1 - Yoroshiku Onegaishimasu: sound -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-say-yoroshiku/source/scripts/mix.py
Voices: the owner's registered Lanclo voice (assets/own-voice/, not in Git; rebuild with kits/mimi-short/scripts/ownvoice.py + own-voice.json):
  friend-please-yoroshiku.wav  "Please... yoroshiku?" (the Friend; used in two pieces, the long pause trimmed)
  nice-to-meet-you.wav         "Nice to meet you." (situation card, row 1, us)
  look-forward-working.wav     "I look forward to working with you." (row 2, us; the app's real answer)
Series: episode 2 copies this file and swaps the cue times and the clips; the beat ids are the same as hf/index.html.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, boing, ding, freeze, pochi, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = 0.0           # frame 1: the hook line, the Friend frozen mid-bow
LINE_A = 1.55        # "Please..."
LINE_B = 2.35        # "yoroshiku?"
PUZZLED = 3.95       # Mimi (the colleague) puzzled
APP = 5.0            # the real app: the phrase composer
TYPE = (5.7, 6.3, 7.25)   # the three typed chunks
CREATE = 7.65        # フレーズを作成
RESULT = 8.45        # the real result
SAVE = 10.35         # 保存
CARD = 11.35         # Mimi's situation card
ROW1 = 11.75         # 初対面: "Nice to meet you."
ROW2 = 13.25         # 一緒に働く: "I look forward to working with you."
PAYOFF = 15.55       # back at the office: the Friend says it with a smile
END = 17.35
CTA_TAP = END + 0.6
DUR = 18.6

m = Mix(DUR, voice_dir=SRC / 'assets/own-voice')
m.sfx(freeze(0.4), HOOK + 0.02)                     # the air freezes mid-bow
m.sfx(pop_seq(2, 0.05, base=76), HOOK + 0.08)       # the hook line lands
# "Please..." (clip 0.85-1.58 s), then "yoroshiku?" (clip 2.62-4.25 s): the hesitation pause shortened to ~0.1 s
m.voice('friend-please-yoroshiku.wav', LINE_A, g=1.0, start=0.85, length=0.73)
m.voice('friend-please-yoroshiku.wav', LINE_B, g=1.0, start=2.62, length=1.63)
m.sfx(boing(False), PUZZLED)
m.sfx(whoosh(0.35, 0.3), APP - 0.08)
for at in TYPE:
    m.sfx(tap() * 0.35, at)
m.sfx(tap() * 0.6, CREATE)
m.sfx(pop_seq(3, 0.05, base=76), RESULT)
m.sfx(tap() * 0.6, SAVE)
m.sfx(ding(0.1), SAVE + 0.25)
m.sfx(whoosh(0.3, 0.3), CARD - 0.05)
m.sfx(pop_seq(2, 0.05, base=72), ROW1 - 0.15)
m.voice('nice-to-meet-you.wav', ROW1, g=1.0, start=0.25, length=0.95)
m.sfx(pop_seq(2, 0.05, base=74), ROW2 - 0.15)
m.voice('look-forward-working.wav', ROW2, g=1.0, start=0.2, length=1.65)
m.sfx(whoosh(0.3, 0.3), PAYOFF - 0.05)
m.sfx(boing(True), PAYOFF + 0.1)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
m.write(SRC / 'hf/assets/mix.wav')
