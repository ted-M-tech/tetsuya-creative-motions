"""065「I'm fine, thank you. しか言えない」 sound: the Friend's two English lines in the owner's voice, kit SFX, the theme bed
-> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-decks-fine/source/scripts/mix.py
Mimi's "How's it going?" is a speech bubble only (one voice for both bunnies would sound like one person talking to himself).
Own voice (Gemini gemini-3.8-flash-tts via kits/mimi-short/scripts/ownvoice.py; WAVs not in Git, Drive Decks_ImFine_assets/own-voice/):
  fine.wav   "I'm fine, thank you. And you?"  robotic textbook style; speech 0.27-3.20 s (silencedetect -40 dB)
  casual.wav "All good! What's new?"          relaxed US; speech 0.21-1.59 s
"""
import json as _j
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import SR, Mix, ding, pochi, pofu, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
ASK = 0.1          # Mimi's bubble "How's it going?"
FINE = 0.45        # fine.wav placed here: speech 0.72-3.65
YAWN = 3.8
APP = 5.5
TAPS = (6.7, 7.9, 10.25)   # スラング・カジュアル, ユニット4, the bookmark
SCROLL = 9.0
CARD = 10.0
SAVED = 10.7
RETRY = 12.2
ASK2 = 12.3
CASUAL = 12.75     # casual.wav: speech 12.96-14.34
FIVE = 14.9
END = 16.5
DUR = 18.0

m = Mix(DUR, voice_dir=SRC / 'assets/own-voice')
m.sfx(pop_seq(1, 0.05, base=79), ASK)
m.voice('fine.wav', FINE, g=0.9)
m.sfx(pofu() * 0.5, YAWN)
m.sfx(whoosh(0.35, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.sfx(whoosh(0.25, 0.2), SCROLL)
m.sfx(ding(), SAVED)
m.sfx(whoosh(0.3, 0.3), RETRY)
m.sfx(pop_seq(1, 0.05, base=79), ASK2)
m.voice('casual.wav', CASUAL, g=0.9)
m.sfx(tap() * 0.8, FIVE + 0.05)
m.sfx(pop_seq(3, 0.05, base=79), FIVE + 0.15)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), END + 0.6)
out = m.write(SRC / 'hf/assets/mix.wav')


# loudnorm's single pass stops short of -14 on a short, voice-sparse film (true peak bound): measure, add the missing gain
# in front of a limiter (0.8, true peak under -1.5 dBTP), and measure again. The balance between voice, SFX and bed is unchanged.
# (Same step as films/mimi-katakana-mcdonalds/source/scripts/mix.py.)
def lufs(f):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    d = _j.loads(re.search(r'\{[^{}]*\}', err[err.rfind('Parsed_loudnorm'):]).group(0))
    return float(d['input_i']), float(d['input_tp'])


for _ in range(3):
    i, tp = lufs(out)
    if abs(i + 14) < 0.3 and tp <= -1.5:
        break
    tmp = out.with_suffix('.tmp.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(out), '-af',
                    f'volume={-14 - i + 0.1:.2f}dB,alimiter=limit=0.8:level=false:attack=1:release=60', '-ar', str(SR), str(tmp)], check=True)
    shutil.move(tmp, out)
print(out, 'I=%.1f LUFS TP=%.1f dBTP' % lufs(out))
