# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

## Steps and decisions

1. Brief from the commander (batch 055–066): Katakana Traps episode 2, Notion ID 059, a meaning trap. The Notion idea had Pippa picturing the castle (Kokoro voice); changed to Mimi per the owner's cast rule, and Mimi's “Wow, you're rich!” is a bubble only (no voice), like episode 1's “Sorry…?”. Commander notes from episode 1 applied: integrated loudness -14 LUFS, the small Mimi and everything meaningful above the bottom ~400 px.
2. Branch from `origin/feat/mimi-katakana-mcdonalds`; `source/` copied from episode 1, beat ids kept (hook, slip, explain, model, cta, end). `model` holds the quick-fire trap card here (episode 1 used it for the said-right retake).
3. Art: all character poses from the library (no new poses): Mimi `sparkle` (dreaming), `perk` (“Wow, you're rich!”), `confident` (card), `point` (quick-fire), `droop` (castle deflated); the Friend `friend-order` (the line), `friend-oops` (panic), `friend-nod` (CTA). Plate `street`. One codex-p run drew four props ([prompts/01-codex-props.txt](prompts/01-codex-props.txt)): a castle-like mansion with a fountain, an ordinary apartment block, a US wall outlet with a plug, an angry speech bubble; all usable at first try.
4. Voice: `own-voice.json` → ownvoice.py, 4 lines, 1 take each, no regenerations.

| Line | Text | Direction | Takes | Speech (s, silencedetect -40 dB) |
|---|---|---|---|---|
| `learner-mansion` | “I live in a mansion.” | custom style: friendly Japanese learner, clear English, light accent, every word pronounced correctly (the mistake is the meaning) | 1 | 0.29–1.89 |
| `us-apartment` | “I live in an apartment.” | `us` preset | 1 | 0.20–1.49 |
| `us-outlet` | “Outlet.” | `us` preset | 1 | 0.33–0.87 |
| `us-complaint` | “Complaint.” | `us` preset | 1 | 0.23–1.05 |

   No deliberate mispronunciation in this episode, so no formant check was needed; the takes were trimmed by their measured leading silence (`TRIM` in `cues.json`), heads and tails left whole. A Whisper pass for timestamps produced no output on this machine and was not needed. Needs a human listen.
5. Sound (`scripts/mix.py`, kit Mix): soft pops on the hook and on “Wow, you're rich!”, a low boing on the panic (×0.6), the bed drops to 30 % during the panic and comes back with the card, a soft tap before each quick-fire word, a quiet pofu + falling boing + poof for the deflating castle (lowered after a level check: the first pass peaked at -3.7 dBFS, now -7.9). No bells. The loudness fix from episode 1 (measure, gain in front of a -1.5 dBTP limiter, measure again) is in `mix.py`: mix.wav -14.2 LUFS / -1.4 dBTP; the rendered MP4s measure -13.6 LUFS (ebur128) / -1.2 dBFS. Voice RMS about -12 to -14 dB vs the bed alone about -26 dB.
6. `hyperframes check`: `#think` moved with x/y instead of top/left (snap warning); the remaining layout item is the intended red strike over コンセント / クレーム. Contact sheet ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)): hook readable at frame 1, captions and bubbles at the top, faces clear, cast feet end at about y 1515; 「えっ…!?」 moved up off the Friend's ear. The English subtitle first sat at the series position (bottom 150 px, as in episode 1); moved in step 7. Japanese-only cut has no subtitles.

7. Commander review (2026-10-23): content approved; platform safe zones per the owner (quoted verbatim): 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」 Fixed: English subtitles moved fully above y 1500 and within x 60–880 (36 px, at most two lines; the explain subtitle split in two; the end-card subtitle moved to the top); the Friend moved left so his face stays left of x 900; the small Mimi and the お手本 tags on the explain and quick-fire cards moved out of the right rail (x > 900, y 820–1520); first text lines of the hook, card titles and CTA start at y ≥ 200; the end card moved up 70 px so the store badge clears the bottom zone. Checked on an overlay sheet with the three zones drawn every ~1.5 s ([process/01-safe-zones.jpg](process/01-safe-zones.jpg)). Sound unchanged (-13.6 LUFS in the MP4s). Drive: the first drafts moved to `old/` with a `_v1` suffix.

## Uncertain / for review

- The Friend's line is normal English on purpose; the joke is only the meaning, carried by the castle bubble and Mimi's “Wow, you're rich!”.
- The castle bubble deflating sits inside the CTA beat (12.1 s) so the end card still starts at 13.6 s.
- The owner's (adult male) voice on the Friend and as the model, as in earlier episodes.

## Owner approval

- 2026-10-23: 「全部OK」 (all twelve shorts of the 055–066 batch approved as delivered; the Drive cuts were renamed without `_draft_`: `KT2_Mansion_2026-10-23.mp4`, `KT2_Mansion_EN-subs_2026-10-23.mp4`).
- Earlier owner notes in the same review round (2026-10-23): 「56の英語音声少し切れている？」 (clipped English in 056; led to the voice-cut audit of every episode); 「62透過されている？」 (the see-through angry pose in 062; fixed there with a filled pose).
