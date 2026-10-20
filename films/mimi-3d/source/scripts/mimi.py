"""Mimi as a soft matte vinyl toy: one fused body mesh, armature rig, face decals, headphones, studio stage.

usage: blender -b -P scripts/mimi.py -- [--out renders/v5] [--save renders/mimi.blend] [--eevee] [--samples 96]
Character faces -Y, Z up, about 1.4 tall to the ear tips. Other scripts import build() / stage() / aim().
"""
import math
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector, Matrix

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ROOT = Path(__file__).resolve().parent.parent
FONT = '/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf'


def arg(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else default


def lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


def material(name, color, rough=0.6, sss=0.0, sheen=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(color)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Subsurface Weight'].default_value = sss
    b.inputs['Subsurface Radius'].default_value = (0.05, 0.04, 0.035)
    b.inputs['Subsurface Scale'].default_value = 0.4
    b.inputs['Sheen Weight'].default_value = sheen
    b.inputs['Coat Weight'].default_value = coat
    b.inputs['Specular IOR Level'].default_value = 0.35
    return m


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def link(o):
    bpy.context.collection.objects.link(o)
    return o


def ellipsoid(name, loc, size, mat=None, seg=48, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def shape(o, fn):
    """Move every vertex (object space) through fn(Vector) -> Vector."""
    for v in o.data.vertices:
        v.co = fn(v.co.copy())


def apply_mods(o):
    bpy.context.view_layer.objects.active = o
    for m in list(o.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)


HEAD_C = Vector((0, 0, 0.77))


def fused_body(mat):
    """Head, torso, legs and hugging arms as one soft mesh (voxel remesh + smoothing)."""
    parts = []
    head = ellipsoid('p_head', HEAD_C, (0.40, 0.34, 0.315))
    # mochi head: fuller cheeks low, slightly flatter crown
    shape(head, lambda c: Vector((c.x * (1 + 0.07 * max(0, -c.z / 0.3)), c.y, c.z * (0.97 if c.z > 0 else 1.0))))
    parts.append(head)
    torso = ellipsoid('p_torso', (0, 0.01, 0.28), (0.255, 0.225, 0.245))
    shape(torso, lambda c: Vector((c.x * (1 + 0.1 * max(0, -c.z / 0.25)), c.y * (1 + 0.06 * max(0, -c.z / 0.25)), c.z)))
    parts.append(torso)
    for s in (-1, 1):
        parts.append(ellipsoid(f'p_leg{s}', (0.105 * s, -0.01, 0.07), (0.11, 0.115, 0.09)))
        arm = ellipsoid(f'p_arm{s}', (0.155 * s, -0.165, 0.37), (0.078, 0.07, 0.08), rot=(math.radians(-20), math.radians(22 * s), 0))
        parts.append(arm)
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = head
    bpy.ops.object.join()
    body = bpy.context.object
    body.name = 'body'
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    rm = body.modifiers.new('remesh', 'REMESH')
    rm.mode, rm.voxel_size = 'VOXEL', 0.006
    sm = body.modifiers.new('smooth', 'CORRECTIVE_SMOOTH')
    sm.factor, sm.iterations, sm.smooth_type = 0.9, 8, 'SIMPLE'
    sm.use_only_smooth = True
    apply_mods(body)
    lap = body.modifiers.new('lap', 'LAPLACIANSMOOTH')
    lap.lambda_factor, lap.iterations = 0.6, 6
    apply_mods(body)
    for p in body.data.polygons:
        p.use_smooth = True
    body.data.materials.append(mat)
    return body


def surface(body, x, z):
    """Point on the body surface hit by a ray from the front at (x, z), plus its normal (body has identity transform)."""
    ok, loc, nrm, _ = body.ray_cast(Vector((x, -2.0, z)), Vector((0, 1, 0)))
    assert ok, (x, z)
    return loc, nrm


def decal(name, body, x, z, size, mat, lift=0.0):
    """A thin ellipsoid lying on the surface (eyes, cheeks, nose)."""
    loc, nrm = surface(body, x, z)
    o = ellipsoid(name, (0, 0, 0), size, mat, seg=32)
    o.matrix_world = Matrix.Translation(loc + nrm * lift) @ nrm.to_track_quat('-Y', 'Z').to_matrix().to_4x4()
    return o


def ear(name, s, tilt, flop, mats):
    """Paddle ear: narrow root, wide rounded middle, flat blue inner panel on the front."""
    e = ellipsoid(name, (0, 0, 0.28), (0.15, 0.085, 0.285), mats['white'])
    bpy.ops.object.transform_apply(location=True)  # mesh starts at the ear root, origin at the pivot
    shape(e, lambda c: Vector((c.x * (0.55 + 0.45 * min(1, max(0, c.z / 0.22))), c.y * (0.8 + 0.2 * min(1, c.z / 0.3)), c.z)))
    inner = ellipsoid(name + '_in', (0, -0.072, 0.31), (0.102, 0.014, 0.205), mats['blue'])
    shape(inner, lambda c: Vector((c.x * (0.7 + 0.3 * min(1, max(0, (c.z - 0.1) / 0.2))), c.y, c.z)))
    inner.parent = e
    base = HEAD_C + Vector((0.13 * s, -0.03, 0.245))
    e.matrix_world = Matrix.Translation(base) @ (Matrix.Rotation(math.radians(tilt), 4, 'Y') @
                                                Matrix.Rotation(math.radians(8), 4, 'X') @
                                                Matrix.Rotation(math.radians(flop), 4, 'Z'))
    return e, base


def headphones(mats):
    objs = []
    bpy.ops.mesh.primitive_torus_add(major_radius=0.435, minor_radius=0.036, major_segments=96, minor_segments=16,
                                     location=HEAD_C + Vector((0, 0.04, -0.01)), rotation=(math.radians(90), 0, 0))
    band = bpy.context.object
    band.name = 'band'
    band.scale = (1, 1, 1.7)  # flat strap: wider front-to-back than thick
    bpy.ops.object.transform_apply(scale=True)
    bm = bmesh.new()
    bm.from_mesh(band.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if (band.matrix_world @ v.co).z < HEAD_C.z - 0.03], context='VERTS')
    bm.to_mesh(band.data)
    bm.free()
    bpy.ops.object.transform_apply(location=True, rotation=True)
    pivot = HEAD_C + Vector((0, 0.04, -0.03))
    band.data.transform(Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(-24), 4, "X") @ Matrix.Translation(-pivot))
    band.data.materials.append(mats['navy'])
    for p in band.data.polygons:
        p.use_smooth = True
    objs.append(band)
    for s in (-1, 1):
        c = HEAD_C + Vector((0.415 * s, 0.035, -0.03))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.12, vertices=96, location=c, rotation=(0, math.radians(90), 0))
        cup = bpy.context.object
        cup.name = f'cup{s}'
        b = cup.modifiers.new('bev', 'BEVEL')
        b.width, b.segments, b.limit_method = 0.035, 8, 'ANGLE'
        cup.data.materials.append(mats['navy'])
        bpy.ops.mesh.primitive_cylinder_add(radius=0.138, depth=0.045, vertices=96, location=c + Vector((0.07 * s, 0, 0)),
                                            rotation=(0, math.radians(90), 0))
        face = bpy.context.object
        face.name = f'cupface{s}'
        b = face.modifiers.new('bev', 'BEVEL')
        b.width, b.segments, b.limit_method = 0.02, 8, 'ANGLE'
        face.data.materials.append(mats['blue'])
        for o in (cup, face):
            for p in o.data.polygons:
                p.use_smooth = True
            o.data.shade_auto_smooth() if hasattr(o.data, 'shade_auto_smooth') else None
        objs += [cup, face]
        if s == -1:
            bpy.ops.object.text_add(location=c + Vector((0.093 * s, 0, 0)), rotation=(math.radians(90), 0, math.radians(-90)))
            t = bpy.context.object
            t.name = 'L'
            t.data.body = 'L'
            t.data.font = bpy.data.fonts.load(FONT)
            t.data.align_x, t.data.align_y = 'CENTER', 'CENTER'
            t.data.size, t.data.extrude, t.data.bevel_depth = 0.15, 0.003, 0.002
            t.data.materials.append(mats['letter'])
            objs.append(t)
    return objs


