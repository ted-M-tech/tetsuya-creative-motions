# "think" turns into "sink" — a 2D Mimi short

**English** · [日本語](README.ja.md)

Mimi proudly says "I sink so!" and a kitchen sink drops from the sky; she says it again and a second one lands. Lanclo plays her own voice saying "I think so." right, a radar card gives one fix for "th", she practises along, the sinks vanish and she says it right. The second Mimi short, and the first built on the shared Mimi shorts kit.

0:15 / 1080×1920, 60 fps / Japanese captions, English voice / 2D: official art style drawn with Codex + Rive bones + HyperFrames

Two cuts: Japanese only (`mimi-think-sink.mp4`) and with English subtitles (`mimi-think-sink-en.mp4`, rendered by `kits/mimi-short/render-cuts.sh`); both in Lanclo's Google Drive `002.SNS/005. Think Becomes Sink/`.

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the making-of — the owner's directions, the kit, reviews, decisions, lessons.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction to remake it or make another episode.
- [prompts/](prompts/): the exact prompts given to Codex (art and review).
- [reviews/](reviews/): Codex's final-cut review.
- [source/](source/README.md): episode shots, sound, HyperFrames edit, build steps.
- [kits/mimi-short](../../kits/mimi-short/README.md): the shared kit (library copy, rig, sound, look).
- [CREDITS.md](CREDITS.md): materials and rights.
- General guide: [2D character animation](../../docs/2D-CHARACTER-ANIMATION.md).

## Reproduce

Follow [source/README.md](source/README.md). Everything needed is in Git except the two voice lines (the owner's own voice, kept out of the public repo: Drive `Mimi_02_Think_Becomes_Sink_assets/own-voice/`, or regenerate with `kits/mimi-short/scripts/ownvoice.py`), renders and the final MP4.

Since 2026-10-21 Mimi's English lines are the owner's registered Lanclo voice (Gemini `gemini-3.8-flash-tts`): "I sink so!" with a learner accent, "I think so." as the General American model.
