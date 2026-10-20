"""Find bone rotation signs: render a grid of ear/arm/head poses.  blender -b -P scripts/pose_test.py"""
import math
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent.parent / 'mimi-3d' / 'source' / 'scripts'))
import mimi as M  # noqa: E402

M.ARGS[:] = []
M.reset()
rig, _ = M.build()
cam = M.stage(False)
scn = bpy.context.scene
scn.render.resolution_percentage = 25
M.aim(cam, -15, dist=5.0, height=0.9, target=(0, 0, 0.75))
pb = rig.pose.bones
for b in pb:
    if b.name != 'head':
        b.rotation_mode = 'XYZ'
tests = [('earL_x+60', 'ear-1', (60, 0, 0)), ('earL_x-60', 'ear-1', (-60, 0, 0)), ('earL_z+60', 'ear-1', (0, 0, 60)),
         ('earR_x+70', 'ear1', (70, 0, 0)), ('earR_x-70', 'ear1', (-70, 0, 0)), ('earR_z-60', 'ear1', (0, 0, -60)),
         ('armR_x-80', 'arm1', (-80, 0, 0)), ('armR_z+60', 'arm1', (0, 0, 60))]
for label, bone, rot in tests:
    for b in pb:
        if b.name != 'head':
            b.rotation_euler = (0, 0, 0)
    pb[bone].rotation_euler = tuple(math.radians(r) for r in rot)
    scn.render.filepath = str(ROOT / f'renders/pose/{label}.png')
    bpy.ops.render.render(write_still=True)
