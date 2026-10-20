# 「自分の声、むり」 — source

15-second vertical Mimi short for Reels/TikTok, in the official 2D illustration style (chosen over 3D after a side-by-side comparison).

## Pipeline

1. **Poses** — drawn by Codex (`codex-p`) from the approved Mimi PNGs: `art/hide, droop, perk, reach, hide-reach, peek, jump`, plus `speak-open/closed` (one pose, two mouths, cut with one shared crop for lip-sync); official `listening, success, master` used as is. Desk background `art/bg-desk.png` drawn the same way.
2. **Cut-outs** — `scripts/cutout.sh <pose>` (white flood fill from the corners) → `art/cut/`.
3. **Rig and acting** — `scripts/rig2d.py` builds one Rive project per shot under `rive/<shot>/`: grid+Delaunay skinned mesh, five bones (head, ears, two paws, contact), performances as keyed bones (shiver, reach and tap, droop, pop, hop...); the practice shot swaps the open-mouth skin on syllable peaks of the model voice. Pose scale is tuned so the head reads the same size in every pose.
4. **Frames** — `scripts/render_rive.sh <shot> <frames>`: one headless `rive --screenshot --advance=N` per frame, 4 in parallel → `renders/rive/<shot>.mp4`. Rive screenshots are opaque, so the background is inside the artboard; the camera lives in HyperFrames.
5. **Sound** — `scripts/mix.py`: the LP voice clips (own take and her-voice model), code-made SFX and a 100 BPM bed ducked under the voices → `hf-short/assets/mix.wav`.
6. **Edit** — `hf-short/` (HyperFrames): shots back to back inside one camera wrapper, Lanclo UI on the phone screen, captions, playback tags, rewind treatment, sparkles, end card. `npx hyperframes check`, then `npx hyperframes render --output ../renders/mimi-jibun-no-koe.mp4 --fps 60`.

Earlier stages kept for reference: `scripts/previs.py` + `animatic.py` (3D previs and animatic), `hf-hook/` (the approved 1.3 s hook test), `scripts/npr.py` (3D toon comparison).

Rive rules that bite: the first sibling draws on top; one screenshot per invocation; no transparent background.
`assets/voice/` and rendered media are not in Git.
