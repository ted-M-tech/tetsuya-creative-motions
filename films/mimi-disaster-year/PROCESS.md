# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- Standing series rules carried from earlier episodes (films/mimi-disaster-hat/PROCESS.md): own voice for every pronunciation line, medical-style mouth panels, punchline-first hook, Mimi's first person 「僕」.

## Steps and decisions

1. Brief from the commander (batch 055–066): New Year's morning; the Friend greets Mimi “Happy New Ear!”; flash-forward: Mimi solemnly hands the Friend a pair of earmuffs, hook 「Happy New 耳👂？」; Mimi: 「それ「新しい耳」に聞こえてる〜！！」. Mimi and the Friend only (the owner: 「メインはうさぎ二人ね」), so Mimi is the one greeted and the earmuff gag is hers; no side cast, no Kokoro. Started from episode 12 (`films/mimi-disaster-hat/source/`), same beats, ids and cue times (18.81 s).
2. Art: one codex-p run drew Mimi solemnly presenting pink earmuffs, a gift-wrapped ear icon and a winter shrine plate for New Year's morning (the library `shrine` plate has cherry blossoms, wrong season) ([prompts/01-codex-cast-and-heard.txt](prompts/01-codex-cast-and-heard.txt)). The ear icon replaces the 👂 emoji (deterministic rendering). Mouth panels reused from episode 2 (mimi-disaster-beach): /iː/ (tongue high and front, teal arrow up) stands for the “y” onset, /ɪ/ (tongue lower, coral arrow down) for the bare vowel of “ear”. Other poses from the library.
3. Voice: `own-voice.json` → ownvoice.py (owner's registered voice), one take each, no regenerations.

| Line | Text | Direction | Takes |
|---|---|---|---|
| `learner-ear` | “Happy New Ear!” | custom learner style (“Ear” starts directly on the vowel like Japanese 「イヤー」, no y) | 1 |
| `native-year` | “Happy New Year!” | `us` preset | 1 |

   Acoustic check (Praat, 20 ms frames; Whisper used for timestamps only, it wrote “year” for both):

| | “New” → next word | Onset of the word | Vowel / ending |
|---|---|---|---|
| native “New Year” | voicing continuous (intensity stays 77–80 dB) | F2 jumps from ~1220 Hz (“New”) to **~2670 Hz at 0.76–0.78 s** with F1 ~290 Hz: the /j/ glide, then falls 2460 → 2020 Hz | F3 falls to ~1850 Hz (American r) |
| learner “New Ear” | **voice break** at 1.34–1.36 s (intensity drops to 58 dB, −28 dB), a fresh vowel onset | F2 ~2700 Hz from the restart (a plain 「イ」), no glide out of “New” | open 「ア」 (F1 ~850, F2 ~1500 Hz), F3 stays ~3000 Hz: no r, Japanese 「イヤー」 |

   So the model has the /j/ glide joined to “New”; the learner restarts on a bare vowel after a glottal break. Needs a human listen (the learner's 「イ」 onset is high; a listener may hear “ee-yah”).
   Mix: the learner take starts at 2.0 s, “Ear” lands at 3.38 s; card clips “Ear” (take 1.33 s + 0.70) at 8.5 s and “Year” (take 0.70 s + 0.42) at 9.6 s.
4. Card: 最初に「ィ」を一瞬！ — year: 舌を上あごへ 「ィ」から始める; ear: 「ィ」なしの「イヤー」は ear.
5. App: `app-capture/Walkthrough.swift` + `year-lesson.patch` (capture-only fixture tweak: the first daily sentence becomes “Happy New Year!” and the fixture finding points at “Year” /j/). The lesson screen, お手本 button, score card and flagged-word row are the real app (`lesson.model`, `lesson.record`, `feedback.scores` in native-ios origin/main, `HomeTestSupport.swift` `openDailyLesson`); the sentence, the feedback wording and the score are fixture data. Take recorded under the shared simulator lock (app 5f5571ad); in this build the lesson opens with the fixture score already shown, so the cut is: sentence + score (お手本 tap overlay), the record button, the flagged-word row (「年 /jɪ/ 舌を上あごに近づけて「ィ」を一瞬、それから year。」), stopping before the offline fixture's scoring error (`app-capture/segments.sh`). No 「QA用データ」 text is visible in the used segments. Cut with `scripts/app_track.sh`.
6. Sound: `scripts/mix.py` (kit Mix): boing, rewind, record scratch, freeze, a soft pofu as Mimi holds out the earmuffs; the bed stops at the freeze and returns with Mimi; voice loudest, BGM ~21 dB under.
7. Checked with `hyperframes check` (passes; warnings only for id-less subtitle clips, as in earlier episodes) and a contact sheet of the key moments ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)): captions top, faces clear, bottom 400 px clear apart from the EN subtitle. Both cuts 1080×1920, 60 fps, 18.82 s, no rotation tag. Mix: integrated -15.3 LUFS, true peak -1.5 dBFS (kit `Mix.write`, peak-limited).

## Uncertain / for review

- The learner voice is the owner's (a young adult man) on the Friend.
- The flagged-word feedback text in the app shot is written for the capture; the UI is real.