def mouth_curve(body, mat):
    cu = bpy.data.curves.new('mouth', 'CURVE')
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution = '3D', 0.0082, 4
    cu.use_fill_caps = True
    sp = cu.splines.new('POLY')
    pts = []
    for i in range(41):
        t = i / 20 - 1
        loc, nrm = surface(body, 0.058 * t, HEAD_C.z - 0.11 - 0.024 * abs(math.sin(math.pi * t)) + 0.006 * (abs(t) > 0.9))
        pts.append(loc + nrm * 0.002)
    sp.points.add(len(pts) - 1)
    for pt, co in zip(sp.points, pts):
        pt.co = (*co, 1)
    o = link(bpy.data.objects.new('mouth', cu))
    cu.materials.append(mat)
    return o


def blush(mat, point, radius=0.07, color='#f7a2b2'):
    """Soft cheek blush painted into the body shader around a surface point (no geometry)."""
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    src = bsdf.inputs['Base Color'].links[0].from_socket if bsdf.inputs['Base Color'].is_linked else None
    coord = nt.nodes.get('coord') or nt.nodes.new('ShaderNodeTexCoord')
    coord.name = 'coord'
    dist = nt.nodes.new('ShaderNodeVectorMath')
    dist.operation = 'DISTANCE'
    dist.inputs[1].default_value = point
    nt.links.new(coord.outputs['Object'], dist.inputs[0])
    ramp = nt.nodes.new('ShaderNodeMapRange')
    ramp.interpolation_type = 'SMOOTHERSTEP'
    ramp.inputs['From Min'].default_value, ramp.inputs['From Max'].default_value = radius * 0.35, radius
    ramp.inputs['To Min'].default_value, ramp.inputs['To Max'].default_value = 0.85, 0.0
    nt.links.new(dist.outputs['Value'], ramp.inputs['Value'])
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    if src:
        nt.links.new(src, mix.inputs['A'])
    else:
        mix.inputs['A'].default_value = bsdf.inputs['Base Color'].default_value
    mix.inputs['B'].default_value = lin(color)
    nt.links.new(ramp.outputs['Result'], mix.inputs['Factor'])
    nt.links.new(mix.outputs['Result'], bsdf.inputs['Base Color'])


