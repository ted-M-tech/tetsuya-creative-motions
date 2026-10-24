# How Do You Say It? 3 — Itadakimasu

**English** · [日本語](README.ja.md)

Episode 3 of the feature-led series "How Do You Say It?" (template: [episode 1](../mimi-say-yoroshiku/README.md), [episode 2](../mimi-say-otsukare/README.md)). At the dinner table the Friend holds up the rice bowl and says いただきます word for word: "I will receive!" — Mimi is puzzled: "Receive… what?". In the app the Friend types 「食べる前のいただきます」 in Japanese, taps フレーズを作成, and Lanclo's composer returns its real answer: "Let's eat!" (いただきます（食事を始めるときのあいさつ）) with the real example "Everything looks so delicious, let's eat!". The Friend saves it. Mimi's card: when you start eating "Let's eat!" (the app's answer) / to the cook "This looks great!" (a common line). The Friend says it right; closes with 「次は何を英語にしたい？」.

0:17.30 / 1080×1920, 60 fps / two cuts: Japanese captions only, and with English subtitles (`kits/mimi-short/render-cuts.sh`) / -14 LUFS, true peak ≤ -1.5 dBTP / platform safe zones kept (bottom 420 px, right action rail, top 200 px) / the owner's own voice for the English lines / 2D Mimi and her Friend (library poses + HyperFrames) beside a simulator recording of the iOS app

Status: final, owner approved (2026-10-23). Drive `002.SNS/077. How Do You Say It 3 - Itadakimasu/`: `Say3_Itadakimasu_2026-10-23.mp4`, `Say3_Itadakimasu_EN-subs_2026-10-23.mp4`.

![Frames with the platform safe zones](process/00-draft-frames.jpg)

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the making-of, the owner's words, which real composer answer is shown.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction.
- [process/](process/): the composer's and the example's real answers (`compose-probe-itadakimasu.jsonl`, `example-probe-lets-eat.jsonl`) and frames.
- [source/](source/README.md): rebuild steps.
- [CREDITS.md](CREDITS.md).

## Reproduce

Follow [source/README.md](source/README.md). The simulator take and the own-voice WAVs are in Lanclo's Google Drive (`002.SNS/077. How Do You Say It 3 - Itadakimasu/Say3_Itadakimasu_assets/`).
