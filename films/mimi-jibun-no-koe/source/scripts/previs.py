"""Previs for 「自分の声、むり」: Mimi on a desk with a phone; one still per key pose and camera.

usage: python3 scripts/screens.py && blender -b -P scripts/previs.py -- [--only S4a,S7b] [--pct 50] [--hq (Cycles)]
Outputs renders/previs/<key>.png. Shot timing lives in shots.py (shared with the animatic).
"""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Vector

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(ROOT.parent.parent / 'mimi-3d' / 'source' / 'scripts'))
import mimi as M  # noqa: E402
from shots import KEYS  # noqa: E402

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []


def arg(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else default


# ---------- phone screens (PNG made beforehand by screens.py; Blender's Python has no PIL) ----------
def screen_image(kind):
    return ROOT / f'renders/previs/screen-{kind}.png'


def screen_material(kind):
    m = bpy.data.materials.new(f'screen_{kind}')
    m.use_nodes = True
    nt = m.node_tree
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(str(screen_image(kind)))
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Strength'].default_value = 1.4
    nt.links.new(tex.outputs['Color'], em.inputs['Color'])
    nt.links.new(em.outputs['Emission'], nt.nodes['Material Output'].inputs['Surface'])
    return m


# ---------- set ----------
def build_set():
    bpy.data.objects['sweep'].hide_render = True
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.6, -0.15))
    desk = bpy.context.object
    desk.name = 'desk'
    desk.scale = (8, 4, 0.3)
    bev = desk.modifiers.new('bev', 'BEVEL')
    bev.width, bev.segments = 0.06, 4
    desk.data.materials.append(M.material('wood', '#ead9c2', 0.6))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 2.4, 2.5), rotation=(math.radians(90), 0, 0))
    wall = bpy.context.object
    wall.name = 'wall'
    wall.scale = (12, 6, 1)
    wall.data.materials.append(M.material('wall', '#f1f5fa', 0.9))
    # phone on a small stand, to Mimi's left in the frame (viewer right), screen angled toward Mimi and camera
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.78, -0.3, 0.82))
    phone = bpy.context.object
    phone.name = 'phone'
    phone.scale = (0.78, 0.07, 1.6)
    phone.rotation_euler = (math.radians(-10), 0, math.radians(24))
    bev = phone.modifiers.new('bev', 'BEVEL')
    bev.width, bev.segments = 0.08, 6
    phone.data.materials.append(M.material('phone', '#1d2733', 0.3, coat=0.5))
    bpy.ops.mesh.primitive_plane_add(size=1)
    scr = bpy.context.object
    scr.name = 'screen'
    scr.parent = phone
    scr.location = (0, -0.52, 0)          # phone-local, just in front of the face
    scr.rotation_euler = (math.radians(90), 0, 0)
    scr.scale = (0.88, 0.94, 1)
    for kind in SCREENS:
        scr.data.materials.append(screen_material(kind))
    return scr


SCREENS = ['rec', 'play', 'model']


def set_screen(scr, kind):
    scr.active_material_index = 0
    for p in scr.data.polygons:
        p.material_index = SCREENS.index(kind)


# ---------- posing ----------
EYE_SCALE = {}


def pose(rig, p):
    pb = rig.pose.bones
    for b in pb:
        if b.name != 'head':
            b.rotation_mode = 'XYZ'
            b.rotation_euler = (0, 0, 0)
            b.location = (0, 0, 0)
            b.scale = (1, 1, 1)
    rig.location = (0, 0, p.get('z', 0))
    rig.rotation_euler = (0, 0, math.radians(p.get('spin', 0)))
    sq = p.get('squash', 0)
    pb['torso'].scale = (1 - 0.5 * sq, 1 + sq, 1 - 0.5 * sq)
    pb['torso'].rotation_euler = (math.radians(p.get('lean', 0)), 0, 0)
    M.tilt_head(rig, p.get('tilt', -8))
    head = pb['head']
    if p.get('nod'):  # positive nods the face down
        head.rotation_quaternion = head.rotation_quaternion @ Euler((math.radians(p['nod']), 0, 0)).to_quaternion()
    pb['ear-1'].rotation_euler = tuple(math.radians(v) for v in p.get('earL', (0, 0, 0)))
    pb['ear1'].rotation_euler = tuple(math.radians(v) for v in p.get('earR', (0, 0, 0)))
    pb['arm-1'].rotation_euler = tuple(math.radians(v) for v in p.get('armL', (0, 0, 0)))
    pb['arm1'].rotation_euler = tuple(math.radians(v) for v in p.get('armR', (0, 0, 0)))
    eyes = p.get('eyes', 1.0)  # <1 squints toward "= =", >1 widens
    for s in (-1, 1):
        e = bpy.data.objects[f'eye{s}']
        EYE_SCALE.setdefault(s, e.scale.copy())
        base = EYE_SCALE[s]
        e.scale = (base.x * (1.15 if eyes > 1 else 1.0), base.y, base.z * eyes)
        bpy.data.objects[f'eyehi{s}'].hide_render = eyes < 0.5


CAMS = {  # name: (lens, location, target)
    'cu': (85, (-1.3, -4.3, 1.15), (-0.05, 0, 0.72)),
    'med': (50, (-0.6, -4.6, 1.3), (0.35, 0, 0.62)),
    'insert': (45, (0.05, -2.4, 0.95), (0.5, -0.25, 0.65)),
    'wide': (35, (0, -5.2, 1.6), (0.2, 0, 0.7)),
}


def frame_camera(cam, name):
    lens, loc, tgt = CAMS[name]
    cam.data.lens = lens
    cam.location = loc
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y')


def main():
    M.ARGS[:] = []
    M.reset()
    rig, _ = M.build()
    cam = M.stage('--hq' in ARGS, 64)
    scn = bpy.context.scene
    scn.render.resolution_percentage = int(arg('--pct', 50))
    scr = build_set()
    if '--npr' in ARGS:
        import npr
        npr.apply()
    only = set(arg('--only', '').split(',')) - {''}
    for key, k in KEYS.items():
        if only and key not in only:
            continue
        pose(rig, k['pose'])
        set_screen(scr, k.get('screen', 'rec'))
        frame_camera(cam, k['cam'])
        scn.render.filepath = str(ROOT / arg('--outdir', 'renders/previs') / f'{key}.png')
        bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    main()
