"""Narration, the two LP voice clips, code-made music and SFX for the app intro.  usage: intro_audio.py OUT.wav

Narration lines are assets/voice/vo-intro/v1.wav ... v10.wav (cut from the Mimi take by intro_vo.sh); missing lines are skipped.
The LP clips are assets/voice/own.mp3 and model.mp3; the theme BGM is the kit's library/bgm/everyone-get-up.mp3.
None of these are in Git (see source/README.md); without the BGM the code-made bed plays.
"""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from audio import (A, ROOT, SR, BEAT, CHORDS, load, mallet, bell, pad, sub, kick, clap, shaker, whoosh, pop, impact,  # noqa: E402
                   noise, lowpass, tsec, note)
from render import MODEL_LEN, SAMPLE  # noqa: E402
from intro_timeline import *  # noqa: E402,F403
from intro import LINE1, LINE2A, LINE2B  # noqa: E402

N = int(DURATION * SR)
VO_END = 29.76  # v10's last sound
BGM = ROOT.parents[2] / 'kits/mimi-short/library/bgm/everyone-get-up.mp3'  # Lanclo SNS theme: OpenTracks「Everyone Get Up」(Anonyment), track 1
BGM_GAIN = 0.055  # ~21 dB under the narration
VO_DIR = A / 'voice' / 'vo-intro'


def place(bus, x, t, gain=1.0):
    i = int(t * SR)
    x = x[:max(0, N - i)]
    bus[i:i + len(x)] += x * gain


def key_tap(seed):
    """A soft keyboard tap: a short click on top of a low thock."""
    r = np.random.default_rng(seed)
    n = r.standard_normal(int(0.06 * SR))
    t = tsec(0.06)
    click = (n - lowpass(n, 0.3)) * np.exp(-90 * t)
    thock = np.sin(2 * np.pi * r.uniform(150, 190) * t) * np.exp(-60 * t)
    return 0.35 * click + 0.25 * thock


TEMPO = 60 / 118  # a bouncy two-step, quicker than the promo's 100
PLAY_CH = [(62, [62, 66, 69]), (67, [67, 71, 74]), (69, [69, 73, 76]), (62, [62, 66, 69])]  # D G A D
MOTIFS = [[0, None, 4, 7, None, 4, 9, 7], [12, None, 11, 9, 7, None, 4, None]]  # semitones over the chord root


def pluck(midi, d=0.35, vel=0.3):
    """Short ukulele-ish pluck: a few harmonics, quick decay."""
    t = tsec(d)
    f = note(midi)
    w = sum(np.sin(2 * np.pi * f * h * t) / h ** 1.5 for h in (1, 2, 3, 4))
    return vel * w * np.exp(-14 * t) * np.minimum(1, t / 0.002)