def build():
    mats = dict(white=material('vinyl_white', '#f5f6f9', 0.58, sss=0.04, sheen=0.2),
                blue=material('vinyl_blue', '#3f8ff0', 0.5), navy=material('vinyl_navy', '#1b2f6b', 0.42, coat=0.12),
                eye=material('eye', '#172a5c', 0.08, coat=1.0), pink=material('cheek', '#f6a9b4', 0.75),
                shine=material('shine', '#ffffff', 0.3), letter=material('letter', '#ffffff', 0.45))
    body = fused_body(mats['white'])
    face = []
    for s in (-1, 1):
        face.append(decal(f'eye{s}', body, 0.168 * s, HEAD_C.z - 0.055, (0.06, 0.022, 0.072), mats['eye'], 0.004))
        loc, nrm = surface(body, 0.168 * s + 0.022, HEAD_C.z - 0.022)
        face.append(ellipsoid(f'eyehi{s}', loc + nrm * 0.022, (0.021, 0.012, 0.021), mats['shine'], 24))
        loc, nrm = surface(body, 0.168 * s - 0.02, HEAD_C.z - 0.09)
        face.append(ellipsoid(f'eyehi2{s}', loc + nrm * 0.02, (0.009, 0.006, 0.009), mats['shine'], 16))
        blush(mats['white'], surface(body, 0.245 * s, HEAD_C.z - 0.12)[0])
    face.append(decal('nose', body, 0, HEAD_C.z - 0.078, (0.02, 0.012, 0.014), mats['eye'], -0.002))
    face.append(mouth_curve(body, mats['eye']))
    ears = {}
    for s, tilt, flop in ((-1, -62, 6), (1, 8, -6)):
        ears[s] = ear(f'ear{s}', s, tilt, flop, mats)
    gear = headphones(mats)
    root = rig(body, face + gear, ears)
    return root, mats


def rig(body, head_parts, ears):
    """Armature: root > torso > head > ear.L/R, plus arm bones; body skinned with automatic weights."""
    arm = bpy.data.armatures.new('rig')
    ob = link(bpy.data.objects.new('Mimi', arm))
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.edit_bones

    def bone(name, head, tail, parent=None):
        b = eb.new(name)
        b.head, b.tail = head, tail
        if parent:
            b.parent = eb[parent]
        return b

    bone('root', (0, 0, 0), (0, 0.15, 0))
    bone('torso', (0, 0, 0.12), (0, 0, 0.46), 'root')
    bone('head', (0, 0, 0.5), (0, 0, 1.0), 'torso')
    for s, (e, base) in ears.items():
        tip = base + e.matrix_world.to_3x3() @ Vector((0, 0, 0.45))
        bone(f'ear{s}', base, tip, 'head')
    for s in (-1, 1):
        bone(f'arm{s}', (0.12 * s, -0.06, 0.42), (0.16 * s, -0.17, 0.27), 'torso')
    bpy.ops.object.mode_set(mode='OBJECT')
    # skin the fused body; rigid parts follow their bone
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

    def to_bone(o, name):
        mw = o.matrix_world.copy()
        o.parent, o.parent_type, o.parent_bone = ob, 'BONE', name
        bpy.context.view_layer.update()
        o.matrix_world = mw

    for o in head_parts:
        to_bone(o, 'head')
    for s, (e, _) in ears.items():
        to_bone(e, f'ear{s}')
    return ob


