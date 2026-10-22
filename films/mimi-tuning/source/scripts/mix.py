"""Voice tuning: Mimi's AI voice before (General American) and after the request「イギリス英語っぽく」(British), kit SFX, the theme bed
-> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-tuning/source/scripts/mix.py
Voices: the owner's own registered Lanclo voice (Gemini gemini-3.8-flash-tts), "Can't I have a bottle of water after the party?"
with the `us` and `uk` presets — made by kits/mimi-short/scripts/ownvoice.py source/own-voice.json into source/assets/own-voice/
(not in Git: biometric; kept in Drive Tuning_assets/own-voice/). The film never presses「試聴音声を作る」: the after take is illustrative.
Japanese lines are speech bubbles only.
Measured (silencedetect -40 dB, whisper word timestamps): before-us speech 0.24-2.69 s; after-uk speech 0.19-3.15 s,
words can't 0.21, bottle 0.88, water 1.53, after 1.95, party 2.67.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
BEFORE = 0.3           # her AI voice (us), trimmed 0.2 s of lead-in: speech 0.34-2.79
TILT = 1.6
COPY = 3.75            # the hook card
APP = 4.95             # the app
TAPS = (5.47, 5.945, 6.575, 7.195, 7.45)
TYPING = [7.875 + 0.24 * i for i in range(9)]
CREATE = 10.0          # the button pulses (not pressed)
LIST = 10.75           # the previews to compare
AFTER = 12.6           # the British preview (uk), trimmed 0.15 s: speech 12.64-15.6
OOH = 15.6
PUNCH = 16.2
NEVER = 17.2
END = 18.2
CTA_TAP = 18.8

m = Mix(19.6, voice_dir=SRC / 'assets/own-voice')
m.voice('before-us.wav', BEFORE, g=0.85, start=0.2)
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
m.voice('after-uk.wav', AFTER, g=0.9, start=0.15)
m.sfx(pop_seq(4, 0.05, base=79), OOH)
m.sfx(bell(93, 0.9, 0.08), PUNCH + 0.1)
m.sfx(pofu() * 0.7, NEVER)
m.bed(COPY, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
