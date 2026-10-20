# 2D character animation

**English** · [日本語](2D-CHARACTER-ANIMATION.ja.md)

How to animate an approved 2D character in its own art style for short videos, as done for Mimi's 「自分の声、むり」. The work: [films/mimi-jibun-no-koe](../films/mimi-jibun-no-koe/README.md) (full making-of and prompts are shared privately). For 3D see the [3D character workflow](3D-CHARACTER-WORKFLOW.md).

## 2D or 3D

2D for expression, the exact brand art, fast series production and in-app reuse (Rive); 3D for turns, camera moves and spatial scenes. For Mimi the owner compared the same three poses in 3D, 3D toon and 2D and chose 2D. Duolingo also ships its in-app characters as 2D Rive.

## Tools

Rive CLI (`brew install --cask rive-app/tap/rive-cli`, `rive update`; look up `rive docs` / `rive schema`, the format is newer than model training), Codex (`codex-p exec --image ... - < prompt.txt`) for art and reviews, HyperFrames for the edit, ffmpeg / ImageMagick / Python for cut-outs, encoding and sound.

## Steps

1. Story and a one-second hook (emotional peak + a relatable question), as a timed beat table.
2. Storyboard: 3D previs or an animatic with the real voice; get an AI director review.
3. Draw poses with an image model, attaching the official PNGs and earlier poses every time; specify line, colours, proportions, accessory side, the same three-quarter direction, scale, white background, no text. Use official art where it fits.
4. Cut out (flood-fill white from the corners); cut lip-sync pairs with one shared crop.
5. Match scale by head size, not drawing height; plant the feet on the same spot; check a sheet of all poses.
6. Rig: grid + Delaunay mesh, weights from position, five bones (head, ears, two paws, contact); act with keyed bones. Move head and contact together for whole-body moves; move only the head for squash and stretch.
7. Lip-sync: an open-mouth skin on the same mesh, shown only on syllable peaks of the voice.
8. Render one `rive --screenshot --advance=N` per frame (in parallel), background inside the artboard.
9. Edit in HyperFrames: all shots inside one camera wrapper, captions, UI, labels, effects, end card.
10. Sound: voice, code-made SFX, a light bed ducked under the voice; nothing on top of the voice that proves the product.
11. Check: `npx hyperframes check`, key frames, duration and size, a final AI review (SHIP), and listen through.

## Rive pitfalls

The first sibling draws on top; one screenshot per invocation; screenshots are opaque; opacity is property 18, bone rotation 15, position 90/91.

## Screen rules

Captions at the top; keep the bottom ~400 px clear for platform UI; phone UI is atmosphere, meaning goes in large labels; never cover the character's face.

## Keep every work reproducible

Each work keeps a consolidated prompt, the making-of, verbatim prompts and reviews, progress images, source with build steps and credits: the finished video and a summary in public, the rest in the private vault. See [Adding a film](ADDING-A-FILM.md).
