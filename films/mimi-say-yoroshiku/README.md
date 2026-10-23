# How Do You Say It? 1 — Yoroshiku Onegaishimasu

**English** · [日本語](README.ja.md)

Episode 1 and template of the feature-led series "How Do You Say It?": a Japanese phrase with no one-to-one English goes into Lanclo's real phrase composer. On her first day at work the Friend freezes mid-bow — "Please... yoroshiku?" — and Mimi, as the new colleague, is puzzled. In the app the Friend types 「新しい職場でよろしくお願いします」 in Japanese, taps フレーズを作成, and gets the composer's real answer, "I look forward to working with you.", editable, then saves it. Mimi's card splits the phrase by situation: first meeting "Nice to meet you." / working together "I look forward to working with you." Closes with 「次は何を英語にしたい？」.

0:18.6 / 1080×1920, 60 fps / two cuts: Japanese captions only, and with English subtitles (`kits/mimi-short/render-cuts.sh`) / the owner's own voice for the English lines / 2D Mimi and her Friend (pose swap + HyperFrames) beside a simulator recording of the iOS app

Status: draft (2026-10-23), in Drive `002.SNS/063. How Do You Say It 1 - Yoroshiku Onegaishimasu/` as `Say1_Yoroshiku_draft_2026-10-23.mp4` and `Say1_Yoroshiku_draft_EN-subs_2026-10-23.mp4`.

![Draft frames](process/00-draft-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the making-of, the owner's words, how the composer's real answer was obtained.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction.
- [prompts/](prompts/): Codex prompts and logs for the poses.
- [process/](process/): the composer's real answers (`compose-probe-*.jsonl`, also お疲れ様 for episode 2) and frames.
- [source/](source/README.md): rebuild steps and the **series template** (how the composer was captured).
- [CREDITS.md](CREDITS.md).

## Reproduce

Follow [source/README.md](source/README.md). The simulator take and the own-voice WAVs are in Lanclo's Google Drive (`002.SNS/063. How Do You Say It 1 - Yoroshiku Onegaishimasu/Say1_Yoroshiku_assets/`).
