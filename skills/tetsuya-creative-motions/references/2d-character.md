# 2D characters (Rive)

Default for recurring mascot shorts. Full guide: `docs/2D-CHARACTER-ANIMATION.md`; worked record: `films/mimi-jibun-no-koe/` in the private vault (tetsuya-creative-motions-vault).

- Keep the approved art style: draw new poses with an image model (`codex-p`), always attaching the official PNGs and earlier poses; specify line, colours, proportions, accessory side, the same three-quarter direction, scale, white background, no text. Use official art where it fits.
- Cut out by flood-filling white from the corners; cut lip-sync pairs with one shared crop. Match pose scale by head size; plant feet on one spot; review a sheet of all poses before animating.
- Rig like `design/mimi-welcome/build_scene.py` in Lanclo: grid + Delaunay mesh, position weights, five bones, acting as keyed bones. Lip-sync by showing an open-mouth skin on syllable peaks.
- Rive CLI: look up `rive docs`/`rive schema`; first sibling draws on top; one screenshot per call; screenshots are opaque, so the background lives in the artboard and the camera in HyperFrames.
- Edit in HyperFrames; captions at the top, bottom ~400 px clear, labels large, never over the face.
- Review the storyboard and the final cut with Codex as a short-form director; ship on SHIP plus the owner's approval.
- Record everything per `docs/ADDING-A-FILM.md` (full record in the private vault, summary in public) so the work can be rebuilt.
