"""「日記、3日で終わる」 sound: the owner's own voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-nikki/source/scripts/mix.py
Voices: the owner's registered Lanclo voice (Gemini gemini-3.8-flash-tts) from ../own-voice.json via
kits/mimi-short/scripts/ownvoice.py -> assets/own-voice/ (not in Git; copies in the Drive folder Mimi_04_Journal_Ends_in_3_Days_assets/own-voice/):
rough.wav "Yesterday... I go to cafe." (learner accent, speech 2.48 s) and model.wav "Yesterday, I went to a cafe."
(General American, 2.10 s). Cue times are the first sound; the clips' lead silence is trimmed with start=.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, mokugyo, pencil, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
POK = (0.12, 0.42, 0.72)   # the monk taps the wooden fish
DESK = 1.0
TAP = 2.83                 # taps the journal mic
ROUGH = 3.35               # she talks about her day (ends 5.83)
RESULT = 5.9               # the diary check card
MODEL = 7.45               # the corrected diary in her own voice (ends 9.55)
PAINT = 9.6                # Mimi paints the day
CAL = 11.4                 # the picture calendar: days 4..6 fill in
JUMP = (11.45, 11.88)
PUMP = 12.15
PROUD = 14.0
END = 15.6

LEAD_ROUGH, LEAD_MODEL = 0.19, 0.23   # speech starts 0.23 / 0.27 s into the clips
m = Mix(16.6, voice_dir=SRC / 'assets/own-voice')
for at in POK:
    m.sfx(mokugyo(), at)
m.sfx(whoosh(0.25, 0.25), DESK - 0.12)
m.sfx(tap(), TAP)
m.voice('rough.wav', ROUGH - 0.04, start=LEAD_ROUGH)
m.sfx(whoosh(0.25, 0.25), RESULT)
for i in range(5):
    m.sfx(tap() * 0.35, RESULT + 0.15 + i * 0.07)
m.sfx(ding(0.12), RESULT + 0.75)
m.voice('model.wav', MODEL - 0.04, start=LEAD_MODEL)
m.sfx(pencil(1.2), PAINT + 0.3)
for i, n in enumerate([86, 90, 93, 98]):
    m.sfx(bell(n, 1.0, 0.07), PAINT + 1.5 + i * 0.06)
m.sfx(whoosh(0.3, 0.3), CAL + 0.1)
m.sfx(pop_seq(1, 0.2), CAL + 0.3)
m.sfx(pop_seq(2, 0.22, base=83), CAL + 0.97)
m.sfx(boing(True), JUMP[0])
m.sfx(pofu() * 0.6, JUMP[1])
for i, n in enumerate([81, 85, 88]):
    m.sfx(bell(n, 0.9, 0.12), PUMP + i * 0.07)
m.sfx(ding(), PROUD + 0.05)
m.bed(DESK, END, joy_from=PAINT)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)  # the end card button gets tapped (kit.tapCta)
print(m.write(SRC / 'hf/assets/mix.wav'))
