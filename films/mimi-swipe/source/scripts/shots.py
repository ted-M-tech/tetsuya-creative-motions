"""Swipe review: the Rive shot of Mimi beside the real app -> rive/<shot>/ (then scripts/render.sh).

Mimi stands beside the app screen on a flat plate (the page colour); the edit scales and moves her.
The swipe pose is drawn by Codex in art/ and cut out to art/swipe.webp (see README). The two-shots with the friend are
static cut-outs moved in the edit (hf/index.html).
usage: uv run --no-project --with scipy --with pillow --with numpy python films/mimi-swipe/source/scripts/shots.py
"""
import math
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
import rig2d as R  # noqa: E402
from rig2d import body, bone_rot, wave  # noqa: E402

PLAIN = SRC / 'art/plain.webp'
R.add_pose('swipe', SRC / 'art/swipe.webp', 1000)


def act_swipe(anim, hp, cp, n):
    """Into her phone: a happy little bounce and a sway, as if flicking cards."""
    body(anim, hp, cp, n, squash=lambda f: -3 * abs(math.sin(math.pi * f / 30)), rot=lambda f: wave(f, 60, 0.04))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 60, 0.05, 1))


SHOTS = {'swipe': dict(pose='swipe', act=act_swipe, frames=600, bg=PLAIN)}   # the app demo, 10 s

if __name__ == '__main__':
    R.build_shots(SHOTS, SRC / 'rive')
