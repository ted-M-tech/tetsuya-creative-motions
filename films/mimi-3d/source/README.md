# Mimi 3D — source (v1 snapshot)

Snapshot of the approved v1 (2026-10-20). The master copy, including `mimi.blend`, is in Lanclo's product repository at `design/mimi-3d/`.

Mimi as a soft matte vinyl toy, built entirely by Python in Blender 5.2 and rendered with Cycles. Target look: `source/ref/codex/toy-look.png` (generated with Codex from the 2D mascot art).

```sh
cd films/mimi-3d/source
blender -b -P scripts/mimi.py -- --out renders/sheet --views hero:-28,front:0 --samples 128 --exposure -1.0 --save renders/mimi.blend
blender -b -P scripts/mimi.py -- --out renders/t --views hero:-28 --samples 24 --pct 40 --exposure -1.0   # quick look
blender -b -P scripts/check_overlap.py      # parts must not intersect (band x ears, band x head)
blender -b -P scripts/anim_hop.py -- --out renders/hop/ --eevee --pct 50   # rig motion test
scripts/review_round.sh r1                  # one art-director round with codex-p against the target
```

## How it was finished

Claude builds and renders; codex-p reviews each render beside the target (`scripts/review_prompt.txt`) and returns ranked fixes with numbers. Claude decides what to take, then re-checks part intersections and renders again. Nine rounds; the last verdict was SHIP.

- Lock what the reviewer keeps flipping: camera yaw/framing and lighting/exposure were fixed by the director after the reviewer reversed itself twice, and the prompt says so.
- Client decisions go into the prompt (full torso, outward-leaning upright ear) so they are not undone.
- Paint flat inlays (ear panels, blush) in the shader rather than as geometry: cut-out geometry gave holes and stair-stepped edges.
- Quick looks at 40-60 % and 24-64 samples; full quality only for the final sheet (`--samples 160`, about 30 s per 1080x1920 frame on an M5 Pro).

Known limit: automatic weights on the fused body smear a little when an arm is raised high (wave pose); hand-tune weights before close-up acting shots.

- `scripts/mimi.py`: fused body (joined ellipsoids, voxel remesh, smoothing), paddle ears with inner panels, face decals placed by ray casts, shader blush, headphones, armature (root, torso, head, ears, arms) with automatic weights, studio sweep and lights.
- `scripts/check_overlap.py`: BVH intersection report between parts.
- `scripts/anim_hop.py`: posing the rig per frame.

Mimi and the Lanclo mark are Lanclo's; not licensed for reuse.
