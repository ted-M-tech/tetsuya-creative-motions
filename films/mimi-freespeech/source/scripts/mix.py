"""Keep talking for 3 minutes: Mimi's halting English, the French friend's line, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-freespeech/source/scripts/mix.py
Voices in assets/voice/ (rebuild with scripts/voices.sh): Mimi describing the café photo (af_heart) and the friend's
"Trois minutes, c'est trop court !" (ff_siwis). Japanese lines are speech bubbles only (Kokoro's Japanese voice garbles them).
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, bell, boing, ding, freeze, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
HOOK = 0.0             # Mimi's despair: 「こんなの学校でやったことなかったもん！」
APP = 2.0              # the photo screen, 最大 3:00
TALK = 4.1             # Mimi speaks on her own, the clock runs (fast-forwarded)
VOICE = 4.15
TIME_UP = 7.85         # the clock reaches 3:00
RESULT = 8.1           # AI feedback: scores and transcript
ZOOM = 9.6
FRIEND = 11.0          # the French friend
COURT = 11.25
REPLY = 13.4           # Mimi: …こっちは3分が長いんだけど
MESSAGE = 15.2         # researcher Mimi: the output hypothesis
END = 17.6
CTA_TAP = 18.2
TOTAL = 19.0

m = Mix(TOTAL, voice_dir=SRC / 'assets/voice')
m.sfx(freeze(0.4), HOOK)
m.sfx(boing(False) * 0.7, HOOK + 0.15)
m.sfx(whoosh(0.35, 0.3), APP - 0.05)
m.sfx(whoosh(0.3, 0.25), TALK - 0.05)
m.voice('describe-af_heart.wav', VOICE, g=0.9)
t = TALK + 0.2
while t < TIME_UP - 0.1:          # the running clock
    m.sfx(tap() * 0.18, t)
    t += 0.25
m.sfx(ding(), TIME_UP)
m.sfx(bell(84, 0.6, 0.08), TIME_UP + 0.08)
m.sfx(whoosh(0.35, 0.3), RESULT - 0.05)
m.sfx(pop_seq(4, 0.05, base=79), RESULT + 0.15)
m.sfx(tap() * 0.4, ZOOM)
m.sfx(boing(True), FRIEND)
m.voice('court-ff_siwis.wav', COURT, g=0.9)
m.sfx(pofu() * 0.6, REPLY + 0.05)
m.sfx(whoosh(0.3, 0.3), MESSAGE - 0.05)
m.sfx(pop_seq(3, 0.05, base=79), MESSAGE + 0.4)
m.bed(APP, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
