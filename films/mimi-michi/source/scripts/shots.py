"""「道を聞かれて固まる」: every Rive shot of the episode -> rive/<shot>/ (then scripts/render.sh).

usage: uv run --no-project --with scipy --with pillow --with numpy python films/mimi-michi/source/scripts/shots.py [shot ...]
"""
import math
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
import rig2d as R  # noqa: E402
from rig2d import body, bone_rot, breathe, smooth, spring, wave  # noqa: E402

# point, the street plate and the ice: drawn for this film (../prompts/01-codex-street-pose-props.txt), now in the library.
STREET = 'street'


def act_freeze(anim, hp, cp, n):
    """Asked in English: a startled tremble, then the ice forms at frame 36 and she is stock-still."""
    ice = 36
    shake = lambda f: 1.0 if f < ice else 0.0
    body(anim, hp, cp, n, squash=lambda f: spring(f, 0, -10, 10, 0.12) + spring(f, ice, 6, 6, 0.4),
         dx=lambda f: wave(f, 3, 2.0) * shake(f), rot=lambda f: wave(f, 3, 0.008) * shake(f))
    bone_rot(anim, '0:41', n, lambda f: spring(f, 0, 0.08, 10) * shake(f))


def act_say(anim, hp, cp, n):
    """Practice: says the answer with the model; mouth from the voice line, a small nod after."""
    body(anim, hp, cp, n, squash=lambda f: breathe(f) + (10 * max(0.0, math.sin(math.pi * (f - 110) / 14)) if 110 <= f < 124 else 0),
         rot=lambda f: wave(f, 40, 0.02))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 20, 0.04))
    R.lipsync(anim, 24, SRC / 'assets/voice/answer-af_heart.wav', SRC / 'scripts/lipsync-answer.json')


def act_direct(anim, hp, cp, n):
    """Giving directions: the pointing arm beats with the words, a confident little bounce."""
    body(anim, hp, cp, n, squash=lambda f: -4 * abs(math.sin(math.pi * f / 20)), rot=lambda f: 0.02 * smooth(f / 12))
    bone_rot(anim, '0:45', n, lambda f: wave(f, 20, 0.05))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 24, 0.05, 1))


A = R.ACTS
SHOTS = {
    'freeze': dict(pose='stunned', act=act_freeze, frames=174, bg=STREET),   # 0.0  asked the way; ice at 0.6
    'reach': dict(pose='reach', act=A['reach'], frames=42),                   # 2.9  at the desk, taps Lanclo (3.33)
    'listen': dict(pose='listen', act=A['listen'], frames=108),               # 3.6  her own voice gives the answer
    'perk': dict(pose='perk', act=A['perk'], frames=36),                      # 5.4
    'think': dict(pose='think', act=A['think'], frames=108),                  # 6.0  result card
    'practice': dict(pose='speak', act=act_say, frames=132),                  # 7.8  says it with the model
    'thaw': dict(pose='perk', act=A['perk'], frames=72, bg=STREET),           # 10.0 back on the street, the ice shatters
    'direct': dict(pose='point', act=act_direct, frames=108, bg=STREET),      # 11.2 gives the directions
    'thanks': dict(pose='success', act=A['success'], frames=60, bg=STREET),   # 13.0 "Thank you!"
}

if __name__ == '__main__':
    only = sys.argv[1:]
    R.build_shots({k: v for k, v in SHOTS.items() if not only or k in only}, SRC / 'rive')
