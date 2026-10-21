"""Café roleplay (frozen at the counter) sound: the English lines, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-roleplay/source/scripts/mix.py
Voices: the barista and Mimi speak English (Kokoro, scripts/voices.sh); everything Japanese is on screen only.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, freeze, pochi, pofu, pop_seq, shatter, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
ASK1 = 0.3             # "For here, or to go?"
FREEZE1 = 1.95         # Mimi freezes solid (カチッ)
COPY = 3.3             # copy card
APP = 4.3              # the app on the phone
TAPS = (4.65, 5.25, 6.8, 7.8, 9.0)   # café, the scene, meaning, hint, record
REPLY = 9.45           # the partner's reply, シチュエーション完了
ORDER = 10.75          # back at the counter: "For here, please. I'd like a latte!"
ASK2 = 13.0            # "Would you like it hot, or iced?"
FREEZE2 = 14.5         # frozen again
SHATTER = 15.2         # she breaks out grinning
COPY2 = 15.55          # いろんな場面で、何度でも。
END = 16.85
CTA_TAP = 17.4
DUR = 18.0

m = Mix(DUR, voice_dir=SRC / 'assets/voice')
m.voice('here-bf_emma.wav', ASK1)
m.sfx(freeze(0.7), FREEZE1)
m.sfx(bell(96, 0.5, 0.1), FREEZE1 + 0.08)          # the カチッ
m.sfx(whoosh(0.3, 0.3), COPY)
m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.1)
m.sfx(whoosh(0.3, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(ding(), REPLY)
m.sfx(whoosh(0.3, 0.3), ORDER - 0.15)
m.voice('order-af_heart.wav', ORDER)
m.sfx(pop_seq(4, 0.06, base=79), ORDER + 2.0)       # served, sparkle
m.voice('hot-bf_emma.wav', ASK2)
m.sfx(freeze(0.7), FREEZE2)
m.sfx(bell(96, 0.5, 0.1), FREEZE2 + 0.08)
m.sfx(shatter(), SHATTER)
m.sfx(boing(True), SHATTER + 0.1)
m.sfx(whoosh(0.35, 0.35), COPY2)
m.sfx(pop_seq(5, 0.07, base=76), COPY2 + 0.3)
m.sfx(pofu() * 0.5, COPY2 + 0.05)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
