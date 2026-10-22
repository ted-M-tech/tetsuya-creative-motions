"""「180秒しゃべり続けたら、口癖がバレた」(033) sound: the owner's voice, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-180/source/scripts/mix.py
Voices: assets/own-voice/ (not in Git; the owner's registered Lanclo voice via ownvoice.py, see own-voice.json):
habit.wav (learner, the habit-heavy take) and fix.wav (us, the improved wording).
Word times measured on habit.wav (silencedetect -32 dB + whisper small.en): "It" 0.30, really 1.07 / 1.81, "nice" ends 2.79,
"And" 3.43, really 5.33 / 5.91, "good" ends 6.64, "Really." 7.40-7.78. fix.wav: speech 0.01-2.08.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
A_AT, A_FROM, A_LEN = 0.05, 0.25, 2.62     # "It looks really, really nice."  -> really at 0.87, 1.61
FF = (2.7, 3.4)                            # fast-forward: 4 more "really" pops
FF_POPS = (2.8, 2.95, 3.1, 3.25)
B_AT, B_FROM = 3.45, 3.38                  # "And the coffee looks really, really good. Really." -> really 5.40, 5.98, 7.47
REALLY = (0.87, 1.61) + FF_POPS + (5.40, 5.98, 7.47)
TIME_UP = 8.0
DONE = 8.1
APP = 9.1
GAG = 14.1
FIX_AT = 16.55
END = 18.8
CTA_TAP = 19.25

m = Mix(20.0, voice_dir=SRC / 'assets/own-voice')
m.voice('habit.wav', A_AT, start=A_FROM, length=A_LEN)
m.voice('habit.wav', B_AT, start=B_FROM, length=8.10 - B_FROM)
for at in REALLY:
    m.sfx(pofu() * 0.35, at)
m.sfx(whoosh(0.6, 0.3), FF[0])
m.sfx(ding() * 0.6, TIME_UP)
m.sfx(pop_seq(3, 0.05, base=76), DONE)
m.sfx(whoosh(0.3, 0.2), APP)
m.sfx(tap() * 0.5, APP + 1.6)
m.sfx(bell(88, 0.6, 0.06), APP + 3.2)
m.sfx(boing(False), GAG)
m.sfx(boing(True), GAG + 1.0)
m.sfx(pop_seq(3, 0.05, base=79), FIX_AT - 0.4)
m.voice('fix.wav', FIX_AT)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
