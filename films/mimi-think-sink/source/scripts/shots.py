"""「think が sink に」: every Rive shot of the episode -> rive/<shot>/ (then scripts/render.sh).

usage: uv run --no-project --with scipy --with pillow --with numpy python films/mimi-think-sink/source/scripts/shots.py
"""
import math
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
import rig2d as R  # noqa: E402
from rig2d import body, bone_rot, breathe, smooth, spring, wave  # noqa: E402

# confident, stunned: drawn for this film (../prompts/01-codex-poses-and-props.txt), now in the library.


def act_boast(anim, hp, cp, n):
    """Showing off: leans back, finger wags in time with the words, a proud bounce."""
    body(anim, hp, cp, n, squash=lambda f: -5 * abs(math.sin(math.pi * f / 22)), rot=lambda f: -0.04 * smooth(f / 14) + wave(f, 44, 0.015))
    bone_rot(anim, '0:45', n, lambda f: wave(f, 11, 0.06))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 22, 0.05, 1))


def act_stun(anim, hp, cp, n):
    """Hit by the sink: a jolt at frame 0, then frozen with a fine tremble; the second sink lands at IMPACT2."""
    impact2 = 48
    jolt = lambda f: spring(f, 0, -18, 10, 0.12) + spring(f, impact2, 12, 8, 0.15)
    body(anim, hp, cp, n, squash=jolt, dx=lambda f: wave(f, 3, 1.6), rot=lambda f: wave(f, 3, 0.006))
    bone_rot(anim, '0:41', n, lambda f: spring(f, 0, 0.1, 10) + spring(f, impact2, 0.08, 8))


def act_say(anim, hp, cp, n):
    """Practice: says the line with the model; mouth from the model clip's syllables, a small nod after."""
    body(anim, hp, cp, n, squash=lambda f: breathe(f) + (10 * max(0.0, math.sin(math.pi * (f - 90) / 14)) if 90 <= f < 104 else 0),
         rot=lambda f: wave(f, 40, 0.02))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 20, 0.04))
    # the clip's speech starts 0.27 s in (placed at SAY - 0.04 with 0.23 s trimmed, so clip time 0 falls on shot frame 8)
    R.lipsync(anim, 8, SRC / 'assets/own-voice/right.wav', SRC / 'scripts/lipsync-right.json')


A = R.ACTS
SHOTS = {
    'hook': dict(pose='confident', act=act_boast, frames=60),       # 0.0  "I sink so!"; the first sink drops
    'stun': dict(pose='stunned', act=act_stun, frames=72),          # 1.0  frozen; the second sink at 1.8
    'reach': dict(pose='reach', act=A['reach'], frames=42),         # 2.2  taps Lanclo (frame 26 = 2.63 s)
    'listen': dict(pose='listen', act=A['listen'], frames=90),      # 2.9  hears her own voice say "think"
    'perk': dict(pose='perk', act=A['perk'], frames=36),            # 4.4  realises
    'think': dict(pose='think', act=A['think'], frames=108),        # 5.0  reads the result card, nods
    'practice': dict(pose='speak', act=act_say, frames=132),        # 6.8  says it with the model
    'clear': dict(pose='perk', act=A['perk'], frames=72),           # 9.0  the sinks poof away, a bulb lights
    'jump': dict(pose='jump', act=A['jump'], frames=42),            # 10.2
    'success': dict(pose='success', act=A['success'], frames=72),   # 10.9
    'proud': dict(pose='confident', act=act_boast, frames=114),     # 12.1 "I think so." for real
}

if __name__ == '__main__':
    only = sys.argv[1:]
    R.build_shots({k: v for k, v in SHOTS.items() if not only or k in only}, SRC / 'rive')
