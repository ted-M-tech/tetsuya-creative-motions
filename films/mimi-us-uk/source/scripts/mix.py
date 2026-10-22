"""US vs UK quiz: the same sentence in the owner's own registered Lanclo voice, British (A) and American (B), kit SFX,
the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-us-uk/source/scripts/mix.py
Voices: "I can't park the car by the water." with the ownvoice.py `uk` and `us` presets (Gemini gemini-3.8-flash-tts) —
made by kits/mimi-short/scripts/ownvoice.py source/own-voice.json into source/assets/own-voice/ (not in Git: biometric;
kept in Drive US_UK_assets/own-voice/). Japanese lines are speech bubbles only.
Measured (silencedetect -40 dB; mlx-whisper large-v3-turbo word timestamps):
  take-uk speech 0.21-2.61 s, words can't 0.40, park 0.78, car 1.28, water 2.04
  take-us speech 0.26-2.15 s
  Rhoticity check (praat-parselmouth, median F3): uk park 3015 / car 2867 Hz (no r colouring), us park 1972 / car 2469 Hz
  (r-coloured); can't F2 uk 1223 Hz (back, broad a) vs us 1410 Hz. UK take accepted on the first generation.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
QUIZ = 1.5             # 「イギリス英語はどっち？」
A = 2.0                # take-uk, trimmed 0.15 s: speech 2.06-4.46
B = 4.75               # take-us, trimmed 0.2 s: speech 4.81-6.70
COUNT = (6.95, 7.35, 7.75)
GUESS = 7.05           # friend: 「Bでしょ！」
REVEAL = 8.2           # 正解は A
OOPS = 8.55
REPLAY = 9.0           # take-uk again, trimmed 0.15 s: can't 9.25, park 9.63, car 10.13, water 10.89, end 11.46
APP = 11.8             # the app, 4.0 s
TAP = 12.15            # 落ち着いて
TYPING = [12.8 + 0.2 * i for i in range(9)]
CREATE = 14.6          # 試聴音声を作る pulses (never pressed)
PUNCH = 15.8
END = 17.5
CTA_TAP = 18.1
DUR = 18.9

m = Mix(DUR, voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(2, 0.06, base=76), 0.02)
m.sfx(whoosh(0.3, 0.3), QUIZ - 0.05)
m.sfx(pop_seq(3, 0.05, base=79), QUIZ + 0.05)
m.voice('take-uk.wav', A, g=0.9, start=0.15)
m.voice('take-us.wav', B, g=0.9, start=0.2)
for i, at in enumerate(COUNT):
    m.sfx(tap() * 0.7, at)
m.sfx(boing(True) * 0.5, GUESS)
m.sfx(bell(88, 0.9, 0.1), REVEAL)
m.sfx(bell(93, 0.9, 0.08), REVEAL + 0.08)
m.sfx(boing(False) * 0.5, OOPS)
m.voice('take-uk.wav', REPLAY, g=0.9, start=0.15)
m.sfx(whoosh(0.35, 0.3), APP)
m.sfx(tap() * 0.6, TAP)
for at in TYPING:
    m.sfx(tap() * 0.25, at)
m.sfx(ding(), CREATE)
m.sfx(pofu() * 0.7, PUNCH)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
