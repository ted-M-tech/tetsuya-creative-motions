"""Your voice in every language: the hook's greetings, the app's French passage, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-multilang/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh) are a Kokoro TTS STAND-IN for the friend's own AI voice, not a clone:
one female Kokoro voice per language where Kokoro has one. Korean, German, Russian, Turkish, Vietnamese and Japanese are speech
bubbles only (a pop, no voice). Japanese lines are speech bubbles (Kokoro's Japanese voice garbles them).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, boing, ding, pochi, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = [  # (time, voice file or None for a bubble only)
    (0.05, 'hi-en.wav'), (0.40, 'hi-fr.wav'), (0.75, 'hi-es.wav'), (1.08, 'hi-zh.wav'), (1.40, None),
    (1.70, 'hi-it.wav'), (2.02, 'hi-pt.wav'), (2.32, 'hi-hi.wav'),
]
BURST = (2.70, 2.77, 2.84, 2.91, 2.98)  # Hallo / Привет / Merhaba / Xin chào / こんにちは: bubbles only
COPY = 3.1
INTRO = 4.4
APP = 5.7
TAPS = (5.85, 6.865, 8.0, 12.28, 13.09)
FRENCH = 8.35          # 試聴 starts playing in the take (61.35 s)
KOREAN = 13.9          # the Korean passage is on screen (no voice: Kokoro has no Korean)
TRIP = 14.9
REPLY = 16.0
END = 17.3
CTA_TAP = 17.9

m = Mix(18.7, voice_dir=SRC / 'assets/voice')
for i, (at, name) in enumerate(HOOK):
    nxt = HOOK[i + 1][0] if i + 1 < len(HOOK) else BURST[0]
    if name:
        m.voice(name, at, g=0.95, length=nxt - at + 0.12)   # quick cuts: each greeting stops as the next one starts
    else:
        m.sfx(pop_seq(1, 0.05, base=81), at)
m.sfx(pop_seq(len(BURST), 0.07, base=76), BURST[0])
m.sfx(whoosh(0.3, 0.3), COPY - 0.1)
m.sfx(pop_seq(3, 0.05, base=79), COPY + 0.05)
m.sfx(boing(True), INTRO)
m.sfx(whoosh(0.35, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.voice('app-fr.wav', FRENCH, g=0.9, speed=1.08)
m.sfx(ding(), KOREAN)
m.sfx(pop_seq(4, 0.05, base=79), TRIP)
m.sfx(pop_seq(2, 0.06, base=83), REPLY)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
