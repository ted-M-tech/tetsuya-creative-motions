"""「写真で英語」: every Rive shot of the episode -> rive/<shot>/ (then scripts/render.sh).

Mimi stands beside the real app screen, so the shots use a flat plate (art/plain.webp, the page colour) and the edit
scales and moves them to the left without a visible edge.
usage: uv run --no-project --with scipy --with pillow --with numpy python films/mimi-shashin/source/scripts/shots.py [shot ...]
"""
import math
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC.parents[2] / 'kits/mimi-short/scripts'))
import rig2d as R  # noqa: E402
from rig2d import body, bone_rot, breathe, smooth, wave  # noqa: E402

PLAIN = SRC / 'art/plain.webp'


def talk(voice, cache, start, nod_at):
    def act(anim, hp, cp, n):
        """Speaks the line (mouth from the voice), a small nod at nod_at."""
        body(anim, hp, cp, n, squash=lambda f: breathe(f) + (10 * max(0.0, math.sin(math.pi * (f - nod_at) / 14)) if nod_at <= f < nod_at + 14 else 0),
             rot=lambda f: wave(f, 40, 0.02))
        bone_rot(anim, '0:41', n, lambda f: wave(f, 20, 0.04))
        R.lipsync(anim, start, SRC / 'assets/voice' / voice, SRC / 'scripts' / cache)
    return act


def act_present(anim, hp, cp, n):
    """Points at the phone: the pointing arm beats gently, a friendly bounce."""
    body(anim, hp, cp, n, squash=lambda f: -3 * abs(math.sin(math.pi * f / 30)), rot=lambda f: 0.02 * smooth(f / 12))
    bone_rot(anim, '0:45', n, lambda f: wave(f, 30, 0.05))
    bone_rot(anim, '0:41', n, lambda f: wave(f, 36, 0.05, 1))


A = R.ACTS
SHOTS = {
    'hook': dict(pose='speak', act=talk('rough-af_heart.wav', 'lipsync-rough.json', 12, 110), frames=126, bg=PLAIN),  # 0.0  "People is sitting... at a cafe."
    'present': dict(pose='point', act=act_present, frames=90, bg=PLAIN),                                               # 2.1  points at the app
    'record': dict(pose='speak', act=talk('rough-af_heart.wav', 'lipsync-rough.json', 18, 200), frames=132, bg=PLAIN), # 3.6  says it into the app (3.9)
    'think': dict(pose='think', act=A['think'], frames=108, bg=PLAIN),                                                 # 5.8  reads the feedback
    'point2': dict(pose='point', act=act_present, frames=96, bg=PLAIN),                                                # 7.6  is -> are
    'listen': dict(pose='listen', act=A['listen'], frames=180, bg=PLAIN),                                              # 9.2  her own voice, a better sentence
    'jump': dict(pose='jump', act=A['jump'], frames=42, bg=PLAIN),                                                     # 12.2
    'success': dict(pose='success', act=A['success'], frames=66, bg=PLAIN),                                            # 12.9
}

if __name__ == '__main__':
    only = sys.argv[1:]
    R.build_shots({k: v for k, v in SHOTS.items() if not only or k in only}, SRC / 'rive')
