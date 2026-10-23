# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- Standing cast rule (kits/mimi-short/cast/README.md): 「なんでちょこちょこ新しいキャラ出てるの？メインキャラは二人。ミミと友達。そこメインで回して。…」

## Steps and decisions

1. Brief from the batch commander ([prompts/00-commander-brief.txt](prompts/00-commander-brief.txt)) and the Notion row 062 (team review; its first script had Coco bristling and storming off). Per the owner's cast direction the offended one is Mimi, not Coco. Branched from origin/main; episode 1's tracked `source/` (films/mimi-hear-can, branch feat/mimi-hear-can) copied in, beat ids kept (hook, play, reveal, rule, ask, end), the three-card layout from its “Series template” (cards 320 px at left 40 / 380 / 720, the countdown moved under the cards, one rule row per intonation with an arrow instead of `.syl` bars).
2. Cast: Mimi + Friend only, all library poses. Mimi: `angry` (bristling, hook) → `confident` (listening) → `angry` (reveal) → `flat` hopping and sliding away with 「ぷいっ！」 → `point` on the rule card → `jump`. Friend: `dreamy` → `tease` 「Bでしょ！」 → `shock` 「えっ、Bじゃないの！？」 → `yay`. The turn-away is a hop, tilt and slide (not a mirrored pose: mirroring would put the L on the wrong cup). No codex-p run, no new art.
3. Quiz order: A falling, B rising, C sharp rise on ME (the answer). The intonation arrows are on the cards from frame 1 (as in the Notion script); each arrow draws along while its take plays. The Friend picks B: the plain question rise sounds “pushy” to him.
4. Voice: `own-voice.json` → ownvoice.py, 3 lines + 3 regenerations of A = 6 paid generations (B and C: first take). Direction verbatim in own-voice.json. Acoustic check with Praat (`source/scripts/check_voice.py`; 20 ms frames, F0 and intensity, voiced runs split by the unvoiced k / s):

| Take | “ex” | “cuse” | “me” | Reading |
|---|---|---|---|---|
| A take 1 | 87 Hz | 81 Hz | 119 → 171 Hz (rise) | rejected: rises |
| A take 2 | — | 85 → 83 Hz | 83 → 81 Hz, creaky | rejected: flat and creaky, no audible fall |
| A take 3 | — | 128 Hz, flat | 117 → 136 Hz (slight end rise) | rejected: level / slight rise |
| **A take 4 (used)** `us-a-fall` | 123 Hz | 100 → 94 Hz (peak 79 dB) | 91 → 85 → 89 Hz, quieter (75 dB) | falling: ~6 semitones from “ex”, ~2.5 from “cuse” to “me”; no end rise |
| **B** `us-b-rise` | 88 Hz | 84 → 88 Hz (79 dB) | 143 → 284 Hz in 0.14 s (80 dB) | a clear question rise (~12 semitones) on a short “me” |
| **C** `us-c-offended` | 149 Hz | 92 → 225 Hz (83 dB, already rising) | 255 → 392 Hz over 0.28 s (83 dB) | sharp rise: “me” twice as long as B's, ~5 semitones higher at its top (392 vs 284 Hz), as loud as “cuse”: stress on ME |

   A's fall is gentle (the owner's voice sits low, ~85 Hz, and the model kept pulling “me” up); take 4 is the first with a monotonic fall and no end rise, so it is used; regenerations stopped at the limit (3). C is clearly distinct from B (longer, higher, louder “me”, the whole phrase climbing). Whisper not used. Rejected A takes 2 and 3 are in Drive `Hear2_ExcuseMe_assets/own-voice/rejected/` (take 1 was overwritten by the regeneration).
5. Mix: takes trimmed to speech with heads and tails kept (silencedetect -45 dB: A 0.12–1.12 s, B 0.19–0.94 s, C 0.15–1.57 s of the take); kit bed and levels unchanged; soft taps for the countdown, pofu for the reveal, a whoosh for Mimi's turn-away; the rule punch line comes after C's “me” so no pop lands on it. Episode 1's -14 LUFS post-gain + limiter step kept: -14.2 LUFS / -1.9 dBTP in the WAV, -14.3 LUFS / -1.9 dBTP in both cuts. Voice sections measure 9–14 dB (mean) above the bed-only sections.
6. Layout check on the contact sheet: captions at the top, subtitles at `bottom: 410px` over the feet only, never a face; the rule subtitle cut to two lines. `hyperframes check`: 0 errors (lint warnings for missing ids on subtitle clips, as in episode 1).

## Draft v2 (2026-10-23, platform safe zones)

- Owner: 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」 Commander: the bristling / ぷいっ Mimi and the small Mimi on the rule card sat in the right action rail (x > 900, y 820–1520); EN subtitles must sit fully above y 1500 within x 60–880; the hook's first line must start at y ≥ 200.
- Layout: hook, question, answer, rule title and the comment card start at y ≥ 200 (hook 96 / 100 px); cards moved to y 445 and 370 px high; Mimi moved to x 600 (face left of 900), her turn-away is a hop and tilt without sliding right; the 「ぷいっ！」 and 「Bでしょ！」 bubbles moved out of the rail; the rule-card arrows end at x 890; the rule Mimi (200 px, x 690) sits next to a narrower punch line; subtitles at `bottom: 430px` (box bottom y 1490), x 60–880.
- Checked on a zone-overlay sheet (EN cut, frames every ~1.5 s, the three zones drawn): no text, bubble or small Mimi in the rail; faces left of x 900; nothing meaningful below y 1500 except the kit end card's App Store badge (kit level, unchanged). Loudness unchanged: -14.3 LUFS / -1.9 dBTP in both cuts.
- v1 drafts moved to Drive `old/` with a `_v1` suffix.

## Draft v3 (2026-10-23, see-through angry Mimi)

- Owner: 「62透過されている？」 The library pose `angry.webp` had lost its white body fill in an old cutout, so the background showed through Mimi in the hook and the reveal. The commander made a filled copy (same size; enclosed body, face and ears filled white, outline untouched), kept in this episode as `source/art/pose-angry-filled.webp` and staged by `scripts/art.sh`; both angry shots use it. The shared kit library is unchanged.
- Every other pose in the film (`flat`, `confident`, `point`, `jump`, `friend-dreamy`, `friend-tease`, `friend-shock`, `friend-yay`) checked on a dark background: all fills are opaque.
- Loudness unchanged (-14.3 LUFS / -1.9 dBTP). v2 drafts moved to Drive `old/` with a `_v2` suffix.

## Open questions

- Owner's ear on A: the fall is real but gentle (~2.5 semitones from “cuse” to “me”); it no longer rises, but it is less dramatic than B and C. Regeneration limit reached.
- Length 17.8 s (brief ~17 s).

## Owner approval

- 2026-10-23: 「全部OK」 (all twelve shorts of the 055–066 batch approved as delivered; the Drive cuts were renamed without `_draft_`: `Hear2_ExcuseMe_2026-10-23.mp4`, `Hear2_ExcuseMe_EN-subs_2026-10-23.mp4`).
- Earlier owner notes in the same review round (2026-10-23): 「56の英語音声少し切れている？」 (clipped English in 056; led to the voice-cut audit of every episode).
