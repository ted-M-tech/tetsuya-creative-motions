"""AI voice in 1 minute: the two English takes of the model sentence, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-voice/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh): "Let's grab a coffee and catch up this weekend." by am_michael (the native
speaker she admires, heard through her headphones) and by af_bella (the friend's own English voice since mimi-action-add).
Japanese lines are speech bubbles only (Kokoro's Japanese voice garbles them).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
MODEL = 0.1            # the native speaker in her headphones
COPY = 3.0             # the hook card
MIMI = 4.2             # Mimi pops in
APP = 5.5              # the app
TAPS = (7.28, 8.13, 8.89, 9.11, 10.06, 11.47)
TOGGLES = (5.73, 6.10, 6.55, 6.95)
READY = 12.19
OWN = 13.5             # the same sentence in her own voice
FLUENT = 14.7
TEASE = 16.0
END = 17.3
CTA_TAP = 17.9

m = Mix(18.7, voice_dir=SRC / 'assets/voice')
m.voice('model-am_michael.wav', MODEL, g=0.8, muffle=False)
m.sfx(whoosh(0.3, 0.3), COPY - 0.1)
m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.05)
m.sfx(boing(True), MIMI)
m.sfx(whoosh(0.35, 0.3), APP)
for at in TOGGLES:
    m.sfx(tap() * 0.3, at)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(ding(), READY)
m.sfx(bell(88, 0.7, 0.08), READY + 0.1)
m.voice('friend-af_bella.wav', OWN, g=0.9)
m.sfx(pop_seq(4, 0.05, base=79), FLUENT)
m.sfx(pofu() * 0.6, TEASE)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
