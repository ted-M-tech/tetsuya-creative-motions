"""Motion test on the armature rig: idle, anticipation, hop, land, wave. Renders a 9:16 PNG sequence.

usage: blender -b -P scripts/anim_hop.py -- --out renders/hop/ [--frames 1-90] [--eevee --pct 50]
"""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).parent))
import mimi as M  # noqa: E402

FPS, N = 30, 90


def spring(t, t0, amp, freq=2.4, decay=6.0):
    return 0.0 if t < t0 else amp * math.exp(-decay * (t - t0)) * math.cos(2 * math.pi * freq * (t - t0))


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def pose(t):
    """Returns root z, squash, neck tilt, ear swing (deg), arm raise (deg), right-arm wave (deg)."""
    breathe = 0.008 * math.sin(2 * math.pi * t / 1.6)
    z, sq, tilt, ear, arm, wave = 0.0, breathe, 0.0, 0.0, 0.0, 0.0
    if 0.5 <= t < 0.8:                      # anticipation
        k = ease((t - 0.5) / 0.3)
        sq, ear, arm = -0.14 * k, 10 * k, -10 * k
    elif 0.8 <= t < 1.45:                   # airborne
        u = (t - 0.8) / 0.65
        z = 0.42 * math.sin(math.pi * u)
        sq = 0.12 * (1 - 2 * abs(u - 0.5)) - 0.02
        ear, arm = -28 * math.cos(math.pi * u), 70 * math.sin(math.pi * u)
    if t >= 1.45:                           # land and settle
        sq = spring(t, 1.45, -0.18, 2.2, 7.0)
        ear = spring(t, 1.45, 24, 1.8, 4.5)
        tilt = 8 * ease((t - 1.9) / 0.4)
    if t >= 2.0:                            # happy wave
        wave = 110 * ease((t - 2.0) / 0.25) + 18 * math.sin(2 * math.pi * 2.2 * (t - 2.0)) * ease((t - 2.1) / 0.2)
    return z, sq, tilt, ear, arm, wave


def main():
    args = M.ARGS
    out = M.ROOT / M.arg('--out', 'renders/hop/')
    a, b = (int(x) for x in M.arg('--frames', f'1-{N}').split('-'))
    M.reset()
    rig, _ = M.build()
    cam = M.stage(not ('--eevee' in args), int(M.arg('--samples', 48)))
    scn = bpy.context.scene
    scn.render.fps = FPS
    cam.data.lens = 50
    M.aim(cam, -24, dist=5.4, height=0.8, target=(0, 0, 0.72))
    pb = rig.pose.bones
    for b_ in pb:
        b_.rotation_mode = 'XYZ'
    for f in range(a, b + 1):
        t = (f - 1) / FPS
        z, sq, tilt, ear, arm, wave = pose(t)
        rig.location = (0, 0, z)
        pb['torso'].scale = (1 - 0.6 * sq, 1 + sq, 1 - 0.6 * sq)  # bone Y is its length axis
        pb['head'].rotation_euler = (0, 0, math.radians(-tilt))
        pb['ear-1'].rotation_euler = (math.radians(ear * 0.5), 0, math.radians(-ear * 0.4))
        pb['ear1'].rotation_euler = (math.radians(ear), 0, math.radians(ear * 0.3))
        pb['arm-1'].rotation_euler = (math.radians(-arm), 0, 0)
        pb['arm1'].rotation_euler = (math.radians(-arm - wave), 0, 0)
        scn.frame_set(f)
        scn.render.filepath = str(out / f'{f:04d}.png')
        bpy.ops.render.render(write_still=True)


main()
