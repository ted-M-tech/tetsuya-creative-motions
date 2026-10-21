"""Action Button ① (Add a phrase): every Rive shot of the episode -> rive/<shot>/ (then scripts/render.sh).

Mimi stands beside the real app screen on a flat plate (the page colour); the edit scales and moves her.
New poses (blush, angry) are drawn by Codex in art/ and cut out to art/*.webp (see README).
usage: uv run --no-project --with scipy --with pillow --with numpy python films/mimi-action-add/source/scripts/shots.py [shot ...]
"""
import math
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
import rig2d as R  # noqa: E402
from rig2d import body, bone_rot, breathe, wave  # noqa: E402

PLAIN = SRC / 'art/plain.webp'
R.add_pose('blush', SRC / 'art/blush.webp', 1000)
R.add_pose('angry', SRC / 'art/angry.webp', 1050)


def act_blush(anim, hp, cp, n):
    """Flattered: a bashful twist side to side, a little bounce."""
    body(anim, hp, cp, n, squash=lambda f: -4 * abs(math.sin(math.pi * f / 26)), rot=lambda f: wave(f, 34, 0.05))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 34, 0.04, 1))


def act_angry(anim, hp, cp, n):
    """Comic anger: stamping hops with a fast shake."""
    body(anim, hp, cp, n, squash=lambda f: 9 * abs(math.sin(math.pi * f / 9)), dx=lambda f: wave(f, 4, 3.0), rot=lambda f: wave(f, 9, 0.03))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 9, 0.06))


A = R.ACTS
SHOTS = {
    'blush': dict(pose='blush', act=act_blush, frames=372, bg=PLAIN),        # 0.0  thinks she was complimented
    'stunned': dict(pose='stunned', act=A['stun'], frames=84, bg=PLAIN),     # 6.2  おめでたい人だね
    'angry': dict(pose='angry', act=act_angry, frames=120, bg=PLAIN),        # 7.6  at the friend
    'success': dict(pose='success', act=A['success'], frames=204, bg=PLAIN),  # 9.6  saved, into review
}

if __name__ == '__main__':
    only = sys.argv[1:]
    R.build_shots({k: v for k, v in SHOTS.items() if not only or k in only}, SRC / 'rive')
