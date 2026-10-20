# 3D characters (Blender)

Use when a film needs a recurring character in 3D, or when turning 2D art into a 3D master. Full guide: `docs/3D-CHARACTER-WORKFLOW.md`; worked record: `films/mimi-3d/`.

- Build the character once as a scripted Blender master (`blender -b -P build.py`) and reuse it; do not regenerate the character with AI video per shot.
- Before modelling, generate a turnaround and a finished-look target from the 2D art (Codex image generation, prompt on stdin) and get the owner to approve the target.
- One fused soft body (joined ellipsoids → voxel remesh → smooth); accessories as separate parts; face features placed by ray casts; flat markings painted in the shader, never as stuck-on geometry.
- Check part intersections with BVH after every change; keep them at zero.
- Quick looks at 40–60 % and 24–64 samples; full quality only for the sheet.
- Review loop: render "target | current", ask Codex as a strict art director for at most six ranked fixes with function names and numbers and a SHIP/HOLD line; the director decides. Put the owner's decisions in the review prompt. Lock anything the reviewer reverses twice and say so in the prompt.
- Finish with the `.blend`, scripts, four-view sheet and identity rules (silhouette, hex colours, face placement, accessory orientation, bone names, known limits) in the character owner's repository; keep process, prompts and reviews in `films/<id>/`.
- Tools: Blender 5.2, mcp-for-blender for interactive checks (manual `claude mcp add` / `codex-p mcp add`, not the all-clients setup), blender-production-skills for sets, HyperFrames for editing.
