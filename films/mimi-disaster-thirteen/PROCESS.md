# PROCESS

## The owner's words

- Batch request, 2026-10-23: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- Approval, 2026-10-23: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- Standing series rules (films/mimi-disaster-sit, films/mimi-disaster-hat): own voice for every pronunciation line, punchline-first hook, Mimi's first person 「僕」, main cast Mimi + Friend.

## Steps and decisions

1. Brief from the commander (batch 055–066): the Friend orders “Thirteen tickets, please” with flat stress; the clerk hears thirty and 30 tickets bury the Friend; punchline 「13枚頼んだら30枚来た」. Cast change: the clerk is **Mimi in a ticket-booth role outfit** (no Bruno, no side cast). The mouth card becomes a **stress card** (the series' first stress episode). Started from episode 12 (`films/mimi-disaster-hat/source/`), same beats and ids, retimed and tightened to 17.9 s.
2. Art: one codex-p run with the cast references (Mimi master/success, Friend sheet/aww) drew Mimi as the clerk (two poses), the Friend buried in tickets, a ticket prop and the booth plate ([prompts/01-codex-cast-and-plate.txt](prompts/01-codex-cast-and-plate.txt)). The counter front is cropped from the plate and layered over Mimi so she stands behind the counter. Library poses: `friend-order`, `friend-shock`, `friend-yay`, `scream` (Mimi out of role; she is on the right so she never has to be mirrored), `jump`, `confident`. No new characters.
3. Mimi as herself at 5.6 s: the clerk Mimi leaves the window when Mimi (no outfit) pops up, so only one Mimi is on screen at a time.
4. Stress card (HTML/SVG, no image generation): per number the syllables sized by stress (thir **TEEN** / **THIR** ty), stress dots (small/big), and a navy-headed panel 「音の高さ」 with a pitch line (rise on TEEN / high on THIR then down); tips 「後ろのティーンを強く・長く」 / 「平ら・前寄りだと thirty（30）に」. Same column/panel/mark style as the mouth cards.
5. Voice: `own-voice.json` → ownvoice.py (owner's registered voice), 2 lines, 3 takes each (the limit). Measured with Praat (intensity, F0, F3 for the r-coloured “thir”) per syllable; Whisper used for rough word timestamps only.

| Take | “thir” | “teen” / “tin” | Verdict |
|---|---|---|---|
| learner 1 (“Thirteen…”, stress on THIR asked) | 0.30 s, 79 dB, F0 115→143 | 0.42 s, 83 dB, F0 peak 157 | TEEN prominent (native-like): rejected |
| learner 2 (same text, stronger style) | 0.24 s, 82 dB, F0 140 | 0.34 s, 85 dB, F0 196 | TEEN prominent: rejected |
| **learner 3** (text spelled “Thirtin tickets, please.”) | 0.20 s, 78 dB, F0 116–122 | 0.38 s incl. the n, 77 dB, F0 120–125 | **kept**: flat pitch (<0.5 semitone apart), equal loudness, no r-colouring on “thir” (F3 ≈ 2.8 kHz: katakana サー) — the flat, katakana stress of the brief |
| **native 1** (us, stress on TEEN) | 0.16 s voiced, 80–83 dB, F0 116–118 flat | voiced ~0.14 s + n, 81 dB, F0 jumps to 137 then falls | **kept**: pitch accent on TEEN (+2.8 semitones), “thir” r-coloured (F3 dips to ~1.9 kHz) |
| native 2 (longer “ee” asked) | 0.12 s, F0 113 | 0.24 s, 77 dB, F0 104→90 (lower) | duration on TEEN but pitch falls from THIR: ambiguous, rejected |
| native 3 (contrastive TEEN asked) | 85.7 dB, F0 130 (loudest, highest) | 80 dB, F0 101→77 | prominence on THIR: rejected |

   The learner text in `own-voice.json` is the deliberate spelling “Thirtin” (the way the Friend says it); on screen it reads “Thirteen”. All six takes are in Drive `Disasters13_Thirteen_assets/own-voice/takes/`. **Needs a human listen**: whether the flat learner take reads as “thirty” to the ear.
6. App: `app-capture/Walkthrough.swift` + `thirteen-lesson.patch` (capture-only fixture tweak: the first daily sentence becomes “Thirteen tickets, please.” (ja 「チケットを13枚ください。」) and the fixture finding points at “Thirteen” with category `stress` / kind `word-stress`, no sound label). Checked on native-voice-clone origin/main: `lesson.model`, `lesson.record` (Views/PracticeScreen.swift), `feedback.scores` (Views/AccountProgress.swift), the issue categories include `stress` (Core/LancloAPI.swift, Core/ProgressSummary.swift). The sentence, the feedback wording and the score are fixture data. Cut with `scripts/app_track.sh`.
7. Sound: `scripts/mix.py` (kit Mix, cue sheet `cues.json`): paper rustle (code-made) for the avalanche, boing, rewind, record scratch, freeze, soft pops; the bed stops at the freeze and returns with Mimi; voice loudest, BGM ~21 dB under; -14 LUFS.
   The take (app 5f5571ad, 84 s, resampled to 60 fps) is cut to 4.1 s: the sentence and score with お手本 pressed (28.1–30.1), the record button pressed (33.1–33.9) and the flagged-word row, where the app shows “Thirteen /θɜrˈtiːn/” with the fixture tip 「thir-TEEN：前は軽く、後ろの「ティーン」を強く長く。」 (40.7–42.0). No fixture labels (「QA用データ」「デモデータ」) appear in the used segments; no counts are shown.
8. Checks: `hyperframes check` (0 errors), both cuts ffprobed (1080×1920, 60 fps, no rotation, 17.9 s), a contact sheet of the key moments ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)): captions at the top, the bottom 400 px holds only the subtitle, the ticket pile and feet; bubbles moved off Mimi's face (the order bubble sits over the counter). Only Mimi and the Friend on screen. Mix: -14 LUFS, true peak -1.5 dBFS, voice sections about 2–4 dB above the SFX-only freeze; the paper rustle lowered after a first listen of the levels.

## Uncertain / for review

- Whether the flat learner take is heard as “thirty” (measured flat, but the joke depends on the ear). The learner text was spelled “Thirtin” to get it; 3 of 3 generations used for each line.
- The native “thirteen” has its stress as a pitch jump on TEEN; the “ee” is not much longer than “thir” (the take that made it longer lost the pitch accent).
- Mimi the clerk's “Thirty tickets!” is a bubble without voice (no side cast, no Japanese TTS).
- The flagged-word feedback text in the app shot is written for the capture; the UI and the IPA line are the real app.
