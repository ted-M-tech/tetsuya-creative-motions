"""Your voice in every language: the hook's greetings, the app's French passage, kit SFX, the theme bed -> hf/assets/mix.wav.

usage: uv run --no-project --with numpy python films/mimi-multilang/source/scripts/mix.py
Voices: the owner's own registered Lanclo voice (Gemini gemini-3.8-flash-tts), the same speaker in every language (`native` +
`language`), made by kits/mimi-short/scripts/ownvoice.py source/own-voice.json into source/assets/own-voice/ (not in Git: biometric;
kept in Drive Multilang_assets/own-voice/). German, Russian, Turkish, Vietnamese and Japanese in the 0.07 s burst stay bubbles only.
Speech windows (silencedetect -40 dB, seconds in each file) — the hook plays them back to back at 1.15x (pitch kept), each bubble
pops as its word starts: en .254-.663, fr .297-.748, es .324-.709, zh .270-.691, ko .259-1.013, it .340-.666, pt .312-.831,
hi .347-.864; app-fr .216-2.984.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
from sfx import Mix, boing, ding, pochi, pop_seq, tap, whoosh  # noqa: E402

# Cue sheet (seconds); hf/index.html uses the same times.
SPEED = 1.15
CLIPS = [  # (file, speech onset, speech end) in the file
    ('hi-en.wav', .254, .663), ('hi-fr.wav', .297, .748), ('hi-es.wav', .324, .709), ('hi-zh.wav', .270, .691),
    ('hi-ko.wav', .259, 1.013), ('hi-it.wav', .340, .666), ('hi-pt.wav', .312, .831), ('hi-hi.wav', .347, .864),
]
GAP = 0.03
HOOK, at = [], 0.05
for name, on, off in CLIPS:
    HOOK.append((round(at, 3), name, on, off))
    at += (off - on) / SPEED + GAP          # 0.05 0.436 0.858 1.223 1.619 2.305 2.618 3.099 (hf/index.html `hook`)
BURST = (3.55, 3.62, 3.69, 3.76, 3.83)  # Hallo / Привет / Merhaba / Xin chào / こんにちは: bubbles only
COPY = 3.95
INTRO = 5.25
APP = 6.55
TAPS = (6.7, 7.715, 8.85, 13.13, 13.94)
FRENCH = 9.2           # 試聴 starts playing in the take (61.35 s); speech 9.22-11.99
KOREAN = 14.75         # the Korean passage is on screen (試聴 not pressed: no voice)
TRIP = 15.75
REPLY = 16.85
END = 18.15
CTA_TAP = 18.75

m = Mix(19.55, voice_dir=SRC / 'assets/own-voice')
for at, name, on, off in HOOK:
    lead = 0.03
    m.voice(name, at - lead / SPEED, g=0.95, start=on - lead, length=off - on + 2 * lead, speed=SPEED)
m.sfx(pop_seq(len(BURST), 0.07, base=76), BURST[0])
m.sfx(whoosh(0.3, 0.3), COPY - 0.1)
m.sfx(pop_seq(3, 0.05, base=79), COPY + 0.05)
m.sfx(boing(True), INTRO)
m.sfx(whoosh(0.35, 0.3), APP)
for at in TAPS:
    m.sfx(tap() * 0.6, at)
m.voice('app-fr.wav', FRENCH - 0.02, g=0.9, start=0.19)
m.sfx(ding(), KOREAN)
m.sfx(pop_seq(4, 0.05, base=79), TRIP)
m.sfx(pop_seq(2, 0.06, base=83), REPLY)
m.bed(0.0, END)
m.end_chord(END)
m.sfx(pochi(), CTA_TAP)
print(m.write(SRC / 'hf/assets/mix.wav'))
