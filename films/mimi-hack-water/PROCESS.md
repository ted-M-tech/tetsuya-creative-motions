# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- 2026-10-23 (safe zones, batch rule): 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」
- 2026-10-23 (series look, batch rule): 「フォントの色とか変わってる？統一感出して過去と」

## Steps and decisions

1. Brief from the commander: Pronunciation Hacks episode 2, Notion ID 073, US flap T (water, better), labelled US, UK only as a small note. Branch from `feat/mimi-hack-check-it-out` (episode 1, the series template); `source/` copied, beat ids and element ids kept.
2. Story ≈15 s (same clock as episode 1): hook 「“ウォーター”じゃ水が出ない」 over the restaurant, Mimi as the waiter with an empty glass; the Friend's katakana “Wo-o-ta-a, please.”, the waiter blank, 「キョトン…」; the card with a tongue-tap icon and the own-voice US models; the Friend says it with the tap and the water arrives; CTA 「次のコツは？」; end card + tap. Mimi in a role outfit plays the other party (no side cast).
3. Art: no waiter pose existed in the library, so three Mimi waiter poses (empty glass blank, “Sorry?” ear cup, serving a full glass) and a restaurant plate with an empty table (the films/mimi-disaster-fork plate already had a glass of water on the table, which would spoil the joke) were drawn with codex-p from the cast references: [prompts/01-codex-mimi-waiter.txt](prompts/01-codex-mimi-waiter.txt) (+ log). Poses cut out with `cutout.sh`, checked on a dark background (solid fills, the L on the viewer's left cup). Library: `presenter`, `point`, `friend-hello`, `friend-order`, `friend-yay`. The plate is scaled 1.14 from the top and its table edge redrawn in front of the cast (`#plate-front`), so the cast stand behind the table with the glass visible.
4. Voice: `own-voice.json` → ownvoice.py. Generated: `learner-wota` (1 take), `us-water` (1 take), no regenerations. **Not generated**: `us-better`. The Gemini TTS project hit its daily limit (“Rate limit exceeded for model gemini-3.8-flash-tts (limit: 100 requests per day on Tier 1)”, shared by the whole batch) after the second line; 8 retries over ≈10 min all returned 429 (no audio was returned). The planned `us-water-please` line was dropped (the Friend's fix line reuses “Water.”, bubble “Water!”) to save a paid line. Draft v1 shows the “better” row without audio; to be filled after the quota resets (see README).

   Acoustic check (5 ms steps / 20 ms window: RMS vs clip peak, energy < 500 Hz and 3–8 kHz; ffmpeg silencedetect −40 dB / 60 ms; spectrograms in [process/01-takes-waveform.jpg](process/01-takes-waveform.jpg)); a transcript was not used:
   - Learner “Wo-o-ta-a, please.”: three chunks 0.32–0.95 (wo-o), 1.12–1.65 (ta-a), 1.90–2.62 (please). Before “ta”: a ≈130 ms silent closure (1.00–1.115 at −50…−64 dB, no low-band energy = voiceless), then a release burst at 1.12 where the 3–8 kHz band is at or above the low band for ≈25–30 ms before voicing starts (1.15) = a hard, aspirated t. No r colouring in the long “a-a”.
   - Model “Water.”: speech 0.21–0.67, no silence inside. One short dip at 0.460–0.485 (≈25 ms): RMS −18 dB vs −9 dB in the vowel before, the < 500 Hz band only ≈4 dB down (voicing continues through the closure), the 3–8 kHz band drops ≈20 dB and does not spike after the release (no burst, no aspiration); then the r-coloured vowel (F3 down to ≈1.8 kHz). = a voiced flap, the target. Needs a human listen.
   - Cuts: placed only at measured silence (`TAKES` in `cues.json`: learner 0.24 + 2.50 s, water 0.14 + 0.80 s); `scripts/mix.py` asserts the first and last 10 ms of every placement are ≤ −38 dB vs the clip peak (measured −56.3 to −62.7 dB).
5. Sound (`scripts/mix.py`, kit Mix): soft low ticks on the learner's chunks and on the tongue tap, pencil strokes for the tap marks, ding + pops when the water arrives, whooshes on scene changes, pochi on the CTA tap; the bed is the kit theme at kit level (no extra dip: the learner take has no pauses to expose). Post-gain + limiter step as in episode 1: mix.wav −14.0 LUFS, −2.3 dBTP; both rendered cuts −14.1 LUFS, −1.9 dBTP. Voice windows ≈ −12…−14 dBFS RMS vs ≈ −22 dBFS for the bed alone under the hook and the silent “better” row.
6. Edit: the learner's chunks light on their measured starts; the waiter switches to the ear-cup pose at 4.3. On the card the t is red with a blue tap mark (three short rays, drawn by the template's `draw()`); on the measured flap of the model (6.1 + 0.33 s) the t turns blue, a small ラ pops under it and the tongue icon taps. `hyperframes check` passes (layout 0 issues, contrast 32/32).
7. Safe zones (EN cut, overlay every ≈1–1.5 s: [process/02-safe-zones.jpg](process/02-safe-zones.jpg)): top captions and card titles start at y ≥ 200 (hook card background from 165 as in episode 1); EN subtitles inside x 60–880, box bottom y 1490; nothing in y > 1500 except the plate's tablecloth and the kit end card's App Store badge (kit layout, every episode); the right rail holds no text: only the empty right part of the card rows' boxes and a little of Mimi's headphone, her face stays left of x 900. The cast were raised 60–90 px vs episode 1 so the glass shows above the table.

## Series look

- Diffed against episode 1's CSS: same colour roles (red #e5484d = the t as written / the wrong reading, blue #2a8dff = the tap and the correct sound, yellow #ffd84a in the tip pill, #5b7f9f secondary text, #273b4b ink), same fonts, weights and sizes for hook (124/100/52), title 74, rows 150, bubbles 92, reaction 80, CTA 104/64, subtitles 36. Added only: the small ラ under the t (0.38 em of the row word), the UK note (38 px, #5b7f9f) and the tongue icon label (40 px, #5b7f9f, like the tags); the tap-mark stroke is 10 px (episode 1's arcs 13 px) because three short rays at 13 px read as a letter “w”.

## Uncertain / for review

- “Better.” model take missing in draft v1 (quota); the model beat currently has no voice.
- 「ラ（d）」: the flap is described as a light d / ラ行, per the brief; the card says “US” and the note says UK usually keeps the t.
- The Friend's fix line reuses the isolated “Water.” take (said as “Water!”), not “Water, please!”.
- Hook uses no voice (the joke is read in 1.5 s, then the learner take starts at 2.1).
- Drive folder `073. Pronunciation Hacks 2 - Water (US T)`: created if missing, with the name from the brief.
