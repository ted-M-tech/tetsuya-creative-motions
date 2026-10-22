# Asked the way, she freezes — a 2D Mimi short

**English** · [日本語](README.ja.md)

A passer-by asks Mimi the way in English and she freezes into a block of ice. At her desk Lanclo plays her own voice giving the answer, a radar card gives one fix (link "turn left" in one breath), she practises; back on the street the ice shatters, she points the way and gets a "Thank you!". The third Mimi short, built on the shared kit.

0:15.3 / 1080×1920, 60 fps / Japanese captions, English voices / 2D: official art style drawn with Codex + Rive bones + HyperFrames

Two cuts: Japanese only (`mimi-michi.mp4`) and with English subtitles (`mimi-michi-en.mp4`, rendered by `kits/mimi-short/render-cuts.sh`); both in Lanclo's Google Drive `002.SNS/006. Frozen When Asked for Directions/`.

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the making-of — the owner's directions, reviews, decisions, lessons.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction to remake it or make another episode.
- [prompts/](prompts/): the exact prompts given to Codex (art and review).
- [reviews/](reviews/): Codex's final-cut review.
- [source/](source/README.md): episode shots, sound, HyperFrames edit, build steps.
- [kits/mimi-short](../../kits/mimi-short/README.md): the shared kit.
- [CREDITS.md](CREDITS.md): materials and rights.

## Reproduce

Follow [source/README.md](source/README.md). Everything needed is in Git except Mimi's two voice lines (the owner's own voice, kept out of the public repo: Drive `Mimi_03_Frozen_Asked_Directions_assets/own-voice/`, or regenerate with `kits/mimi-short/scripts/ownvoice.py`), renders and the final MP4.

Since 2026-10-21 Mimi's English lines are the owner's registered Lanclo voice (Gemini `gemini-3.8-flash-tts`): "Uh... uh..." with a learner accent, "Go straight, and turn left." as the General American model. The passer-by keeps the Kokoro voice `bm_george`.
