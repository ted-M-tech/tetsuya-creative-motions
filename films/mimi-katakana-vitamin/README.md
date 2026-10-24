# Katakana Traps 4 - Vitamin

[日本語](README.ja.md)

Lanclo SNS short #076, episode 4 of “Katakana Traps” (stress + the V sound). Draft (2026-10-23), waiting for the owner's review. 15.5 s, 1080×1920, 60 fps, two cuts (Japanese only / English subtitles).

Frame 1: 「ビタミン、通じない？」. At a pharmacy counter the Friend asks the pharmacist (Mimi in a role outfit: a white pharmacist coat) for 「ビタミン」 the katakana way, four even beats starting with a B (owner's own voice, learner style), while a four-dot meter fills. Pharmacist Mimi, blank: “Sorry…?”; caption 「ビじゃなくて VI！」. A card: katakana × (four equal dots ビ・タ・ミ・ン) vs English ○ (VI · ta · min, the first dot big), the model twice in the owner's own voice (US, VAI-ta-min), a V mouth panel 「V＝上の歯を下唇に」 and the tip 「VI-ta-min（VIを強く）」; a small note 「※お手本は米 VAI-ta-min（英 VIT-a-min）」. Back at the counter the Friend says it right, the pharmacist smiles with a vitamin bottle: “Right here!”. CTA 「次に通じないカタカナは？」, then the end card.

| Time (s) | Beat id | What |
|---|---|---|
| 0.00–1.30 | `hook` | 「ビタミン、通じない？」 from frame 1; the Friend at the pharmacy counter, pharmacist Mimi blank-faced |
| 1.30–4.60 | `slip` | Learner take “Bitamin” (owner's voice), 4 dots light on the measured beats; “Sorry…?” at 2.6; caption 「ビじゃなくて VI！」 at 3.2 |
| 4.60–9.40 | `explain` | Card: katakana × (4 equal dots, learner take again at 5.0) vs English ○ (VI · ta · min, first big; model take at 6.6 and 7.9); V mouth panel at 6.9; tip 「VI-ta-min（VIを強く）」; お手本＝自分の声; US/UK note at 8.5 |
| 9.40–12.00 | `model` | The Friend says it right (model take), 3-dot meter (first big); pharmacist Mimi smiles “Right here!”; caption 「VIを強く → 通じた！」 |
| 12.00–14.20 | `cta` | 「次に通じないカタカナは？」「コメントで教えてね」 with Mimi and the Friend |
| 14.20–15.50 | `end` | End card, CTA tap at 14.8 |

- Cast: Mimi (also as the pharmacist) and her Friend only. No side cast, no Kokoro, no app shot.
- Art: three new pharmacist poses of Mimi and a pharmacy plate drawn with codex-p ([prompts/01-codex-mimi-pharmacist.txt](prompts/01-codex-mimi-pharmacist.txt)); the V mouth panel is reused from [films/mimi-disaster-very](../mimi-disaster-very/README.md).
- Voices: two lines in the owner's registered voice via `kits/mimi-short/scripts/ownvoice.py` (one regeneration of the model line for a real V onset); WAVs are biometric and not in Git (Drive `076. Katakana Traps 4 - Vitamin/KT4_Vitamin_assets/own-voice/`). Stress and the V onset verified acoustically, see [PROCESS.md](PROCESS.md).
- Draft files in Lanclo's Google Drive `002.SNS/076. Katakana Traps 4 - Vitamin/` (`KT4_Vitamin_draft_2026-10-23.mp4`, `KT4_Vitamin_draft_EN-subs_2026-10-23.mp4`).
- Loudness: -14.3 LUFS integrated, -2.1 dBTP (both cuts).
- Rebuild: [source/README.md](source/README.md). Making-of: [PROCESS.md](PROCESS.md). Prompt: [PROMPT.md](PROMPT.md). Credits: [CREDITS.md](CREDITS.md). Series template: [episode 1](../mimi-katakana-mcdonalds/README.md#series-template-episodes-2).

Platform safe zones (TikTok / Reels / Shorts UI) checked: frames below carry the zone overlay (EN cut).

![Frames with the platform safe zones](process/00-draft-frames.jpg)
