"""「写真で英語」 sound: the owner's own voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-shashin/source/scripts/mix.py
Voices in assets/own-voice/ (the owner's registered Lanclo voice, not in Git; rebuild with
kits/mimi-short/scripts/ownvoice.py source/own-voice.json): rough.wav, Mimi's learner take "People is sitting... at a cafe."
(the same sentence the app's fixture transcript corrects), and model.wav, the app's better sentence in General American.
Speech spans (measured): rough 0.29-3.46 s (pause 2.14-2.57), model 0.32-3.42 s.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
ROUGH = 0.0            # hook: she tries to describe the photo ("People is sitting", up to the pause)
APP = 2.1              # the real app
TAP_DESCRIBE = 2.7     # taps 写真描写
TAP_MIC = 3.8          # taps record on the cafe photo
SAY = 3.61             # says the whole line into the app (speech 3.90-7.07)
RESULT = 7.2           # score, the mistake in red
FIX = 9.0              # is -> are
BETTER = 10.6          # a more natural sentence
MODEL = 10.53          # ...in her own voice (speech 10.85-13.95)
JUMP = (14.3, 14.73)
END = 16.05

m = Mix(17.05, voice_dir=SRC / 'assets/own-voice')
m.voice('rough.wav', ROUGH, length=2.15)
m.sfx(whoosh(0.25, 0.25), APP - 0.1)
m.sfx(tap(), TAP_DESCRIBE)
m.sfx(tap(), TAP_MIC)
m.voice('rough.wav', SAY, g=0.8)
m.sfx(ding(0.12), RESULT + 0.1)
m.sfx(whoosh(0.2, 0.2), FIX)
m.sfx(bell(86, 0.8, 0.1), FIX + 0.3)
m.voice('model.wav', MODEL)
m.sfx(boing(True), JUMP[0])
m.sfx(pofu() * 0.6, JUMP[1])
for i, n in enumerate([81, 85, 88]):
    m.sfx(bell(n, 0.9, 0.12), 15.0 + i * 0.07)
m.bed(APP, END, joy_from=BETTER)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)  # the end card button gets tapped (kit.tapCta)
print(m.write(SRC / 'hf/assets/mix.wav'))
