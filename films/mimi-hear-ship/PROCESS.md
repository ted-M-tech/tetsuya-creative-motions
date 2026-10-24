# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- 2026-10-23 (safe zones): 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」

## Steps and decisions

1. Brief from the batch commander ([prompts/00-commander-brief.txt](prompts/00-commander-brief.txt)) and the Notion row (078, Status Idea → Planning). Copied films/mimi-hear-can/source (episode 1, the two-option form): beat ids, layout, the 3 dB bed / SFX pre-cut and the -14 LUFS post-gain + limiter step in `scripts/mix.py` unchanged.
2. Cast: Mimi + Friend only, the same library poses as episode 1 (Friend `dreamy` → `tease` “Bでしょ！” → `shock` → `yay`; Mimi `confident` → `tease` → `point` on the rule card → `jump`). No codex-p run, no new art; the small sheep and ship icons under the cards are inline SVG.
3. Quiz order: A = “I saw a sheep.”, B = “I saw a ship.”, question 「sheep はどっち？」, answer A (episode 1's answer was B, so the position varies). The Friend picks B: to a Japanese ear both are 「シップ」-ish (「えっ！？ 同じに聞こえた…」).
4. Voice: `own-voice.json` → ownvoice.py. `us-ship`: 1 generation, kept. `us-sheep`: 1 generation + 3 regenerations (the maximum); all earlier takes are kept on Drive `Hear3_Ship_assets/own-voice/rejected/`. The final direction is verbatim in `own-voice.json`.

   Acoustic check with Praat (`source/scripts/check_voice.py`; 20 ms windows every 10 ms; the vowel = the frames after the sh, below 2.5 kHz centroid, until the energy stays 20 dB under the peak (p closure); the final vowels are partly creaky, so the vowel is found by energy and spectrum, not the pitch track; F1 / F2 = Burg median over the middle 60 %):

| take | sh | vowel | vowel F1 / F2 | used |
|---|---|---|---|---|
| `us-ship` “I saw a ship.” | 0.62–0.77 s (~150 ms) | 0.77–0.89 s = **120 ms** | **523 / 1734 Hz** (lax /ɪ/) | yes |
| `us-sheep` take 1 | 0.76–0.91 s | 150 ms | 384 / 2129 Hz | no: only 1.25× the ship vowel |
| `us-sheep` take 2 (“about twice as long”) | | 130 ms | 353 / 2630 Hz | no: not longer |
| `us-sheep` take 3 (“teacher, slow”) | | 230 ms | 293 / 2724 Hz | no: the whole sentence slow with a 0.2 s pause before “a sheep”, a giveaway in the quiz |
| `us-sheep` final (“normal speed, only the vowel long”) | 0.63–0.82 s (~190 ms) | 0.84–1.06 s = **220 ms** | **286 / 2686 Hz** (tense /iː/) | yes |

   So the sheep vowel is 1.8× as long as the ship vowel, F1 237 Hz lower (closer, tongue higher) and F2 950 Hz higher (fronter, lips spread): the contrast the film teaches. “I saw a” matches in both takes (the sh starts at 0.62 / 0.63 s), so length and quality are the only cues. The sh before the long vowel is also a little longer (natural). Whisper not used.
5. Mix: takes cut at real silence (us-ship 0.20–1.12 s, us-sheep 0.17–1.37 s of the take; speech onset 77 / 88 ms after the cut; first and last 10 ms at -55 / -58 dB and -59 / -58 dB vs the clip peak). Kit bed and SFX, soft taps for the countdown, pofu for the reveal. `mix.wav` -14.1 LUFS, -1.9 dBTP; voice RMS 9–11 dB above the bed-only stretches (episode 1: 8.8 dB).
6. Layout after the first contact sheet: the reveal and rule subtitles ran to three lines and covered the bunnies' chins and the small rule-card Mimi; the subtitles were cut to two lines (the rule subtitle split per row), the bunnies and their bubbles moved up 40 px, 「えっ！？」 on one line. Rule title at 68 px (one line, inside the frame), the ship row's note on its own line. Hook “sheep” orange darkened to #c96a2c for contrast. `hyperframes check`: 0 errors (lint warnings as in episode 1).
7. Safe zones: overlay sheet of the EN cut every ~1.5 s ([process/01-safe-zones.jpg](process/01-safe-zones.jpg)): subtitles end at y 1495 within x 60–880; no text, bubble or face in the right rail (Mimi x 570–870, rule Mimi x 620–870); top texts start at y ≥ 200.
8. Delivery: both cuts 1080×1920, 60 fps, 16.2 s, no rotation side data, -14.2 LUFS, -1.8 dBTP. Drive: `Hear3_Ship_draft_2026-10-23.mp4`, `Hear3_Ship_draft_EN-subs_2026-10-23.mp4`.

## Draft v2 (2026-10-23, owner review)

- Owner: 「078みた。フォントの色とか変わってる？統一感出して過去と」
- Commander: episode 1 colours the two target words blue #2a8dff / red #e5484d (hook, question pill, card answers, rule card); v1 had switched them to the A / B card colours (purple / orange) and drifted in other styles.
- Fix: the A / B cards keep episode 1's colours (A orange, B purple); ship = blue, sheep = red everywhere, like can / can't (hook, 「sheep はどっち？」 pill in episode 1's light red #ff9ea1 on navy, answers under the cards, rule rows, bars, borders and highlights, the 「口を横に「イー」→sheep」 pill, the ask line). ○ blue / × red marks as in episode 1. The style block now differs from episode 1 only in content: rule title back to 76 px (text shortened to 「長さと口の形を聞く！」), row tops / heights 320 / 345 and 685 / 410, the long word 100 px like CAN'T, grey syllable bars for “I saw a” plus the coloured vowel bar (ship 120 px, sheep 240 px), cast and bubble positions back to episode 1's; removed #c96a2c, #ffc08a and the extra grey bar labels. The card icons stay (content).
- Side by side with episode 1: [process/02-v2-vs-061.jpg](process/02-v2-vs-061.jpg). Safe zones re-checked ([process/01-safe-zones.jpg](process/01-safe-zones.jpg)). Audio unchanged (-14.2 LUFS, -1.8 dBTP). v1 drafts moved to Drive `old/` with a `_v1` suffix.

## Open questions

- Owner's ear on the final sheep take (direction “only the vowel long”): does the sentence still sound natural next to the ship take?
- Length 16.2 s (brief ~16 s).
