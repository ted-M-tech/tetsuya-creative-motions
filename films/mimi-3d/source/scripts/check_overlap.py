"""Report mesh pairs that intersect (BVH overlap) after building Mimi.  usage: blender -b -P scripts/check_overlap.py"""
import sys
from pathlib import Path

import bpy
from mathutils.bvhtree import BVHTree

sys.path.insert(0, str(Path(__file__).parent))
import mimi as M  # noqa: E402

M.reset()
M.build()
dg = bpy.context.evaluated_depsgraph_get()
trees = {}
for o in bpy.data.objects:
    if o.type in ('MESH', 'CURVE', 'FONT'):
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        me.transform(o.matrix_world)
        trees[o.name] = BVHTree.FromPolygons([v.co.copy() for v in me.vertices], [p.vertices[:] for p in me.polygons])
        ev.to_mesh_clear()
pairs = [('band', n) for n in trees if n.startswith('ear')] + [('body', n) for n in trees if n.startswith(('cup', 'band'))]
for a, b in pairs:
    hits = trees[a].overlap(trees[b])
    print(f'OVERLAP {a} x {b}: {len(hits)} triangle pairs')
