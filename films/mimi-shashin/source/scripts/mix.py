"""「写真で英語」 sound: Kokoro voice lines, kit SFX, the kit bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-shashin/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh), af_heart: Mimi's rough "People is sitting... at a cafe."
(the same sentence the app's fixture transcript corrects) and the app's better sentence, standing in for her own voice.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, tap, whoosh  # noqa: E402

# Cue sheet (seconds); the HyperFrames edit uses the same times.
ROUGH = 0.2            # hook: she tries to describe the photo
APP = 2.1              # the real app
TAP_DESCRIBE = 2.7     # taps 写真描写
TAP_MIC = 3.8          # taps record on the cafe photo
SAY = 3.9              # says it into the app
RESULT = 5.8           # score, the mistake in red
FIX = 7.6              # is -> are
BETTER = 9.2           # a more natural sentence
MODEL = 9.45           # ...in her own voice
JUMP = (12.25, 12.68)
END = 14.0

m = Mix(15.0, voice_dir=SRC / 'assets/voice')
m.voice('rough-af_heart.wav', ROUGH)
m.sfx(whoosh(0.25, 0.25), APP - 0.1)
m.sfx(tap(), TAP_DESCRIBE)
m.sfx(tap(), TAP_MIC)
m.voice('rough-af_heart.wav', SAY, g=0.8)
m.sfx(ding(0.12), RESULT + 0.1)
m.sfx(whoosh(0.2, 0.2), FIX)
m.sfx(bell(86, 0.8, 0.1), FIX + 0.3)
m.voice('model-af_heart.wav', MODEL)
m.sfx(boing(True), JUMP[0])
m.sfx(pofu() * 0.6, JUMP[1])
for i, n in enumerate([81, 85, 88]):
    m.sfx(bell(n, 0.9, 0.12), 12.95 + i * 0.07)
m.bed(APP, END, joy_from=BETTER)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)  # the end card button gets tapped (kit.tapCta)
print(m.write(SRC / 'hf/assets/mix.wav'))
