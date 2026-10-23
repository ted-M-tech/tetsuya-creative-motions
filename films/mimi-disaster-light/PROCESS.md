# PROCESS

## The owner's words

- Series request: 「同じような発音でとんでもない勘違いシリーズも作って。Shit、sitとか。よくある系でウケる、フック強烈に」
- This batch (episodes 7–12): 「1.それでいこう」
- Standing rules from earlier episodes (see [mimi-disaster-rice/PROCESS.md](../mimi-disaster-rice/PROCESS.md)): own voice for pronunciation lines, Mimi + Friend main cast with Bruno / Pippa / Coco only, Mimi's 「僕」, medical-style mouth panels, punchline-first hook.

## Steps and decisions

1. Built by a child agent from the commander's batch brief (Notion row 052). Template: episode 3 (rice / lice) source, same beats and ids; swapped the scene (dark living room at Bruno's home), the cast poses, the gag (Bruno turning right with a right-arrow sign, 「クルッ…」「（まだ真っ暗）」), Mimi's entrance (flashlight), the card and the app patch. The room is darkened in HTML (`#dark` multiply overlay) and lit at the fix when "light" is said (16.4 s), with a lamp glow.
2. Art: one codex-p run ([prompt](prompts/01-codex-cast-and-plate.txt), log alongside) drew the plate and five cut-outs; first take kept. Mouth panels r / l reused from episode 3 (same pair).
3. Voice (owner, ownvoice.py, first take for both lines; 2 paid generations):

| Line | Text | Direction |
|---|---|---|
| `learner-right` | "Could you turn on the right?" | custom learner style: clear rounded English R, tongue touching nothing |
| `native-light` | "Could you turn on the light?" | `us` preset |

   Acoustic check (Praat formants via parselmouth, 10 ms steps; Whisper medium.en only for rough word times): the learner's word onset (take 2.72–2.80 s) has **F3 ≈ 1800–2000 Hz** rising to ≈ 3300 Hz into the vowel, the low-F3 signature of English /r/. The native "light" onset (0.78–0.84 s) keeps **F3 ≈ 2460–2640 Hz** (no r-dip) with low F1 ≈ 240 Hz and F2 ≈ 1160 Hz, a clear /l/. Silencedetect: learner phrase 0.23–3.18 s, native 0.17–1.29 s.
4. App: native-ios origin/main 3b670ee8. The QA fixture's first daily sentence is already "Please leave the light on." with the flagged word "light" /l/ (`VisualQAData.swift`); the capture-only `light-lesson.patch` changes the sentence to "Could you turn on the light?" (ja 電気をつけてもらえますか？) and replaces the 「QA用データ」 feedback texts with sample wording (written for the capture, not real AI output). Real UI: the lesson screen, `lesson.model` (お手本 = your own voice), `lesson.record`, the score radar, overall feedback and the flagged-word row. Cut at 28.1–29.9 / 33.0–34.0 / 40.5–41.85 s of the 60 fps take, before the offline "could not score" message.
5. Sound: kit Mix, voice first; the bed stops at the scratch and returns with Mimi; soft whooshes for the three turns; a soft tap for the light switch. Integrated loudness −14.1 LUFS.
6. Checks: `hyperframes check` passed (0 errors); contact sheet [process/00-final-frames.jpg](process/00-final-frames.jpg); ffprobe both cuts 1080×1920, 60 fps, no rotation, 19.75 s.

## Uncertain / for review

- Bruno's "turning right" is a squash-and-shift animation of one pose (the sign keeps pointing right) rather than a drawn turnaround.
- Length 19.75 s (the learner take is slow, 3.0 s).
- The learner voice is the owner's (young adult man) on the Friend, as accepted.

## Owner approval

- 2026-10-22: 「6本ともOK。限定公開して」 (episodes 7–12 approved as delivered; the Drive cuts were renamed without `_draft_`: `Disasters11_Light_2026-10-22.mp4`, `Disasters11_Light_EN-subs_2026-10-22.mp4`).
