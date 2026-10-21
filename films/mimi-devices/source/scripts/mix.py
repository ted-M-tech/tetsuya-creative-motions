"""「スマホでも、タブレットでも、パソコンでも」 (mimi-devices) sound: kit SFX on the cue sheet and the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-devices/source/scripts/mix.py
No voices: every line is a speech bubble (Kokoro's Japanese voice is garbled).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
STUDY = 0.1
NOTIF = 0.85            # the video app's notification
TAP = 1.45
HAHA = 1.65
SIGH = 2.65
WANT = 3.45
LAPTOP = 4.4
FLASH = 4.85            # the screen flashes, Mimi bursts out
WEB = 5.35
DEVICES = 6.6
ASK = (8.05, 12.35, 15.45)   # 「…Androidの私は？」 x3
SYNC = 9.2
HL_WEB, ARC, HL_IOS = 10.55, 10.8, 11.3
COPY = (13.45, 13.8, 14.15)
SOON = 16.1
WEB2 = 17.05
CHEER = 17.3
END = 18.6
CTA_TAP = 19.2

m = Mix(20.0, voice_dir=SRC / 'assets/voice')
m.sfx(pofu() * 0.4, STUDY)
m.sfx(ding(0.16), NOTIF)
m.sfx(tap() * 0.7, TAP)
m.sfx(pop_seq(3, 0.06, base=79), HAHA)
m.sfx(boing(False), SIGH)
m.sfx(pofu() * 0.4, WANT)
m.sfx(whoosh(0.3, 0.2), LAPTOP)
m.sfx(bell(84, 0.5, 0.06), FLASH)
m.sfx(whoosh(0.4, 0.3), FLASH + 0.1)
m.sfx(boing(True), FLASH + 0.35)
m.sfx(pop_seq(3, 0.05, base=76), WEB)
m.sfx(whoosh(0.3, 0.2), DEVICES)
m.sfx(whoosh(0.25, 0.15), DEVICES + 0.15)
for i, at in enumerate(ASK):
    m.sfx(boing(False) * (0.8 + 0.1 * i), at)
m.sfx(whoosh(0.3, 0.2), SYNC)
m.sfx(whoosh(0.3, 0.2), SYNC + 0.15)
m.sfx(tap() * 0.5, HL_WEB)
m.sfx(whoosh(0.5, 0.3), ARC)
m.sfx(bell(79, 0.6, 0.07), HL_IOS)
m.sfx(ding(), HL_IOS + 0.05)
for i, at in enumerate(COPY):
    m.sfx(bell(72 + 4 * i, 0.5, 0.06), at)
m.sfx(boing(True), SOON)
m.sfx(pop_seq(3, 0.05, base=76), WEB2)
m.sfx(boing(True), CHEER)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
