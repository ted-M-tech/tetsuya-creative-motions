"""「道を聞かれて固まる」 sound: voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-michi/source/scripts/mix.py
The passer-by (Kokoro bm_george, assets/voice/, rebuild with scripts/voices.sh) asks the way and says thanks.
Mimi's lines are the owner's registered Lanclo voice (Gemini gemini-3.8-flash-tts) from ../own-voice.json via
kits/mimi-short/scripts/ownvoice.py -> assets/own-voice/ (not in Git; copies in the Drive folder Mimi_03_Frozen_Asked_Directions_assets/own-voice/):
uh.wav "Uh... uh..." (learner accent; only the first "Uh"), answer.wav "Go straight, and turn left." (General American).
Cue times are the first sound; the clips' lead silence is trimmed with start=.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, ding, freeze, pochi, poof, shatter, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
ASK = 0.05                 # "Excuse me, how do I get to the station?" (x1.25, about 2.2 s)
ICE = 0.35                 # the ice forms while the question is still going
UH = 2.18                  # "Uh..." from inside the ice (0.72 s)
DESK = 2.9                 # cut to the desk
TAP = 3.33
MODEL = 3.6                # her own voice gives the answer (speech 1.81 s)
PERK = 5.4
RESULT = 6.0
SAY = 8.1                  # practice
THAW = 10.1                # back on the street: the ice shatters
ANSWER = 11.3              # gives the directions (ends 13.11)
THANKS = 13.35
END = 14.3

OWN = SRC / 'assets/own-voice'
LEAD_UH, LEAD_ANSWER = 0.25, 0.15   # speech starts 0.29 / 0.19 s into the clips
m = Mix(15.3, voice_dir=SRC / 'assets/voice')
m.voice('ask-bm_george.wav', ASK, g=0.8, speed=1.25)
m.sfx(freeze(), ICE)
m.voice(OWN / 'uh.wav', UH - 0.04, g=0.7, start=LEAD_UH, length=0.8, muffle=True)
m.sfx(whoosh(0.25, 0.25), DESK - 0.12)
m.sfx(tap(), TAP)
m.voice(OWN / 'answer.wav', MODEL - 0.04, start=LEAD_ANSWER)
for i, n in enumerate([86, 90, 93, 98]):
    m.sfx(bell(n, 1.0, 0.07), PERK + i * 0.06)
m.sfx(whoosh(0.25, 0.25), RESULT)
for i in range(5):
    m.sfx(tap() * 0.35, RESULT + 0.15 + i * 0.07)
m.sfx(ding(0.12), RESULT + 0.75)
m.voice(OWN / 'answer.wav', SAY - 0.07, g=0.5, start=LEAD_ANSWER)     # the model, under her
m.voice(OWN / 'answer.wav', SAY - 0.04, g=0.85, start=LEAD_ANSWER)
m.sfx(shatter(), THAW)
m.sfx(poof() * 0.5, THAW + 0.05)
m.voice(OWN / 'answer.wav', ANSWER - 0.04, start=LEAD_ANSWER)
m.voice('thanks-bm_george.wav', THANKS, g=0.8)
m.sfx(ding(), THANKS + 0.5)
m.bed(DESK, END, joy_from=PERK)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)  # the end card button gets tapped (kit.tapCta)
print(m.write(SRC / 'hf/assets/mix.wav'))
