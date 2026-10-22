"""「think が sink に」 sound: the owner's own voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-think-sink/source/scripts/mix.py
Voices: the owner's registered Lanclo voice (Gemini gemini-3.8-flash-tts) from ../own-voice.json via
kits/mimi-short/scripts/ownvoice.py -> assets/own-voice/ (not in Git; copies in the episode's Drive folder,
Mimi_02_Think_Becomes_Sink_assets/own-voice/): wrong.wav "I sink so!" (learner accent), right.wav "I think so." (General American model).
Each clip has ~0.3 s of lead silence: placed with start= (LEAD_*) so the cue times are the first sound.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, clang, ding, pochi, pofu, poof, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
WRONG, SINK1 = 0.09, 0.45            # "I sink so!" (speech 0.96 s, "sink" at +0.20) -> the first sink lands
WRONG2, SINK2 = 1.22, 1.80           # said again, unsure (ends 2.18) -> the second sink
TAP = 2.63                           # taps Lanclo
MODEL = 3.05                         # her own voice, native "think" (speech 0.76 s)
PERK = 4.4
RESULT = 5.0
SAY = 7.2                            # practice: says it with the model
POOF1, POOF2, BULB = 9.1, 9.35, 9.7
JUMP = (10.3, 10.73)
PUMP = 10.95
PROUD = 12.3
END = 14.0

LEAD_WRONG, LEAD_RIGHT = 0.28, 0.23  # lead silence trimmed off (speech starts at 0.32 / 0.27 s in the clips)
m = Mix(15.0, voice_dir=SRC / 'assets/own-voice')
m.voice('wrong.wav', WRONG - 0.04, start=LEAD_WRONG)
m.sfx(whoosh(0.35, 0.3), SINK1 - 0.33)
m.sfx(clang(), SINK1)
m.voice('wrong.wav', WRONG2 - 0.04, g=0.7, start=LEAD_WRONG)
m.sfx(whoosh(0.2, 0.3), SINK2 - 0.18)
m.sfx(clang(0.7), SINK2)
m.sfx(tap(), TAP)
m.voice('right.wav', MODEL - 0.04, start=LEAD_RIGHT)
for i, n in enumerate([86, 90, 93, 98]):
    m.sfx(bell(n, 1.0, 0.07), PERK + i * 0.06)
m.sfx(whoosh(0.25, 0.25), RESULT)
for i in range(5):
    m.sfx(tap() * 0.35, RESULT + 0.15 + i * 0.07)
m.sfx(ding(0.12), RESULT + 0.75)
m.voice('right.wav', SAY - 0.07, g=0.5, start=LEAD_RIGHT)     # the model, under her
m.voice('right.wav', SAY - 0.04, g=0.85, start=LEAD_RIGHT)
m.sfx(poof(), POOF1)
m.sfx(poof(), POOF2)
m.sfx(ding(), BULB)
m.sfx(boing(True), JUMP[0])
m.sfx(pofu() * 0.6, JUMP[1])
for i, n in enumerate([81, 85, 88]):
    m.sfx(bell(n, 0.9, 0.12), PUMP + i * 0.07)
m.voice('right.wav', PROUD - 0.04, start=LEAD_RIGHT)
m.bed(1.0, END, joy_from=PERK)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)  # the end card button gets tapped (kit.tapCta)
print(m.write(SRC / 'hf/assets/mix.wav'))