def tuba(midi, d=0.28, vel=0.5):
    """The oom of oom-pah: a round low note with a little lip at the start."""
    t = tsec(d)
    f = note(midi) * (1 - 0.04 * np.exp(-30 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return vel * (np.sin(ph) + 0.35 * np.sin(2 * ph)) * np.exp(-7 * t) * np.minimum(1, t / 0.01)


def slide_mallet(midi, vel):
    """A mallet note that scoops up a semitone into pitch: the cheeky grace note."""
    t = tsec(0.5)
    f = note(midi) * 2 ** (-np.exp(-60 * t) / 12)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return vel * (np.sin(ph) + 0.25 * np.sin(4 * ph)) * np.exp(-6 * t) * np.minimum(1, t / 0.003)


def woodblock(vel=0.25):
    t = tsec(0.08)
    return vel * np.sin(2 * np.pi * 1250 * t) * np.exp(-70 * t)


def boing(vel=0.3, d=0.5):
    """Cartoon spring: pitch wobbles down."""
    t = tsec(d)
    f = 260 + 220 * np.exp(-6 * t) * (1 + 0.35 * np.sin(2 * np.pi * 14 * t))
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-4 * t) * np.minimum(1, t / 0.005)


def music():
    """The Lanclo SNS theme from v1 under the same level automation (the code-made bed below is the fallback)."""
    if BGM.exists():
        bus = np.zeros(N)
        x = load(BGM, DURATION - VO['v1'] + 0.1)
        place(bus, x, VO['v1'] - 0.1)
        return bus * level()
    return music_code()


def level():
    tt = np.arange(N) / SR
    return np.interp(tt, [0, VO['v1'], VO['v1'] + 1.0, MOVE2[0], CARD_IN[0], FREEZE, FREEZE + 0.05, MODEL_START + MODEL_CLIP,
                         H_VOICE[0], TAG[0] - 0.3, TAG[0], DURATION],
                     [0, 0, 0.45, 0.45, 0.18, 0.18, 0.0, 0.0, 0.8, 0.8, 1.0, 1.0])


def music_code():
    """A playful oom-pah bed from v1, out for the comparison, back at the headline, full from the tagline."""
    bus = np.zeros(N)
    bar = 4 * TEMPO
    t0, t1 = VO['v1'], MIMI_LAND
    t, idx = t0, 0
    while t < t1:
        root, ch = PLAY_CH[idx % 4]
        for k in range(4):  # oom on 1 and 3 (root, then fifth), pah on 2 and 4
            tt = t + k * TEMPO
            if tt >= t1:
                break
            if k % 2 == 0:
                place(bus, tuba(root - 24 + (7 if k == 2 else 0)), tt)
            else:
                for j, m in enumerate(ch):
                    place(bus, pluck(m, 0.25, 0.12), tt + j * 0.008)
        for k, iv in enumerate(MOTIFS[idx % 2]):  # swung eighths
            tt = t + k * TEMPO / 2 + (0.06 if k % 2 else 0)
            if iv is None or tt >= t1:
                continue
            m = root + 12 + iv
            place(bus, slide_mallet(m, 0.2) if k == 0 else mallet(m, 0.5, 0.16), tt)
        t += bar
        idx += 1
    t = H_VOICE[0]  # woodblock ticks from the headline onwards
    while t < t1 - 0.05:
        place(bus, woodblock(), t + TEMPO / 2 + 0.06)
        place(bus, shaker(), t)
        t += TEMPO
    for i, m in enumerate([62, 66, 69, 74]):  # ta-da
        place(bus, pluck(m + 12, 0.8, 0.22), MIMI_LAND + i * 0.06)
    place(bus, tuba(38, 1.2, 0.6), MIMI_LAND)
    place(bus, pad([50, 57, 62, 66, 69], DURATION - MIMI_LAND, 0.14), MIMI_LAND)
    return bus * level()


def soft_bell(m, d, vel):
    """The chimes an octave down and much quieter: they were piercing on earphones."""
    return bell(m - 12, d, vel * 0.3)


def sfx():
    bus = np.zeros(N)
    n1 = len(LINE1)
    for i in range(n1):
        place(bus, key_tap(i), TYPE_1[0] + i * TYPE_1[1], 0.9)
    for i in range(len(LINE2A + LINE2B)):
        place(bus, key_tap(40 + i), TYPE_2[0] + i * TYPE_2[1], 0.9)
    place(bus, boing(0.35), 0.1)  # Mimi springs up
    place(bus, impact(0.35), JOLT)
    place(bus, pop(79, 0.25), CARD_2 + 0.2)
    for w in WHOOSHES:
        place(bus, whoosh(0.8, 0.3), w)
    for i, m in enumerate([74, 81, 86]):  # logo chime
        place(bus, soft_bell(m + 12, 1.8, 0.2), LOGO_LINE[1] - 0.05 + i * 0.07)
    place(bus, pop(84, 0.25), MIMI_POP)
    place(bus, pop(79, 0.3), CARD_IN[0] + 0.1)
    c = np.random.default_rng(9).standard_normal(int(0.02 * SR))  # the record button's click
    place(bus, (c - lowpass(c, 0.4)) * np.exp(-200 * tsec(0.02)) * 0.8, REC_CLICK)
    place(bus, pop(83, 0.25), MODEL_LABEL)
    place(bus, whoosh(0.6, 0.15), MERGE[0])
    for i in range(5):
        place(bus, pop(84 + i * 2, 0.12), PENT[0] + i * 0.12)
    place(bus, pop(76, 0.3), FILL[0] + 0.2)
    for i in range(6):  # 61 -> 67 counts up
        place(bus, pop(86 + i, 0.16), GAIN[0] + (i + 0.5) * (GAIN[1] - GAIN[0]) / 6)
    place(bus, soft_bell(98, 1.0, 0.15), GAIN[1])
    place(bus, pop(79, 0.3), TIP_IN)
    for i, m in enumerate([76, 83]):
        place(bus, soft_bell(m + 12, 1.4, 0.22), TIP_IN + 0.7 + i * 0.09)
    for i, t in enumerate([LANG_EN, LANG_KO]):  # the two named languages
        place(bus, pop(81 + 4 * i, 0.35), t)
        place(bus, soft_bell(93 + 4 * i, 1.0, 0.1), t)
    for i in range(15):  # the other fifteen pop in a run
        place(bus, pop(79 + (i * 5) % 14, 0.16), LANG_ALL + i * LANG_STEP)
    for i, m in enumerate([86, 90, 93, 98]):  # 17 lands
        place(bus, soft_bell(m + 12, 1.6, 0.16), LANG_ALL + 15 * LANG_STEP + i * 0.06)
    place(bus, whoosh(0.5, 0.18), CONVERGE)
    place(bus, pop(84, 0.2), TAG[0])
    place(bus, pop(88, 0.2), TAG[1])
    place(bus, impact(0.5), MIMI_LAND)
    place(bus, boing(0.3, 0.45), MIMI_LAND + 0.02)
    for i, m in enumerate([74, 78, 81, 86]):
        place(bus, soft_bell(m + 12, 2.2, 0.22), FANFARE + i * 0.09)
    place(bus, pop(79, 0.25), END_CARD)
    for i, m in enumerate([93, 98]):  # wink twinkle
        place(bus, soft_bell(m + 12, 1.0, 0.12), WINK + 0.05 + i * 0.07)
    return bus


def voice():
    bus = np.zeros(N)
    for k, t in VO.items():
        f = VO_DIR / f'{k}.wav'
        if f.exists():
            place(bus, load(f), t, 1.0)
    for name, start, length in (('own.mp3', OWN_START, OWN_CLIP), ('model.mp3', MODEL_START, MODEL_CLIP)):
        if (A / 'voice' / name).exists():
            place(bus, load(A / 'voice' / name, length), start)
    if TAIL is None:
        return bus
    s = SAMPLE['model']['words'][7]['start']  # "available?" once more, out by the last frame
    tail = load(A / 'voice' / 'model.mp3', MODEL_LEN)[int(s * SR):]
    tail = tail[:int((DURATION - TAIL) * SR)]
    tail[-int(0.06 * SR):] *= np.linspace(1, 0, int(0.06 * SR))
    place(bus, tail, TAIL, 0.85)
    return bus


def main():
    v, m, s = voice(), music(), sfx()
    env = lowpass(np.abs(v), 0.002)
    duck = 1 - 0.8 * np.clip(env / (env.max() * 0.15), 0, 1)
    duck = lowpass(duck, 0.0008)
    # the voice leads: music and effects sit well under it, and ease out after the last line
    tt = np.arange(N) / SR
    tail = np.interp(tt, [0, VO_END, DURATION], [1, 1, 0])
    mix = v * 1.0 + (m * BGM_GAIN * duck + s * 0.12) * tail
    mix /= np.abs(mix).max() / 0.9
    raw = Path(sys.argv[1]).with_suffix('.raw.wav')
    raw.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(raw), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                    '-ar', str(SR), sys.argv[1]], check=True)
    raw.unlink()


if __name__ == '__main__':
    main()
