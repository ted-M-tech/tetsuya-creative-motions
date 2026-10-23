# PROCESS

## The owner's words

- Series request (2026-10-21): 「同じような発音でとんでもない勘違いシリーズも作って。Shit、sitとか。よくある系でウケる、フック強烈に」.
- Episodes 7–12 (2026-10-22): 「1.それでいこう」 (the batch plan approved; this is episode 7, six / s*x).
- Standing rules from earlier episodes (see films/mimi-disaster-peace/PROCESS.md): own voice for every pronunciation line, punchline-first hook, medical-style mouth panels, cute “what they heard” gag (tasteful, no anatomy), cast = Mimi + Friend + recurring side cast, Mimi says 「僕」.

## Brief (from the batch commander)

The Friend, at a restaurant entrance, tells Pippa (staff) “A table for six, please.”: Japanese シックス with the i flattened toward /e/ so it lands as “sex”. Pippa freezes. Punchline 「それ、S★xに聞こえてる！」. Gag object cheeky, not explicit (a blushing heart / Pippa covering her eyes). The fix: short /ɪ/ (“six”) vs /ɛ/ (“sex”); mouth card about the relaxed short i. The learner take must actually sound like “sex”, verified by vowel formants against the native take.

## Steps and decisions

1. Started from episode 6 (mimi-disaster-peace, itself the pilot's layout): same beats, cue sheet and ids; only the slip word moved (WORD 4.10 → 3.45 s).
2. Art: one codex-p run ([prompts/01-codex-cast-and-plate.txt](prompts/01-codex-cast-and-plate.txt)) drew Pippa as the restaurant host (smiling with menus; covering her eyes, blushing, menus dropped), Mimi blushing and yelling, the shy-heart icon and the restaurant plate. The Friend uses library poses (friend-hello, friend-oops, friend-yay). Another run ([prompts/02-codex-mouths.txt](prompts/02-codex-mouths.txt)) drew the /ɪ/ (target, teal arrow: tongue stays high) and /ɛ/ (slip, coral arrow: tongue and jaw drop) panels in the style of the series' earlier mouth art; `scripts/art.sh` splits each into the side and front panels.
3. Voice (own-voice.json → ownvoice.py; Praat formants via parselmouth, Burg, 5 formants up to 5 kHz, steady part of the vowel):

| Take | Text sent | Vowel F1 / F2 (Hz) | Heard as |
|---|---|---|---|
| native-six (us) | A table for six, please. | ~470 / ~1900 | six |
| learner take 1 | A table for sex, please. | ~455 / 1900–2100 | six |
| take 2 (stronger style) | same | ~370 / 2150–2400 | “seeks” / six |
| take 3 (plain style) | same | ~380 / ~2000 | six |
| take 4 | A table for secks, please. | ~420 / 1900–2400 | six |
| **used: take 1, vowel edited** | | **~600 / 1750–2100** | **sex** |

The TTS would not open the vowel to /ɛ/ in four generations (the regeneration limit of 3 was reached), so the vowel of take 1 (1.795–1.872 s) was moved with a Praat source-filter edit: LPC inverse filter → source, Formant → FormantGrid with F1 × 1.35 and F2 × 0.92 inside the vowel → filter, level-matched and spliced back with 15 ms crossfades ([source/scripts/vowel_shift.py](source/scripts/vowel_shift.py)). F1 now sits ~130 Hz above the native “six” (an /ɛ/ for this voice) while the rest of the take is untouched. As a side check only, Whisper medium.en, which wrote “six”/“4-6” for the raw takes, writes “A table for sex, please?” for the edited one. Raw takes are kept in Drive `Disasters7_Six_assets/own-voice/takes/`. Needs a human listen on earphones.
4. Pippa: Kokoro `af_nicole` (her fixed voice), “Um… a table for… sex?!” (`scripts/voices.sh`).
5. App: `app-capture/Walkthrough.swift` + `six-lesson.patch` (capture-only fixture tweak: the first daily sentence becomes “A table for six, please.” and the fixture finding points at “six”, /ɪ/). Lesson screen, お手本 button, record button, score card and flagged-word row are the real app (identifiers `lesson.model`, `lesson.record`, `feedback.scores` on native-voice-clone origin/main); sentence, feedback wording and score are fixture data. Cut with `scripts/app_track.sh`. The first take showed 「sex」 uncensored in the fixture feedback text; the patch was changed to name only 「セ」 and the take redone (raw take in Drive `Disasters7_Six_assets/six-lesson-take.mov`).
6. Sound: `scripts/mix.py` (kit Mix), as episode 6: boing on the punchline, tape rewind, record scratch and the bed stopping dead at the freeze, the slip and the model word on the card, the native line again at the fix.
7. Commander note (2026-10-22): episode 6's yellow multiply freeze layer was a pee joke for that episode only and tints the Friend; the freeze uses episode 5's desaturate layer (#9aa6b2, saturation blend) so the Friend stays white.
8. Checked with `hyperframes check`, ffprobe (1080×1920, 60 fps, no rotation, 20.05 s) and a contact sheet ([process/00-final-frames.jpg](process/00-final-frames.jpg)).

## Uncertain / for review

- The learner word is an edited take (see 3). If it sounds processed on earphones, the alternative is a fresh generation with a different text trick, which needs the owner's OK (paid, limit reached).
- The flagged-word feedback text in the app shot is written for the capture; the UI is real.
- The learner voice is the owner's (a young adult man) on the Friend.

## Owner approval

- 2026-10-22: 「6本ともOK。限定公開して」 (episodes 7–12 approved as delivered; the Drive cuts were renamed without `_draft_`: `Disasters7_Six_2026-10-22.mp4`, `Disasters7_Six_EN-subs_2026-10-22.mp4`).
