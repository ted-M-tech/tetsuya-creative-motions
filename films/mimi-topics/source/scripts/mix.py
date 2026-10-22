"""「AIと会話、毎回『何話そう…』で終わってない？」(031) sound: the owner's voice, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-topics/source/scripts/mix.py
Voice: assets/own-voice/light.wav (not in Git; the owner's registered Lanclo voice via ownvoice.py, accent us, see own-voice.json):
"Please leave the light on." — the lesson's お手本 in your own voice. Speech 0.29-1.57 s in the clip (silencedetect -40 dB).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
TICKS = [0.6 + 0.45 * i for i in range(4)]   # the awkward silence in front of the empty box
TYPE = (2.45, 2.6, 2.75)                      # "Hi!" typed
SEND = 2.9
REPLY = 3.35
STUNNED = 3.75
COPY = 4.6
APP = 5.8
CHIPS = (7.9, 10.1, 11.3)
LESSON = 13.1
MODEL_TAP = 14.1
VOICE = 14.15                                  # speech 14.44-15.72
PROUD = 15.85
END = 16.6
CTA_TAP = 17.05

m = Mix(17.8, voice_dir=SRC / 'assets/own-voice')
for at in TICKS:
    m.sfx(tap() * 0.25, at)
for at in TYPE:
    m.sfx(tap() * 0.45, at)
m.sfx(whoosh(0.2, 0.15), SEND)
m.sfx(pofu() * 0.5, REPLY)
m.sfx(boing(False), STUNNED)
m.sfx(whoosh(0.35, 0.3), COPY - 0.05)
m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.1)
m.sfx(whoosh(0.3, 0.2), APP)
for at in CHIPS:
    m.sfx(pop_seq(2, 0.05, base=79), at)
m.sfx(tap() * 0.6, MODEL_TAP)
m.voice('light.wav', VOICE)
m.sfx(bell(88, 0.6, 0.06), PROUD)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
