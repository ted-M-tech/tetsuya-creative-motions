"""Frozen Abroad sound: the staff lines (Pippa the duck, Kokoro af_nicole), Mimi's replies (the owner's registered voice), kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-frozen-abroad/source/scripts/mix.py
Staff voices: scripts/voices.sh (assets/voice/). Mimi's replies: own-voice.json via kits/mimi-short/scripts/ownvoice.py
(assets/own-voice/, not in Git). Everything Japanese is on screen only.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, freeze, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HAND = 0.45                      # the mitten shoots up out of the ice
SCENES = (1.6, 3.75, 5.6)        # airport, hotel, bus
FREEZES = (3.25, 5.05, 7.0)      # カチッ on the last word of each question
COPY = 7.5
APP = 8.5
TAPS = (9.4, 10.1, 11.1, 11.9, 13.0)   # 空港, the scene, meaning, hint, record
REPLY = 13.3                     # シチュエーション完了
PAYOFF = (14.3, 15.45, 16.95)    # Here you are. / Yes, I have a reservation. / Does this bus go to the station?
CLOSE = 18.7
END = 20.0
CTA_TAP = 20.6
DUR = 21.3

m = Mix(DUR, voice_dir=SRC / 'assets/voice')
own = lambda name: f'../own-voice/{name}.wav'      # relative to voice_dir

m.sfx(freeze(0.5), 0.0)
m.sfx(boing(True), HAND)
for at in SCENES:
    m.sfx(whoosh(0.3, 0.3), at - 0.05)
m.voice('passport-af_nicole.wav', 1.65)
m.voice('reservation-af_nicole.wav', 3.8, start=0.9)           # "Do you have a reservation?" (from 0.92 s in the clip)
m.voice('going-af_nicole.wav', 5.6)
for at in FREEZES:
    m.sfx(freeze(0.6), at)
    m.sfx(bell(96, 0.5, 0.1), at + 0.08)
m.sfx(whoosh(0.3, 0.3), COPY)
m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.1)
m.sfx(whoosh(0.3, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(ding(), REPLY)
m.sfx(whoosh(0.3, 0.3), PAYOFF[0] - 0.05)
m.voice(own('here'), PAYOFF[0] + 0.05, start=0.28)
m.voice(own('reservation'), PAYOFF[1] + 0.05, start=0.33)
m.voice(own('station'), PAYOFF[2] + 0.05, start=0.3)
m.sfx(pop_seq(4, 0.06, base=79), PAYOFF[2] + 1.4)
m.sfx(whoosh(0.35, 0.35), CLOSE)
m.sfx(pop_seq(5, 0.07, base=76), CLOSE + 0.3)
m.sfx(pofu() * 0.5, CLOSE + 0.05)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
