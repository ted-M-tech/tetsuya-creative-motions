# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- 2026-10-23 (safe zones, batch rule): 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」

## Steps and decisions

1. Brief from the commander: new series “Pronunciation Hacks” (one quick, correct tip per episode), episode 1 = linking (check‿it‿out, pick‿it‿up), Notion ID 072; consonant→vowel linking only, no flap-T claim (episode 2 is water / flap T). Generic beat ids (hook, slip, tip, model, fix, cta, end) and a Series template section in README so episodes 2–4 copy `source/`. Layout from `films/mimi-katakana-mcdonalds` (cards).
2. Story ≈15 s: hook 「チェケラ ＝ Check it out」 with the smooth model take under it (so the viewer hears why チェケラ ≈ the phrase); the Friend's robotic “Check. It. Out.”; Mimi's card with link arcs and two own-voice models; the Friend says it smoothly; CTA 「次のコツは？」; end card + tap. The optional real daily-lesson shot was skipped: it would add ≈3 s and no new information to a 15 s tip.
3. Art: library only (plate `meeting`; Mimi `grin`, `talk`, `presenter`, `point`, `highfive`; Friend `friend-amazed`, `friend-speech`, `friend-yay`, `friend-hello`). All checked on a dark background (no see-through fills). The first draft used `friend-proud`, which holds a rice bowl; swapped for `friend-yay`.
4. Voice: `own-voice.json` → ownvoice.py, 3 lines, 1 take each, no regenerations.

| Line | Text | Direction | Takes |
|---|---|---|---|
| `learner-robot` | “Check. It. Out.” | custom style: Japanese beginner reading word by word like a stiff robot, a silent pause of about half a second between the words, no linking, flat pitch | 1 |
| `us-check-it-out` | “Check it out!” | custom native style: one smooth unit, k flows into “it”, t flows into “out”, no pause | 1 |
| `us-pick-it-up` | “Pick it up!” | the same for pick‿it‿up | 1 |

   Acoustic check (20 ms RMS envelope, ffmpeg silencedetect −40 dB / 60 ms, spectrogram: [process/01-takes-waveform.jpg](process/01-takes-waveform.jpg)); a transcript was not used:
   - Learner: three separate words with real gaps. Speech 0.32–0.96 (“Check” + a short katakana-like echo vowel, chekku), silence 0.98–1.52 (≈0.54 s, ≤ −44 dB vs peak), 1.54–2.02 (“It”, itto), silence 2.04–2.58 (≈0.54 s), 2.60–3.04 (“Out”, auto). The added echo vowels are the learner style, not linking.
   - Model “Check it out!”: speech 0.20–1.12 with no silence inside (silencedetect finds only the head and tail); the deepest dip is a ≈40 ms stop closure at 0.50–0.56 at −17…−25 dB, i.e. a consonant hold, not a pause; the voicing runs on from “it” into “out”.
   - Model “Pick it up!”: speech 0.24–0.88, no silence inside; dips only at the k closure (0.38, −22 dB).
   - Cuts: every take is placed at measured silence (`TAKES` in `cues.json`); `scripts/mix.py` asserts the first and last 10 ms of each placement are ≤ −38 dB vs the clip peak (measured −55 to −68 dB). Needs a human listen (in particular whether “Check it out!” sounds flapped; the film makes no claim about the t).
5. Sound (`scripts/mix.py`, kit Mix): a soft low sine tick on each robot word, pencil strokes as the arcs draw, ding + pops on the high five, whooshes on scene changes, pochi on the CTA tap; the bed dips to 35 % under the robot reading so its pauses are heard as gaps (pause windows −35 dB mean vs −12 dB in voice windows). The kit's loudnorm left the mix at −16.3 LUFS; the post-gain + −2.4 dB limiter step from mimi-katakana-mcdonalds (with an overshooting step, as the limiter eats part of each gain step) brings it to −14.2 LUFS; both rendered cuts −14.2 LUFS, −1.7 dBTP.
6. Edit: words in the robot bubble light on their measured starts with a stiff jolt; dotted red gaps appear in the pauses. Link arcs under k‿i / t‿o are SVG arcs revealed by a clip (a dash-offset draw broke with non-scaling strokes in the first render: arcs looked cut off). `hyperframes check` passes (layout 0 issues, contrast 39/39; the warnings are the same nested-structure notes as the template).
7. Safe zones (EN cut, overlay [process/02-safe-zones.jpg](process/02-safe-zones.jpg)): top text starts at y ≥ 200 (hook card top 165, card title 200); EN subtitles x 60–880, box bottom y 1490; right rail (x > 900, y 820–1520) holds no text or bubble, faces stay left of x 900; the cast was moved up 80 px after v0 so the subtitle sits under the faces, not over the chins. The kit end card's App Store badge stays in the bottom zone (kit layout, as in every episode).

## Series look (2026-10-23, v2)

- Owner (batch rule): 「フォントの色とか変わってる？統一感出して過去と」
- Diffed the CSS against the template (films/mimi-katakana-mcdonalds): v1 had added an orange (#ff9f1c) for the link arcs, the active row border and the CTA word, and drifted sizes (hook 150/96 px, card title 70, CTA 112/62, fix bubble 104, reaction word 76). v2 uses only the template's colour roles (red #e5484d = the wrong reading and the final consonant, blue #2a8dff = the vowel, the links and the active row, yellow #ffd84a in the tip) and its sizes (hook 124/100, title 74, CTA 104/64, bubbles 92, reaction 80); the robot words are red like the template's katakana. Fonts and weights unchanged (kit font, Helvetica Neue for English, 700).
- v1 drafts moved to Drive `old/` (`*_v1.mp4`).

## Uncertain / for review

- 「チェケラ」 is used as the familiar Japanese spelling of the phrase, not as a pronunciation target.
- The owner's (adult male) voice on the Friend, as in earlier episodes; the Friend's smooth line reuses the model take.
- Drive folder `072. Pronunciation Hacks 1 - Check It Out` did not exist yet; created with the name from the brief.

## Owner approval

- 2026-10-23: 「あと全部確認した。YouTubeあげてOK」 (the v2 draft approved as delivered; the Drive cuts were renamed without `_draft_`: `Hacks1_CheckItOut_2026-10-23.mp4`, `Hacks1_CheckItOut_EN-subs_2026-10-23.mp4`).
