"""「道を聞かれて固まる」 sound: Kokoro voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-michi/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh): the passer-by (bm_george) asks the way and says thanks;
Mimi's "Uh... uh..." and the answer (af_heart; the answer stands in for her own voice with native pronunciation).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, ding, freeze, pochi, poof, shatter, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
ASK = 0.05                 # "Excuse me, how do I get to the station?" (x1.25, about 2.2 s)
ICE = 0.35                 # the ice forms while the question is still going
UH = 2.25                  # "Uh..." from inside the ice
DESK = 2.9                 # cut to the desk
TAP = 3.33
MODEL = 3.75               # her own voice gives the answer
PERK = 5.4
RESULT = 6.0
SAY = 8.2                  # practice
THAW = 10.1                # back on the street: the ice shatters
ANSWER = 11.35             # gives the directions
THANKS = 13.05
END = 14.0

m = Mix(15.0, voice_dir=SRC / 'assets/voice')
m.voice('ask-bm_george.wav', ASK, g=0.8, speed=1.25)
m.sfx(freeze(), ICE)
m.voice('uh-af_heart.wav', UH, g=0.7, length=0.6, muffle=True)
m.sfx(whoosh(0.25, 0.25), DESK - 0.12)
m.sfx(tap(), TAP)
m.voice('answer-af_heart.wav', MODEL)
for i, n in enumerate([86, 90, 93, 98]):
    m.sfx(bell(n, 1.0, 0.07), PERK + i * 0.06)
m.sfx(whoosh(0.25, 0.25), RESULT)
for i in range(5):
    m.sfx(tap() * 0.35, RESULT + 0.15 + i * 0.07)
m.sfx(ding(0.12), RESULT + 0.75)
m.voice('answer-af_heart.wav', SAY - 0.03, g=0.5)     # the model, under her
m.voice('answer-af_heart.wav', SAY, g=0.85)
m.sfx(shatter(), THAW)
m.sfx(poof() * 0.5, THAW + 0.05)
m.voice('answer-af_heart.wav', ANSWER)
m.voice('thanks-bm_george.wav', THANKS, g=0.8)
m.sfx(ding(), THANKS + 0.5)
m.bed(DESK, END, joy_from=PERK)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)  # the end card button gets tapped (kit.tapCta)
print(m.write(SRC / 'hf/assets/mix.wav'))
