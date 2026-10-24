# Real Slang 2 - Hangry — a 2D Mimi short

**English** · [日本語](README.ja.md)

Status: **draft** (2026-10-23, waiting for the owner's review). The isolated "Hangry." take for the meaning card is not generated yet (the shared TTS quota ran out); the draft has the card without it.

Episode 2 of the series **Real Slang** (template: [mimi-slang-no-cap](../mimi-slang-no-cap/README.md#series-template-real-slang-episodes-24-hangry-ghosted-mid)). Hook from the first frame:「お腹すいてイライラ＝？」 (hungry and irritated = ?) over the Friend fuming with an empty bento while his tummy growls. Mimi points: "You're hangry!" The Friend admits it with the deck's own example, "I'm getting hangry; let's find lunch." (caption: the deck's translation). A meaning card in the deck's wording: hungry ＋ angry, hangry ＝ 空腹でいらいらした, and both deck examples with their translations, all rows in within 0.55 s (the series improvement over episode 1); the spoken example lights up. The real app (simulator, shipped deck content): 単語帳 → スラング・カジュアル → ユニット6 気分・テンション → the "hangry" card → save. Comment prompt:「次のスラングは？コメントで」 over the Friend happy with a rice ball. End card with the CTA tap.

0:17.8 / 1080×1920, 60 fps / English clips in the owner's voice, Japanese captions and cards / official 2D poses + GSAP, real app (simulator) + HyperFrames

Notion Content Calendar ID 069. Two cuts: Japanese only (`mimi-slang-hangry.mp4`) and with English subtitles (`mimi-slang-hangry-en.mp4`); drafts in Lanclo's Google Drive `002.SNS/069. Real Slang 2 - Hangry/` (`Slang2_Hangry_draft_2026-10-23.mp4`, `Slang2_Hangry_draft_EN-subs_2026-10-23.mp4`; raw take and own-voice WAVs in `Slang2_Hangry_assets/`).

![Frames](process/00-draft-frames.jpg)

| Beat (id) | Time (s) | What |
|---|---|---|
| hook | 0.0–3.0 | Hook card from frame 1; the Friend (friend-hangry, empty bento) shakes, 「ぐぅ〜」 and a low growl; Mimi (tilt → point) "You're hangry!" (bubble + own voice, from 1.0) |
| gag | 3.0–5.9 | The Friend: "I'm getting hangry; let's find lunch." (deck example, own voice); caption = the deck translation; Mimi (tease) |
| meaning | 5.9–10.1 | Deck card: hungry ＋ angry, hangry ＝ 空腹でいらいらした, example 1, example 2, all in by 6.45; "Hangry." take at 6.0 (pending); example 1 lit and spoken again 7.4–9.9 |
| app | 10.1–14.5 | 単語帳 deck list → スラング・カジュアル units → ユニット6 → the "hangry" card dragged up → save (bookmark at 13.45); counts masked |
| cta | 14.5–16.3 | Friend (friend-lunch, rice ball) + Mimi (jump);「次のスラングは？コメントで」 |
| end | 16.3–17.8 | End card, CTA tap at 16.9 |

## Files

- [PROCESS.md](PROCESS.md) (Japanese): the owner's words, the feature check and the decisions.
- [PROMPT.md](PROMPT.md) (Japanese): a consolidated instruction to remake it.
- [prompts/](prompts/): the Codex prompt for the two new poses, and its log.
- [source/](source/README.md): app capture, voices, sound, HyperFrames edit, build steps.
- [CREDITS.md](CREDITS.md): materials and rights.
