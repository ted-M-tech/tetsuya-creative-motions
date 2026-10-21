"""「日記、3日で終わる」: every Rive shot of the episode -> rive/<shot>/ (then scripts/render.sh).

usage: uv run --no-project --with scipy --with pillow --with numpy python films/mimi-nikki/source/scripts/shots.py [shot ...]
"""
import math
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
import rig2d as R  # noqa: E402
from rig2d import body, bone_rot, breathe, smooth, wave  # noqa: E402

# Drawn for this film (../prompts/01-codex-bozu-notebook.txt); goes to the library after approval.
R.add_pose('bozu', SRC / 'art/cut/bozu.webp', 1000)
R.add_pose('artist', SRC / 'art/cut/artist.webp', 1000)   # the app's journal artist, redrawn at full size
POK = (7, 25, 43)   # frames of the three knocks (0.12, 0.42, 0.72 s)


def act_pok(anim, hp, cp, n):
    """三日坊主: eyes closed, the mallet paw knocks the wooden fish three times, a resigned sway."""
    knock = lambda f: max((0.35 * math.exp(-((f - k) / 3.0) ** 2) for k in POK), default=0)
    body(anim, hp, cp, n, squash=lambda f: breathe(f) + 3 * sum(math.exp(-((f - k) / 3.0) ** 2) for k in POK), rot=lambda f: wave(f, 60, 0.015))
    bone_rot(anim, '0:45', n, lambda f: -knock(f))
    bone_rot(anim, '0:43', n, lambda f: -knock(f))


def talk(voice, cache, nod_at, start=6):
    def act(anim, hp, cp, n):
        """Speaks the line (mouth from the voice), a small nod at nod_at."""
        body(anim, hp, cp, n, squash=lambda f: breathe(f) + (10 * max(0.0, math.sin(math.pi * (f - nod_at) / 14)) if nod_at <= f < nod_at + 14 else 0),
             rot=lambda f: wave(f, 40, 0.02))
        bone_rot(anim, '0:41', n, lambda f: wave(f, 20, 0.04))
        R.lipsync(anim, start, SRC / 'assets/voice' / voice, SRC / 'scripts' / cache)
    return act


def act_boast(anim, hp, cp, n):
    """Showing off: leans back, finger wags, a proud bounce."""
    body(anim, hp, cp, n, squash=lambda f: -5 * abs(math.sin(math.pi * f / 22)), rot=lambda f: -0.04 * smooth(f / 14) + wave(f, 44, 0.015))
    bone_rot(anim, '0:45', n, lambda f: wave(f, 11, 0.06))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 22, 0.05, 1))


def act_paint(anim, hp, cp, n):
    """Paints the day: the brush paw sweeps in three strokes, a happy sway."""
    body(anim, hp, cp, n, squash=breathe, rot=lambda f: wave(f, 36, 0.03))
    bone_rot(anim, '0:45', n, lambda f: 0.14 * math.sin(2 * math.pi * f / 26))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 26, 0.05, 1))


A = R.ACTS
SHOTS = {
    'bozu': dict(pose='bozu', act=act_pok, frames=60),                                                   # 0.0  三日坊主, three knocks
    'slump': dict(pose='droop', act=A['droop'], frames=84),                                              # 1.0  the blank page
    'reach': dict(pose='reach', act=A['reach'], frames=42),                                              # 2.4  taps the journal mic (2.83)
    'talk': dict(pose='speak', act=talk('rough-af_heart.wav', 'lipsync-rough.json', 94), frames=108),    # 3.1  "Yesterday... I go to cafe."
    'think': dict(pose='think', act=A['think'], frames=90),                                              # 4.9  diary check card
    'listen': dict(pose='listen', act=A['listen'], frames=96),                                           # 6.4  corrected, in her own voice
    'paint': dict(pose='artist', act=act_paint, frames=108),                                             # 8.0  the day becomes a picture
    'jump': dict(pose='jump', act=A['jump'], frames=42),                                                 # 9.8  the picture calendar fills
    'success': dict(pose='success', act=A['success'], frames=114),                                       # 10.5
    'proud': dict(pose='confident', act=act_boast, frames=96),                                           # 12.4 三日坊主、卒業。
}

if __name__ == '__main__':
    only = sys.argv[1:]
    R.build_shots({k: v for k, v in SHOTS.items() if not only or k in only}, SRC / 'rive')
