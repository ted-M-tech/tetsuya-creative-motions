# PROCESS

## The owner's words

- Series request: 「同じような発音でとんでもない勘違いシリーズも作って。Shit、sitとか。よくある系でウケる、フック強烈に」
- Batch 7–12 (2026-10-22): 「1.それでいこう」 (episodes 7–12 approved; this is episode 9, lunch / launch).
- Standing rules from earlier episodes: own voice for every pronunciation line; medical-style mouth panels (唇（正面） / 舌の位置（横から）); punchline-first hook; Mimi's first person 「僕」; cast = Mimi + Friend, side roles only Bruno / Pippa / Coco (「メインキャラは二人。ミミと友達。…統一感持たせたい」).

## Steps and decisions

1. Built by a child agent of the batch commander (shared brief for episodes 7–12). Source copied from episode 6 (`mimi-disaster-peace`, itself the pilot's layout with the same beat ids); pair, place, side cast, gag, card, app patch and lines swapped. Not rude, so nothing is starred: the gag is visual (a rocket).
2. Art: one codex-p run drew the Friend (bento, asking / shocked), Coco (sundress smile / space helmet salute), a big cute rocket, Mimi riding a rocket and a park plate from the cast references ([prompts/01-codex-cast-plate-rocket.txt](prompts/01-codex-cast-plate-rocket.txt), log next to it). A second run drew the two new mouth panels /ʌ/ and /ɔː/ with the series' earlier panels attached as the style reference ([prompts/02-codex-mouths.txt](prompts/02-codex-mouths.txt)). `scripts/art.sh` cuts them out and splits the mouth images into the card panels.
3. Voices: own-voice.json → ownvoice.py, one take each (no regeneration). Coco: Kokoro `af_bella` (`scripts/voices.sh`).

| Line | Text | Direction |
|---|---|---|
| `learner-launch` | “Shall we have launch?” | custom learner style (rounded, long “aw”) |
| `native-lunch` | “Shall we have lunch?” | us preset |

   Verified acoustically (Praat via parselmouth: formants every 20 ms, silencedetect for the word start), not with Whisper:
   - learner “launch” (word 1.54–2.30 s in the WAV, 0.76 s): vowel ≈ 1.66–1.84 s (≈ 180 ms), F1 ≈ 460–500 Hz, F2 ≈ 800–890 Hz: a back, rounded vowel /ɔ(ː)/.
   - native “lunch” (word ≈ 0.70–1.12 s, 0.42 s): vowel ≈ 0.78–0.87 s (≈ 90 ms), F1 ≈ 630–710 Hz, F2 ≈ 980–1280 Hz: open-mid, central, unrounded /ʌ/.
   - So the slip is about twice as long, with F2 ≈ 300 Hz lower (rounding/backing) and F1 ≈ 200 Hz lower. Needs a human listen.
4. App: `app-capture/Walkthrough.swift` + `lunch-lesson.patch` (capture-only: the first daily sentence becomes “Shall we have lunch?” and the fixture finding points at “lunch” /ʌ/). The lesson screen, お手本 button, record button, score card and flagged-word row are the real app (identifiers `lesson.model`, `lesson.record`, `feedback.scores` in native-ios on origin/main); the sentence, feedback wording and score are fixture data. Cut with `scripts/app_track.sh`.
5. Sound: `scripts/mix.py` (kit Mix): punchline boing, tape rewind, record scratch at the freeze (the bed stops dead and comes back with Mimi), a pop for the helmet, a soft low rocket rumble and a whoosh at liftoff, the takes on the card, the native take again when said right. Voice loudest, BGM ~21 dB under, SFX soft.
6. Checked with `hyperframes check` and snapshots of the key moments; layout fixes after the first look (punchline frame decluttered, the card's rocket gag moved off the panels, Mimi's bubble re-broken).

## Uncertain / for review

- The learner voice is the owner's (a young adult man) on the Friend; “Shall we have launch?” is the slip (the vowel only), the subtitle reads it as a rocket launch.
- The flagged-word feedback text in the app shot is written for the capture; the UI is real.
