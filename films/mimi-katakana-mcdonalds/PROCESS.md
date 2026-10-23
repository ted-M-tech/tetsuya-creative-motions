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
5. Sound (`scripts/mix.py`, kit Mix): a soft sine tick per beat (no bell), boing on “Sorry…?”, the bed drops to 25 % from “Sorry…?” until the card and comes back; the model take plays twice on the card and once more when the Friend says it right (the Friend is voiced by the owner). Voice 10–16 dB over the bed; peaks −1.5 dBFS. Integrated loudness of the render is −17.2 LUFS (kit loudnorm with TP −1.5 on a short, voice-sparse film; 053 measured −15.0). Left as is: quieter is the safe side on earphones.
6. Checked with `hyperframes check` (layout overflows on the card fixed) and a contact sheet ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)): captions top, faces clear, the explain-card Mimi moved up so the English subtitle does not cover her.

## Uncertain / for review

- The learner word is fast (six beats in about 0.7 s); the meter fills quickly, so the card replays it over six equal dots.
- “Sorry…?” and “Oh! Next door!” are bubbles only (no voice), so no side-cast TTS is needed.
- The owner's (adult male) voice on the Friend, as in earlier episodes.
