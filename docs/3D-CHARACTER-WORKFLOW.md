# 3D character workflow

**English** · [日本語](3D-CHARACTER-WORKFLOW.ja.md)

How to turn a 2D character into a 3D master and use it for short animations, as done for Mimi (Lanclo). The full record is in [films/mimi-3d](../films/mimi-3d/PROCESS.md) (Japanese); a ready-to-use instruction is in [films/mimi-3d/PROMPT.md](../films/mimi-3d/PROMPT.md) (Japanese).

## Approach

- **Build the character once in 3D and reuse it.** Generating the character with AI video every time drifts on details such as logos, markings and colours.
- **Script everything.** Run Blender headless so the same script always rebuilds the same model. Adjust interactively over MCP, then port the change back to the script.
- **Split the roles between two agents.** Claude Code builds, renders and decides; Codex (`codex-p`) generates reference images and reviews.

## Tools

| Tool | Role | Install |
|---|---|---|
| Blender 5.2 LTS | Model, rig, render (Cycles / EEVEE) | `brew install --cask blender` |
| mcp-for-blender | Drive a running Blender from Claude and Codex | `claude mcp add --scope user blender -- uvx mcp-for-blender`; `codex-p mcp add blender -- uvx mcp-for-blender`; `uvx mcp-for-blender install-addon`, enable it, click "Start MCP Server" |
| blender-production-skills | Scenes and environments, validation habits | Clone `XliuXjianX/blender-production-skills` and link each skill into the Claude and Codex skill folders |
| Codex (`codex-p`) | Reference images; art-director reviews | `codex-p exec --image a.png,b.png - < prompt.txt` (prompt on stdin) |
| HyperFrames | Captions, titles, sound, end card | hyperframes skills for Claude; the official `hyperframes` plugin for Codex |

Skip `uvx mcp-for-blender setup`: it also edits Cursor and other unrelated clients. Considered and not adopted as the main path: img2threejs (outputs Three.js; use it for web 3D) and image-to-3D generators (Meshy, Tripo, Hunyuan3D; messy topology and fused parts, fine only as a proportion guide).

## 1. Make the character master

1. Generate a turnaround and a "finished look" target from the 2D art; have the owner approve the target.
2. Fuse ellipsoids into one soft body (join, voxel remesh, smooth). Accessories stay separate.
3. Place eyes, nose and mouth by ray casts onto the face. Paint flat markings (cheeks, inner ears) in the shader.
4. Minimal rig: torso, head, ears, arms. Automatic weights for the body; face and accessories parented to the head bone.
5. Check part intersections numerically (BVH) and keep them at zero.
6. Run review rounds until the reviewer says SHIP.
7. Store the `.blend`, scripts, four-view sheet and identity rules in the owner's repository. Mimi's master is `native-voice-clone/design/mimi-3d/`.

## 2. Make a short

Storyboard 4–6 cuts for 10–30 s; build sets with blender-production-skills, Codex images and Poly Haven assets; keep reusable motions (hop, ear wiggle, surprise, wave) as functions; render hero cuts in Cycles and the rest in EEVEE; edit in HyperFrames from a template. Use AI video only for spectacle cuts, with the 3D render as the reference.

## Review loop

Render, build a "target | current" image, give it and the script to Codex: "strict art director, at most six differences ranked by impact, with function names, numbers and confidence, plus what to keep; SHIP on the first line if it can ship." The director decides, applies, re-checks intersections.

- Write the owner's decisions into the review prompt, or they get undone.
- Lock anything the reviewer reverses twice (Mimi: camera yaw, lighting, hand size).
- Let the reviewer read the code; it found two real bugs.
- `scripts/review_round.sh` runs one round.

## Render settings that worked

Cycles on Metal, Standard view with exposure compensation (AgX desaturated the brand blue), seamless sweep, large soft key, weak fill, rim, with backdrop and lights turning with the camera. Quick looks at 40–60 % and 24–64 samples; final at 160 samples, about 30 s per 1080×1920 frame on an M5 Pro. Too bright a backdrop washes out a white character through floor bounce.

## Where things live

Master in the character owner's repository; public record (process, prompts, reviews, progress images, source snapshot) in `films/<id>/` here; renders never in Git.
