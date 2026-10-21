# Tsundoku — Mimi does the daily lesson

**English** · [日本語](README.ja.md)

Mimi's pile of English books keeps growing and never gets read (積読, *tsundoku*). Then she opens Lanclo's daily lesson in the real app (recorded in the simulator with QA fixture data): today's sentence, "Please leave the light on.", played as a native model in her own voice; she records it, says "right", gets a five-axis score and the one sound to fix (right → light). The sixth Mimi short and the second on real screens.

0:15 / 1080×1920, 60 fps / Japanese captions, English voice / 2D Mimi (Rive) beside a simulator recording of the app

Two cuts: Japanese only (`mimi-daily.mp4`) and with English subtitles (`mimi-daily-en.mp4`, rendered by `kits/mimi-short/render-cuts.sh`); both in Lanclo's Google Drive `002.SNS/009. Unread Books - Daily Lesson/`.

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the making-of.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction for this episode.
- [prompts/](prompts/), [reviews/](reviews/): the book-tower art prompt and the Codex review.
- [source/](source/README.md): walkthrough, cuts, shots, sound, edit.
- [kits/mimi-short/app-capture](../../kits/mimi-short/app-capture/capture.sh): the shared recorder.
- [CREDITS.md](CREDITS.md).

## Reproduce

Follow [source/README.md](source/README.md). The app recording needs the Lanclo repository and Xcode; the take used for this cut is kept in Lanclo's Google Drive.
