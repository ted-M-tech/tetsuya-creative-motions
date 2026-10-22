# PROCESS

## The owner's words

- Series request: 「同じような発音でとんでもない勘違いシリーズも作って。Shit、sitとか。よくある系でウケる、フック強烈に」
- This batch (episodes 7–12, 2026-10-22): 「1.それでいこう」
- Standing rules from earlier episodes (see films/mimi-disaster-peace/PROCESS.md): own voice for every pronunciation line; medical-style mouth panels (lips front, tongue side); punchline first, censored with ★; cute, not explicit; Mimi says 「僕」; cast = Mimi + Friend + the recurring side cast only (「メインキャラは二人。ミミと友達。…統一感持たせたい」).

## Brief (from the batch commander)

Restaurant: the Friend calls Pippa (waiter): “Excuse me, can I get a fork?” — “フォーク” shortened and flattened toward /ʌ/ so it lands as the F-word. The whole restaurant freezes; Pippa drops the tray. Punchline 「それ、F★ckに聞こえてる！」 (word audible, starred on screen). Gag object: a giant fork with a censor bar / ★. The fix: “fork” /ɔːr/ long rounded vowel (+ r); the slip is a short /ʌ/. Verify by vowel duration + formants vs the native “fork”.

## Steps and decisions

1. Source copied from episode 5 (films/mimi-disaster-coke, the closest variant: ordering from Pippa), beats and ids kept, retimed for the longer line. The learner take is placed in two pieces (`T0` “Excuse me,” and `T1` “can I get a f*ck?”) so its 0.43 s pause becomes 0.3 s.
2. Art: one codex-p run ([prompts/01-codex-cast-and-plate.txt](prompts/01-codex-cast-and-plate.txt)) drew Pippa as a waiter (tray / shock), the tray alone (animated falling), Bruno frozen at the next table (the “whole restaurant freezes”), Mimi with a giant fork, the fork gag and the restaurant plate. The Friend reuses library poses `friend-hello` (calling the waiter) and `friend-shrink`. The censor bar of stars on the fork is HTML, not drawn. The plate's lower part is drawn a second time in front of the cast (`#table-front`, clip-path) so they stand behind the table.
3. Mouth panels: one codex-p run ([prompts/02-codex-mouths.txt](prompts/02-codex-mouths.txt)) drew /ɔːr/ (rounded, open “o”, tongue low and back, tip curling back for r) and /ʌ/ (relaxed, unrounded, tongue flat in the middle), with episode 5's mouth-ou / mouth-aa attached as the style reference; `scripts/art.sh` splits them into the two card panels.
4. Voice (owner's registered voice, ownvoice.py): `native-fork` (us) once; `learner-fuck` three takes (the limit), take 3 kept. Measured with Praat (parselmouth) on the stressed vowel, word boundaries by silencedetect and high-band (3–8 kHz) energy for the f; Whisper not used for judging.

| Take | Vowel (s) | Duration | F1 | F2 | F3 | Verdict |
|---|---|---|---|---|---|---|
| learner 1 | 3.46–3.61 | 150 ms | ≈ 450 Hz | ≈ 850 Hz | ≈ 3100 Hz | back and rounded, closer to “fock/fook”; rejected |
| learner 2 | 2.71–2.87 | 160 ms | ≈ 530–560 | ≈ 890 | ≈ 2960 | still /ɔ/-like (rounded); rejected |
| **learner 3 (kept)** | 2.70–2.85 | 150 ms | **≈ 680–800** | **≈ 1040** | **≈ 2830 (flat, no r)** | open, unrounded /ʌ/–/ɑ/ region: “f*ck” |
| native “fork” | 1.59–1.74 | 150 ms + r | ≈ 500–600 | 840 → 1350 | **falls to ≈ 1830** | rounded /ɔ/ then r-colouring |

   What separates the two takes is vowel quality, not length: the slip is more open (F1 +150–200 Hz) and unrounded (F2 starts ≈ 200 Hz higher) and has no r (F3 stays ≈ 2830 Hz, the native dips to ≈ 1830 Hz). The native “fork” in this question intonation is not longer than the slip (both ≈ 150 ms voiced before the r), so the card says 「唇を丸めて「オー」＋r」 vs 「短く平たい「ア」」 and the duration claim is left soft. Needs a human listen.
5. Pippa's line “Sorry… a WHAT?!” is Kokoro `af_nicole` (`scripts/voices.sh`).
6. App: `app-capture/Walkthrough.swift` + `fork-lesson.patch` (capture-only: the first daily sentence becomes “Excuse me, can I get a fork?”, the fixture's flagged word points at “fork” with /ɔːr/ feedback). Verified on native-voice-clone origin/main: `lesson.model`, `lesson.record` (PracticeScreen.swift), `feedback.scores` (AccountProgress.swift), `openDailyLesson` / `waitForHome` (LancloUITests/HomeTestSupport.swift), the `dp-liquids-1` sentence and the VisualQAData fixture the patch replaces. Sentence, feedback wording and score are fixture data; the UI is real.
7. Sound: `scripts/mix.py` (kit Mix): boing + tape rewind on the punchline, record scratch, a soft clang when the tray lands, bed stops at the freeze and returns with Mimi, the theme ~21 dB under the voice.

## Uncertain / for review

- Is the slip funny enough by ear? Formants say open unrounded /ʌ/ with no r; the owner should listen (take 3, 2.52–3.08 s).
- The flagged-word feedback text in the app shot is written for the capture; the UI is real.