def stage(cycles=True, samples=96):
    scn = bpy.context.scene
    if cycles:
        scn.render.engine = 'CYCLES'
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'METAL'
        bpy.context.preferences.addons['cycles'].preferences.get_devices()
        for d in bpy.context.preferences.addons['cycles'].preferences.devices:
            d.use = True
        scn.cycles.device = 'GPU'
        scn.cycles.samples = samples
        scn.cycles.use_denoising = True
    else:
        scn.render.engine = 'BLENDER_EEVEE'
    scn.render.resolution_x, scn.render.resolution_y = 1080, 1920
    scn.render.resolution_percentage = int(arg('--pct', 100))
    scn.view_settings.view_transform = arg('--view', 'Standard')
    scn.view_settings.exposure = float(arg('--exposure', 0.0))
    world = bpy.data.worlds.new('world')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = lin('#f3f6fa')
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
    scn.world = world
    # seamless sweep: floor curving up into a back wall
    bpy.ops.mesh.primitive_plane_add(size=1)
    sweep = bpy.context.object
    sweep.name = 'sweep'
    bm = bmesh.new()
    rows = []
    for i in range(40):
        a = i / 39
        y = -6 + 9 * a if a < 0.7 else 0.3 + 1.2 * math.sin((a - 0.7) / 0.3 * math.pi / 2)
        z = 0 if a < 0.7 else 1.2 * (1 - math.cos((a - 0.7) / 0.3 * math.pi / 2)) + 2.5 * max(0, a - 0.95) / 0.05
        rows.append([bm.verts.new((x, y + 2.2, z)) for x in (-8, 8)])
    for r0, r1 in zip(rows, rows[1:]):
        bm.faces.new((r0[0], r0[1], r1[1], r1[0]))
    bm.to_mesh(sweep.data)
    bm.free()
    for p in sweep.data.polygons:
        p.use_smooth = True
    bg = material('sweep', '#f2f5f9', 0.9)
    b = bg.node_tree.nodes['Principled BSDF']
    b.inputs['Emission Color'].default_value = lin('#eef3f9')
    b.inputs['Emission Strength'].default_value = float(arg('--bg', 0.45))
    sweep.data.materials.append(bg)

    def area(name, loc, energy, size, color='#ffffff'):
        d = bpy.data.lights.new(name, 'AREA')
        d.energy, d.size, d.color = energy, size, lin(color)[:3]
        o = link(bpy.data.objects.new(name, d))
        o.location = loc
        o.rotation_mode = 'QUATERNION'
        o.rotation_quaternion = (Vector((0, 0, 0.6)) - Vector(loc)).to_track_quat('-Z', 'Y')

    area('key', (-2.0, -2.6, 2.8), 230, 3.0, '#fff6ee')
    area('fill', (2.6, -2.0, 1.4), 45, 3.5, '#eef3ff')
    area('rim', (1.2, 2.2, 2.6), 90, 2.0)
    area('top', (0, -0.4, 3.4), 35, 3.0)
    cam = link(bpy.data.objects.new('cam', bpy.data.cameras.new('cam')))
    cam.data.lens = 70
    scn.camera = cam
    return cam


def aim(cam, yaw_deg, dist=4.3, height=0.75, target=(0, 0, 0.66)):
    a = math.radians(yaw_deg)
    cam.location = (dist * math.sin(a), -dist * math.cos(a), height)
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = (Vector(target) - cam.location).to_track_quat('-Z', 'Y')


def main():
    reset()
    build()
    cam = stage(not ('--eevee' in ARGS), int(arg('--samples', 96)))
    if arg('--save'):
        bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / arg('--save')))
    out = arg('--out')
    if out:
        views = arg('--views', 'hero:-28,front:0,side:-90,back:180')
        for item in views.split(','):
            label, yaw = item.split(':')
            aim(cam, float(yaw))
            bpy.context.scene.render.filepath = str(ROOT / f'{out}-{label}.png')
            bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    main()
