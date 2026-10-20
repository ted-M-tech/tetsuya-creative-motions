# Mimi 3D (work in progress)

Mimi as a soft matte vinyl toy, built entirely by Python in Blender 5.2 and rendered with Cycles. Target look: `source/ref/codex/toy-look.png` (generated with Codex from the 2D mascot art).

```sh
cd films/mimi-3d/source
blender -b -P scripts/mimi.py -- --out renders/sheet --views hero:-28,front:0 --samples 128 --exposure -1.0 --save renders/mimi.blend
blender -b -P scripts/mimi.py -- --out renders/t --views hero:-28 --samples 24 --pct 40 --exposure -1.0   # quick look
blender -b -P scripts/check_overlap.py      # parts must not intersect (band x ears, band x head)
blender -b -P scripts/anim_hop.py -- --out renders/hop/ --eevee --pct 50   # rig motion test
```

- `scripts/mimi.py`: fused body (joined ellipsoids, voxel remesh, smoothing), paddle ears with inner panels, face decals placed by ray casts, shader blush, headphones, armature (root, torso, head, ears, arms) with automatic weights, studio sweep and lights.
- `scripts/check_overlap.py`: BVH intersection report between parts.
- `scripts/anim_hop.py`: posing the rig per frame.

Mimi and the Lanclo mark are Lanclo's; not licensed for reuse.
