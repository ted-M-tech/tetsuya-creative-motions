# PROCESS

## The owner's words

- Batch request (2026-10-23): 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- Approval (2026-10-23): 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- Standing series rules (films/mimi-disaster-sit, films/mimi-disaster-peace): own voice for every pronunciation line, medical-style mouth panels, punchline-first hook, Mimi's first person 「僕」.

## Steps and decisions

1. Brief from the commander (batch 055–066): Mimi in a fruit-stall apron (role outfit, so no Pippa) hands the Friend a strawberry; “Thank you berry much!”; Mimi keeps piling on strawberries; flash-forward of the Friend buried in strawberries with the hook 「Thank you ベリーマッチ🍓」; Mimi out of role: 「それ「いちご」に聞こえてる〜！！」. The Notion plan had Pippa as the keeper; replaced by Mimi per the owner's cast rule. Started from episode 12 (`films/mimi-disaster-hat/source/`), same beats and ids, same clock (18.81 s).
2. Art: one codex-p run ([prompts/01-codex-cast-and-plate.txt](prompts/01-codex-cast-and-plate.txt)) drew Mimi as the stall keeper (giving one strawberry / piling an armful), the Friend buried in strawberries, the strawberry icon (used instead of the 🍓 emoji in the hook, so it renders the same everywhere), a small strawberry for the pouring gag and the fruit stall (placed on the library `street` plate). The Friend's other poses (`friend-amazed`, `friend-yay`) and Mimi's `point`, `jump`, `confident` are library poses. No other characters.
3. Mouth panels: one codex-p run ([prompts/02-codex-mouths.txt](prompts/02-codex-mouths.txt)) drew /v/ (upper teeth resting on the lower lip, voiced airflow lines) and /b/ (both lips closed), with episode 4's mouth-l / mouth-r attached as the style reference; `scripts/art.sh` splits them into the two panels. The side panel header is 歯と唇（横から） (the point is the teeth and lips, not the tongue).
4. Voice: `own-voice.json` → ownvoice.py (owner's registered voice), one take each, no regenerations.

| Line | Text | Direction | Takes |
|---|---|---|---|
| `learner-berry` | “Thank you berry much!” | custom learner style (clear B, both lips closed then popping open) | 1 |
| `native-very` | “Thank you very much!” | `us` preset | 1 |

   Checked on the waveform (5 ms frames, band energies 50–400 Hz / 400–2000 Hz / 2.5–8 kHz) and a spectrogram ([process/02-b-vs-v-spectrogram.jpg](process/02-b-vs-v-spectrogram.jpg); top = learner 0.6–1.3 s, bottom = native 0.42–1.12 s):
   - learner “berry”: 0.835–0.905 s only a low voice bar (low band ~20 dB, mid band down to −16 dB, high band −38 dB: lips closed), then at 0.91 s a vertical burst across all frequencies (mid band +22 dB in 5 ms) into the vowel. That is a voiced /b/: closure + release burst.
   - native “very”: 0.665–0.71 s energy dips but voicing continues without a gap, the 2.5–8 kHz band stays at −10…−2 dB (frication noise), and there is no burst. That is a voiced /v/.
   Whisper (whisper-cli medium.en) writes “very” for both takes, as expected (it corrects the word); used for nothing. Needs a human listen.
5. Card: 「V」は歯を唇に！ — very: 上の歯を下唇に軽く当てて声を; berry: 両唇を閉じると berry（いちご）; the learner word (0.80–1.20 s of the take) at 8.5 s, the model word (0.64–0.90 s) at 9.6 s.
6. App: `app-capture/Walkthrough.swift` + `very-lesson.patch` (capture-only fixture tweak: the first daily sentence becomes “Thank you very much!” and the fixture finding points at “very” /v/). The lesson screen, お手本 button, score card and flagged-word row are the real app (`lesson.model`, `lesson.record`, `feedback.scores` in native-ios origin/main); the sentence, the feedback wording and the score are fixture data. Cut with `scripts/app_track.sh`.
7. Sound: `scripts/mix.py` (kit Mix): boing, rewind, record scratch, freeze, six soft thuds as the strawberries land; no side cast voice (“More berries!” is a bubble only); the bed stops at the freeze and returns with Mimi; voice loudest, BGM ~21 dB under.
8. Loudness: after `Mix.write`, the mix is measured and the missing gain added in front of a limiter (the step from films/mimi-katakana-mcdonalds), so the film sits at -14.1 LUFS integrated, true peak -1.6 dBTP, balance unchanged.
9. Checked with `hyperframes check` and a contact sheet of the key moments ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)).

## Uncertain / for review

- The learner voice is the owner's (a young adult man) on the Friend.
- The flagged-word feedback text in the app shot is written for the capture; the UI is real.

## Commander review (2026-10-23)

- Draft v1 was -15 LUFS and the small Mimi on the card and app beats sat in the bottom 400 px. Fixed in v2: loudness step added to `scripts/mix.py`; card Mimi (170 px, centred between the columns) and app Mimi (260 px) moved up to end above y = 1520. v1 cuts moved to Drive `old/` with `_v1`.
- Owner on platform safe zones (2026-10-23): 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」 Fixed in v3: EN subtitles moved fully above y 1500 within x 60–880 (end-card subtitle above the end-card Mimi); top text starts at y ≥ 200; the card columns end at x 900 and the stall-keeper Mimi, the strawberry icon, ドサドサッ! and the お手本＝自分の声 tag moved left of the action rail (x > 900, y 820–1520); the cast moved up 150 px and the small Mimis moved so faces stay clear of the subtitle band. Checked on a zone overlay of the EN cut ([process/03-v3-safe-zones.jpg](process/03-v3-safe-zones.jpg)). v2 cuts moved to Drive `old/` with `_v2`. Loudness unchanged (-14.1 LUFS, -1.6 dBTP).
