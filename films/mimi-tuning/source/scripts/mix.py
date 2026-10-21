"""Voice tuning: Mimi's AI voice before and a British-sounding stand-in after, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-tuning/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh): "Shall we have a cup of tea?" by af_heart (Mimi's English voice) and by
bf_isabella (stand-in for a preview made with the request「イギリス英語っぽく」; the film never presses「試聴音声を作る」).
Japanese lines are speech bubbles only (Kokoro's Japanese voice garbles them).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
BEFORE = 0.35          # her AI voice, slightly not her
TILT = 0.9
COPY = 2.9             # the hook card
APP = 4.1              # the app
TAPS = (4.62, 5.095, 5.725, 6.345, 6.6)
TYPING = [7.025 + 0.24 * i for i in range(9)]
CREATE = 9.15          # the button pulses (not pressed)
LIST = 9.9             # the previews to compare
AFTER = 11.75          # the British-sounding preview (stand-in)
PUNCH = 14.0
NEVER = 15.0
END = 16.0
CTA_TAP = 16.6

m = Mix(17.4, voice_dir=SRC / 'assets/voice')
m.voice('before-af_heart.wav', BEFORE, g=0.85)
m.sfx(boing(False) * 0.6, TILT)
m.sfx(whoosh(0.3, 0.3), COPY - 0.1)
m.sfx(pop_seq(3, 0.05, base=76), COPY + 0.05)
m.sfx(whoosh(0.35, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
for at in TYPING:
    m.sfx(tap() * 0.25, at)
m.sfx(ding(), CREATE)
m.sfx(bell(88, 0.7, 0.08), LIST)
m.voice('after-bf_isabella.wav', AFTER, g=0.9)
m.sfx(pop_seq(4, 0.05, base=79), 13.2)
m.sfx(bell(93, 0.9, 0.08), PUNCH + 0.1)
m.sfx(pofu() * 0.7, NEVER)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
