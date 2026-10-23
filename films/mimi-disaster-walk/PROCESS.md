# PROCESS

## The owner's words

- Series request (2026-10-21): 「同じような発音でとんでもない勘違いシリーズ…よくある系でウケる、フック強烈に」. For this batch (episodes 7–12, 2026-10-22): 「同じような発音でとんでもない勘違いシリーズも作って。Shit、sitとか。よくある系でウケる、フック強烈に」 and 「1.それでいこう」.
- Standing rules carried over from episodes 1–6: the owner's own voice for every pronunciation line; medical-style mouth panels (唇（正面） / 舌の位置（横から）); punchline first; Mimi's first person 「僕」; cast = Mimi + Friend, side roles only Bruno / Pippa / Coco (「メインキャラは二人。ミミと友達。…統一感持たせたい」).

## Steps and decisions

1. Idea from the batch plan (commander's brief): Bruno asks “How did you get here?”, the Friend proudly says “I walked!” but it comes out as “I worked!”; Bruno: “On a Sunday?!”; punchline 「それ、「働いてきた」に聞こえてる！」; gag object a briefcase / overtime clock. Set at a Sunday garden BBQ so “On a Sunday?!” makes sense; Bruno plays the host in the apron from episode 3 (library pose `bruno-host-smile`).
2. Source copied from episode 6 (mimi-disaster-peace, itself the pilot's template) with beats and ids kept; times moved to `source/cues.json` (read by `scripts/mix.py`, the same numbers in `hf/index.html`). Added one element, `#q-say` (Bruno's question), because the slip is an answer. Nothing is starred: “work” is not a rude word.
3. Art: one codex-p run drew friend-walked, bruno-host-pity, mimi-briefcase, heard-overtime and the backyard plate from the cast references ([prompts/01-codex-cast-and-plate.txt](prompts/01-codex-cast-and-plate.txt)). Another drew the two mouth panels /ɔː/ (walk) and /ɜːr/ (work) with the series' mouth-r and mouth-aa attached as style references ([prompts/02-codex-mouths.txt](prompts/02-codex-mouths.txt)).
4. Voice: own-voice.json → ownvoice.py. Bruno: Kokoro `am_michael` (`scripts/voices.sh`).

| Line | Text | Direction |
|---|---|---|
| `learner-worked` | “I worked! For two hours!” | custom style (take 3: American r-coloured “er”, slow Japanese-learner timing) |
| `native-walked` | “I walked! For two hours!” | us preset |

Measured with Praat (Burg formants, max 4500/5000 Hz) on the vowel of the key word, not with Whisper:

| Take | Vowel window | F1 | F2 | F3 (median / min) | Verdict |
|---|---|---|---|---|---|
| learner take 1 (learner style, “worked rhymes with jerked”) | 0.66–0.94 s | ≈ 610 | ≈ 1130 | ≈ 2420 / 1900 | weak r, open vowel: discarded |
| learner take 2 (“er as in her, never ah”) | 0.74–1.00 s | ≈ 890 | ≈ 1360 | ≈ 3100 / 2500 | no r dip (an open “wah”): discarded |
| **learner take 3 (kept)** | 0.86–1.12 s | ≈ 580 | ≈ 1180 | **≈ 1880 / 1660** (≈ 1700–1850 through the vowel) | r-coloured /ɝ/: heard as “worked” |
| native “walked” (us) | 0.60–0.92 s | ≈ 640 | ≈ 1040 | **≈ 2830** flat | no r: /ɔ~ɑ/ |

Three learner generations were used (the limit). The film uses only “I worked!” (0.25–1.63 s of take 3) for the slip and “worked” (0.66–1.32 s) on the card; “For two hours!” of the take is slow and not used. Needs a human listen.
5. App: `app-capture/Walkthrough.swift` + `walk-lesson.patch` (capture-only fixture tweak: the first daily sentence becomes “I walked! For two hours!”, the fixture finding points at “walked”, sound /ɔː/). The lesson screen, お手本 button, record button, score card and flagged-word row are the real app (identifiers `lesson.model`, `lesson.record`, `feedback.scores` in native-ios on origin/main); the sentence, feedback wording and score are fixture data.
6. Sound: `scripts/mix.py` (kit Mix), as episode 6: boing on the punchline, tape rewind, the bed stops dead at the record scratch and comes back with Mimi, the native take again when the line is said right.

## Uncertain / for review

- The learner voice is the owner's on the Friend; take 3 is more fluent than earlier learners (the style needed a clear American “er” to make the slip audible).
- The plate (backyard) is a little more painterly than earlier plates.

## Revisions

- v2 (2026-10-22, commander review): "in the freeze beat the Friend is rendered cream/yellow instead of white — off-model". Cause: the freeze tint inherited from episode 6 (a yellow `#ffd84a` multiply layer over the whole scene). Replaced with episode 5's desaturating tint (`#9aa6b2`, saturation blend), so the white cast stays white; whole film re-scanned at 2 fps. Previous drafts kept in Drive `old/` as `*_v1-cream-friend.mp4`.

## Owner approval

- 2026-10-22: 「6本ともOK。限定公開して」 (episodes 7–12 approved as delivered; the Drive cuts were renamed without `_draft_`: `Disasters8_Walk_2026-10-22.mp4`, `Disasters8_Walk_EN-subs_2026-10-22.mp4`).
