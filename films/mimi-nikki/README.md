# The diary ends on day three — a 2D Mimi short

**English** · [日本語](README.ja.md)

Day three of her English diary and Mimi has literally become a little monk (三日坊主, the Japanese idiom for quitting after three days). Lanclo's English journal lets her just talk; it corrects the entry (go → went), plays it back in her own voice, and Mimi paints the day as a picture. A calendar of pictures is fun to look back on, so the diary lasts. The fourth Mimi short and the first that introduces a feature (the English journal).

0:16.6 / 1080×1920, 60 fps / Japanese captions, English voice / 2D: official art style drawn with Codex + Rive bones + HyperFrames

Two cuts: Japanese only (`mimi-nikki.mp4`) and with English subtitles (`mimi-nikki-en.mp4`, rendered by `kits/mimi-short/render-cuts.sh`); both in Lanclo's Google Drive `002.SNS/007. Journal Ends in 3 Days/`.

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the making-of — the owner's directions (including the rework around the illustration), reviews, decisions, lessons.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction to remake it or make another feature episode.
- [prompts/](prompts/) and [reviews/](reviews/): Codex prompts and both reviews.
- [source/](source/README.md): shots, sound, edit, build steps.
- [kits/mimi-short](../../kits/mimi-short/README.md): the shared kit.
- [CREDITS.md](CREDITS.md): materials and rights.

## Reproduce

Follow [source/README.md](source/README.md). Everything needed is in Git except the two voice lines (the owner's own voice, kept out of the public repo: Drive `Mimi_04_Journal_Ends_in_3_Days_assets/own-voice/`, or regenerate with `kits/mimi-short/scripts/ownvoice.py`), renders and the final MP4.

Since 2026-10-21 Mimi's English lines are the owner's registered Lanclo voice (Gemini `gemini-3.8-flash-tts`): "Yesterday... I go to cafe." with a learner accent, "Yesterday, I went to a cafe." as the General American model.
