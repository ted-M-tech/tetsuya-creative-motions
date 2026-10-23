# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

## Steps and decisions

1. Brief from the commander (batch 055–066): new series “Katakana Traps”, episode 1 McDonald's; Notion ID 058; Mimi plays the clerk in a role outfit (the Notion idea had Bruno; changed to Mimi per the owner's cast rule); no app beat required. Generic beat ids (hook, slip, explain, model, cta, end) so episodes 2 (Mansion, meaning trap) and 3 (Hotel/Guitar/Shampoo, stress) copy `source/`.
2. Layout started from `films/mimi-disaster-hat/source` (say bubble, card, end card, subtitles) and rebuilt for the new beats; times in `source/cues.json`, shared by `scripts/mix.py` and `hf/index.html`.
3. Art: one codex-p run drew Mimi as a fast-food clerk (red-and-white striped shirt, red visor without a logo, headphones kept): blank, “Sorry?”, smiling thumbs-up ([prompts/01-codex-mimi-clerk.txt](prompts/01-codex-mimi-clerk.txt)); all three on model at first try. Plate `burger-shop` and the Friend / Mimi poses from the library. No new characters.
4. Voice: `own-voice.json` → ownvoice.py, 2 lines, 1 take each, no regenerations.

| Line | Text | Direction | Takes |
|---|---|---|---|
| `learner-katakana` | “Makudonarudo.” | custom style: the katakana reading, six even syllables each with its own vowel, flat Japanese pitch | 1 |
| `us-mcdonalds` | “McDonald's.” | custom native style: three syllables, reduced “mc”, strong “DON”, reduced “alds” ending in z | 1 |

   Acoustic check (Praat via parselmouth, [process/01-takes-spectrogram.jpg](process/01-takes-spectrogram.jpg)); a transcript was not used:
   - Learner: speech 0.27–0.96 s; six band-energy (300–2500 Hz) peaks at 0.32, 0.50, 0.58, 0.71, 0.82, 0.88 s, all within 4.2 dB of each other (even, no stressed syllable); voiced almost throughout (0.33–0.42, 0.49–0.54, 0.56–0.86, 0.89–0.96) and it ends on a voiced vowel with formants (the final “do”), i.e. vowels after the consonants: 6 beats.
   - Model: speech 0.28–1.13 s; a stop closure (silence 0.48–0.54) between “mc” and “DON”; “DON” is the longest (≈0.29 s) and loudest nucleus (peak at 0.59 s, “mc” −3.4 dB, “alds” −9.3 dB); the word ends in unvoiced frication (0.97–1.13, “dz”) with no vowel after it: 3 syllables, stress on DON.
   The measured beats drive the dot meters (`LEARNER_BEATS`, `MODEL_BEATS` in `cues.json`). Needs a human listen.
5. Sound (`scripts/mix.py`, kit Mix): a soft sine tick per beat (no bell), boing on “Sorry…?”, the bed drops to 25 % from “Sorry…?” until the card and comes back; the model take plays twice on the card and once more when the Friend says it right (the Friend is voiced by the owner). Voice 10–16 dB over the bed; peaks −1.5 dBFS. The kit's single-pass loudnorm (TP −1.5) left this short, voice-sparse film at −17.2 LUFS in v1; v2 measures the written mix and adds the missing gain in front of a −1.5 dBTP limiter (end of `scripts/mix.py`), the balance between voice, SFX and bed unchanged: mix −14.3 LUFS / −1.4 dBTP, rendered cuts −13.8 LUFS, peak −1.2 dBFS.
6. Checked with `hyperframes check` (layout overflows on the card fixed) and a contact sheet ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)): captions top, faces clear, the explain-card Mimi sits beside the tip, right of the 英語○ card, above the bottom 400 px (v2).

## Commander review (2026-10-23, v2)

- Loudness to −14 LUFS via the mix (series consistency), voice on top, true peak ≤ −1 dBTP: done as above.
- Explain card: Mimi moved out of the bottom ~400 px (now 1170–1460 px, beside the tip; the tip and お手本 tag are left-aligned). v1 drafts moved to Drive `old/` (`*_v1.mp4`).

## Platform safe zones (2026-10-23, v3)

- Owner: 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」
- EN subtitles moved to x 60–880 with the box bottom at y 1490 (above the bottom 420 px); the end-card subtitle sits at the top (y 220) so it does not cover the CTA button.
- Right rail (x > 900, y 820–1520) kept clear: characters shifted left (clerk Mimi's face now left of x 900), the reply bubbles end at x 890, the explain-card Mimi is at x 560–810 beside the two-line tip, the お手本 tag sits in the 英語○ card header (y 646, above the rail), sparkles moved in.
- Top text starts at y ≥ 200 (hook card top 165, card title 200, CTA card 165).
- Loudness rule tightened to true peak ≤ −1.5 dBTP: the post-limiter is now −2.4 dB; cuts measure −14.0 LUFS, peak −1.9 dBTP.
- Overlay check: [process/02-safe-zones.jpg](process/02-safe-zones.jpg) (EN cut, zones drawn). The kit end card's App Store badge stays in the bottom zone (kit layout, as in every episode).
- v2 drafts moved to Drive `old/` (`*_v2.mp4`).

## Uncertain / for review

- The learner word is fast (six beats in about 0.7 s); the meter fills quickly, so the card replays it over six equal dots.
- “Sorry…?” and “Oh! Next door!” are bubbles only (no voice), so no side-cast TTS is needed.
- The owner's (adult male) voice on the Friend, as in earlier episodes.

## Owner approval

- 2026-10-23: 「全部OK」 (all twelve shorts of the 055–066 batch approved as delivered; the Drive cuts were renamed without `_draft_`: `KT1_McDonalds_2026-10-23.mp4`, `KT1_McDonalds_EN-subs_2026-10-23.mp4`).
- Earlier owner notes in the same review round (2026-10-23): 「56の英語音声少し切れている？」 (clipped English in 056; led to the voice-cut audit of every episode); 「62透過されている？」 (the see-through angry pose in 062; fixed there with a filled pose).
