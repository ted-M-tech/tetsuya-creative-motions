# Describe a photo — Mimi uses the real app

**English** · [日本語](README.ja.md)

Mimi tries to describe a cafe photo and manages only "People is sitting...". Then she uses Lanclo's photo description feature: the real app (recorded in the simulator with QA fixture data) takes her answer, scores it, marks the mistake, corrects is → are and offers a more natural sentence in her own voice. The fifth Mimi short and the first on real screens.

0:15 / 1080×1920, 60 fps / Japanese captions, English voice / 2D Mimi (Rive) beside a simulator recording of the app

![Final frames](process/00-final-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the making-of, including how the app was recorded.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction for real-screen episodes.
- [prompts/](prompts/), [reviews/](reviews/): the Codex review.
- [source/](source/README.md): walkthrough, cuts, shots, sound, edit.
- [kits/mimi-short/app-capture](../../kits/mimi-short/app-capture/capture.sh): the shared recorder.
- [CREDITS.md](CREDITS.md).

## Reproduce

Follow [source/README.md](source/README.md). The app recording needs the Lanclo repository and Xcode; the take used for this cut is kept in Lanclo's Google Drive.
