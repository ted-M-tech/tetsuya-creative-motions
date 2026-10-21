# PROCESS

## The owner's words

- Series request (2026-10-21): 「同じような発音でとんでもない勘違いシリーズ…よくある系でウケる、フック強烈に」, then 「それらも作って」 (episodes 2–6 after the pilot 037 sit / sh*t).
- Own voice for every pronunciation line: 「今まで英語で発音シーンがあった動画、この声で変えて。010以外。」 (the rule for all shorts since 2026-10-21).
- On the pilot's comparison card: 「もう少し口の形っぽく」 → first answered with code-drawn front-view lips, then superseded by the illustrated panels below. Shapes: ee = spread with teeth, short i = relaxed, r = rounded with the tongue pulled back, l = tongue tip up behind the upper teeth, oʊ = rounded, ɑ = wide open.
- Owner feedback on the pilot (2026-10-21), applied here: pronunciation illustrations in a soft semi-realistic medical-education style (side cross-section + front lips, panels with navy headers); a punchline-first hook (frame 1 = Mimi's punchline, e.g. 「それ、B★tchに聞こえてる」 / 「それ、シラミに聞こえてる」, censored with ★, then a rewind to the scene); a cute illustration of the misheard thing (tasteful/kawaii; for erection only a comedic cue such as a blushing Mimi covering her eyes, no anatomy).
- Owner rule (2026-10-21): Mimi's first person in Japanese text is 「僕」.

## Steps and decisions

1. Built in parallel with the pilot; its layout (hook → slip → freeze → Mimi → card → app → fix → end) was reused from the pilot worktree before it was pushed. Episodes 2–6 were generated from one shared beat sheet so the timing rules are the same, and vary the scene, the cast, the listener's reaction gag, Mimi's pose and entrance.
2. Art: one codex-p run per episode drew the learner (two poses), the listener (two poses), Mimi's reaction and the plate in the official 2D style from the official references ([prompts/01-codex-cast-and-plate.txt](prompts/01-codex-cast-and-plate.txt)). The first run was interrupted when the session ended; the second run kept the files the first had saved (log: `01-codex-cast-and-plate.run1.log`, `01-codex-cast-and-plate.log`).
3. Voice: own-voice.json → ownvoice.py. Whisper (small.en/medium.en word timestamps) was used to measure the words and as a rough check of what a listener hears; formants (Praat) were measured where Whisper's language model “corrected” the rude word back to the polite one.

| Line | Text | Direction |
|---|---|---|
| `learner-piss` | “Okay, everyone, piss!” | custom learner style |
| `native-peace` | “Okay, everyone, peace!” | us preset |

learner-piss: three takes. Kept take 2 (vowel F1 ≈ 420 Hz, F2 ≈ 1900 Hz, a lax ɪ; the native “peace” is F1 ≈ 290, F2 ≈ 2380). Take 3 measured closer to iː and was discarded (receipt updated to take 2). Whisper writes “peace” for every take. Needs a human listen.
4. Illustrations: one codex-p run drew the six mouth illustrations shared by episodes 2–6 (ee, short i, r, l, oʊ, ɑ; side cross-section on top, front lips below, no text; [prompts/02-codex-mouths.txt](prompts/02-codex-mouths.txt), a web image was attached as a style reference only and is not kept in this public repo); `scripts/art.sh` splits each into the two card panels. Another drew the kawaii “what they heard” icons ([prompts/02-codex-heard.txt](prompts/02-codex-heard.txt)): b*tch → a cute puppy with a ribbon, lice → three tiny smiling bugs, c*ck → a proud rooster, p*ss → a smiling toilet; election uses Mimi blushing behind her mittens (no object).
5. App: `app-capture/Walkthrough.swift` + `peace-lesson.patch` (capture-only fixture tweak: the first daily sentence becomes the episode's sentence and the fixture finding points at the word). The lesson screen, お手本 button, score card and the flagged-word row are the real app; the sentence, the feedback wording and the score are fixture data. Cut with `scripts/app_track.sh`.
6. Sound: `scripts/mix.py` (kit Mix): a boing on the punchline, a code-made tape rewind, the theme bed stops dead at the freeze and comes back with Mimi (as in the pilot); the pilot's record scratch; the native take again when the line is said right; voice loudest, BGM ~21 dB under, SFX softened.
7. Checked with `hyperframes check` and contact sheets of the key moments ([process/00-final-frames.jpg](process/00-final-frames.jpg)).

## Uncertain / for review

- The flagged-word feedback text in the app shot is written for the capture (the fixture's own text says QA用データ); the UI is real.
- The learner voice is a young adult man for every learner character (by the own-voice rule).
