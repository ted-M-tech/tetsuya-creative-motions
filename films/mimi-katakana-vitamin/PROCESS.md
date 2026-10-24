# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- 2026-10-23 (safe zones, from the batch rules): 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」
- 2026-10-23 (series look, relayed by the commander): 「フォントの色とか変わってる？統一感出して過去と」

## Steps and decisions

1. Brief from the commander (batch, Notion ID 076): Katakana Traps 4, ビタミン vs VI-ta-min, stress on the first syllable and a real V; US VAI-ta-min vs UK VIT-a-min as a small note only, the model is US. Hook 「ビタミン、通じない？」 (the Notion idea said 「ビタミン、英語では？」; the brief's hook was used). Pharmacy counter, Mimi as the pharmacist (the 058 clerk approach). Cast Mimi + Friend only.
2. `source/` copied from `films/mimi-katakana-mcdonalds` (episode 1), beat ids and element ids kept: hook, slip, explain, model, cta, end. The stressed (`.big`) dot is the first one; the card adds a V mouth panel and a US/UK note.
3. Art: one codex-p run ([prompts/01-codex-mimi-pharmacist.txt](prompts/01-codex-mimi-pharmacist.txt)) drew Mimi as a pharmacist (white coat, light-blue top, a mint badge with a plain cross, headphones kept): blank, “Sorry?”, smiling with a blank-label vitamin bottle; plus a pharmacy plate in the layout of the library `burger-shop` plate (no text). All on model at the first try; all three poses checked on a dark background (filled, nothing see-through). The V mouth panel (`mouth-v-front`) is reused from films/mimi-disaster-very.
4. Voice: `own-voice.json` → ownvoice.py, 2 lines. The first call of `us-vitamin` hit HTTP 429 (rate limit, nothing generated) and was retried after a pause. `us-vitamin` was regenerated once (see below); 3 generations in total.

| Line | Text | Direction | Takes |
|---|---|---|---|
| `learner-katakana` | “Bitamin.” | custom style: the katakana reading, four even beats bi-ta-mi-n, a Japanese B (lips closed), flat pitch | 1 |
| `us-vitamin` | “Vitamin.” (the word alone) | custom native style: VAI-ta-min, first syllable stressed, a real voiced V (teeth on the lip, no lip closure) | 2 (take 1 rejected) |

   Acoustic check (5 ms / 2.5 ms frames, band energies 50–400 Hz / 400–2500 Hz / 2.5–8 kHz, Praat pitch and intensity via parselmouth; spectrograms in [process/01-takes-spectrogram.jpg](process/01-takes-spectrogram.jpg): top learner, middle rejected model take 1, bottom model take 2). A transcript was not used.
   - Learner “Bitamin”: speech 0.27–0.93 s. 0.27–0.34 a voice bar only (low band −10 dB, the 2.5–8 kHz band at −60 dB: lips closed), then at 0.34 s a vertical burst across all bands into the vowel: a voiced B with a release burst, not a V. Four nuclei at 0.40 (bi), 0.56 (ta), 0.67 (mi), 0.80 s (n, nasal: low band high, mid band down), each 90–110 ms long (even beats). The first beat is not stressed: bi 76.6 dB vs ta 82 dB, and its pitch is the lowest (89 Hz, then 126–158 Hz on ta-mi, falling on n): flat Japanese rhythm with a low start.
   - Model take 1: 0.25–0.31 s voice bar with the high band at −64…−70 dB (full closure), then a broadband spike at 0.313 s: a B-like onset. Rejected.
   - Model take 2 (used): voicing from 0.29 s; 0.31–0.34 s the high band rises gradually from −50 to −40 dB together with the voicing (continuous frication, no closure, no instant spike), a short noisier stretch at 0.342–0.357 s, then the vowel at 0.36 s. This matches the owner-voice V of episode 056 (`word-very`: 60–90 ms of frication at −40…−50 dB, no burst) and not the B pattern above: a real V. Stress: VAI 0.37–0.50 s (130 ms, the loudest nucleus 80.5 dB, pitch rising 94→123 Hz), ta 0.54–0.57 s (short, 78 dB), min 0.58–0.86 s (soft, ~67–74 dB): first syllable stressed. The F2 rise in VAI (about 1.2→2.0 kHz) is the US diphthong.
   The measured nuclei drive the dot meters (`LEARNER_BEATS` 0.40/0.56/0.67/0.80, `MODEL_BEATS` 0.43/0.555/0.70 in `cues.json`). Needs a human listen.
   - Voice cuts: learner placed from 0.20 s for 0.80 s, model from 0.20 s for 0.75 s (70 ms pre-roll, the tail after the voice has decayed). Every placement: first 10 ms −49.9 / −53.3 dB, last 10 ms −52.4 / −45.2 dB vs the clip peak (rule ≤ −38 dB).
5. Sound (`scripts/mix.py`, copied from episode 1): a soft sine tick per beat (no bell; the stressed tick is now the first), boing on “Sorry…?”, the bed drops to 25 % from “Sorry…?” until the card. With only two short words of voice the −14 LUFS post-gain lifted the bed more than in episode 1 (voice about 8 dB over the hook bed), so the bed is 3 dB lower in this film: voice −12.1…−12.4 dBFS RMS vs bed −22.7 (hook) / −18.3 dBFS (CTA). Post-gain + limiter step from episode 1: mix −14.3 LUFS / −2.0 dBTP; both cuts −14.3 LUFS, −2.1 dBTP.
6. Series look (commander, 2026-10-23): the card CSS was diffed against episode 1 and the drift removed: the katakana / English row dot and text sizes back to episode 1 (74 px dots and 62 px katakana, the stressed dot 190 px and 104 px “VI”), the tip font 56 px, the English strings in captions and titles back to the kit font (Helvetica only inside the tip, the note and the say bubble, as in episode 1). Colour roles unchanged from the series: red #e5484d for katakana ×, blue #2a8dff for English ○ and the stressed dot, navy #273b4b text, #5b7f9f labels, yellow #ffd84a in the tip. Rows put their label on the left (as the rows in episode 3) to make room for the V panel.
7. Checked with `hyperframes check` (0 errors) and an overlay contact sheet ([process/00-draft-frames.jpg](process/00-draft-frames.jpg), EN cut every ~1.5 s, zones drawn): hook readable from frame 1; top text from y ≥ 200; EN subtitles inside x 60–880 with the box bottom at y 1490; nothing in the right rail (the “min” of the English row ends at x ≈ 865, the faces of pharmacist Mimi stay left of x 900, the bubbles end at x 890); captions never over faces. Only Mimi and the Friend on screen; no Japanese first person in the text; no fixture text, no counts.

## Commander review (2026-10-23, v2)

- The card, captions and tip spelled the stressed syllable “VI” while the US model says VAI-ta-min: screen and sound disagreed. v2 follows the model: the stressed-dot label 「VAI」, the tip 「VAI-ta-min（VAIを強く）」, the captions 「ビじゃなくて VAI！」 and 「VAIを強く → 通じた！」, the EN subtitles to match (the pronunciations kept on one line), and the note is now 「※英国では VIT-a-min」. No new voice generation; layout, sound and loudness unchanged (both cuts −14.3 LUFS, −2.1 dBTP). Safe-zone sheet redone (“min” ends at x ≈ 870). v1 cuts moved to Drive `old/` with `_v1`.

## Uncertain / for review

- The V onset of the model is soft (a short frication into the vowel, as natural speech has it); a human listen should confirm it reads as V on earphones.
- “Sorry…?” and “Right here!” are bubbles only (no voice).
- The owner's (adult male) voice on the Friend, as in earlier episodes.
