# PROCESS

## The owner's words

- Series request: 「同じような発音でとんでもない勘違いシリーズも作って。Shit、sitとか。よくある系でウケる、フック強烈に」; for this batch (episodes 7–12): 「1.それでいこう」.
- Standing rules carried from earlier episodes (see films/mimi-disaster-peace/PROCESS.md): own voice for every pronunciation line, medical-style mouth panels, punchline-first hook, Mimi's first person 「僕」, main cast Mimi + Friend with the recurring side cast only (「メインキャラは二人。ミミと友達。…統一感持たせたい」).

## Steps and decisions

1. Brief from the commander (batch 7–12): Coco shows off a new sun hat; the Friend's “I love your hat!” lands as “I love your hut!” (小屋); a hut pops onto Coco's head; punchline 「それ、「小屋」に聞こえてる！」. Started from episode 6 (`films/mimi-disaster-peace/source/`), same beats and ids, retimed (18.8 s).
2. Art: one codex-p run drew Coco showing off the hat, Coco with the cabin on her head, and the kawaii cabin icon ([prompts/01-codex-cast-and-heard.txt](prompts/01-codex-cast-and-heard.txt)). One run drew the /æ/ and /ʌ/ mouth illustrations with the series' earlier mouth illustrations (aa, ee) attached as the style reference ([prompts/02-codex-mouths.txt](prompts/02-codex-mouths.txt)). The Friend and Mimi poses and the street plate come from the library. No new characters.
3. Voice: `own-voice.json` → ownvoice.py (owner's registered voice).

| Line | Text | Direction | Takes |
|---|---|---|---|
| `learner-hut` | “I love your hut!” | custom learner style (“hut” rhymes with “but”, a short relaxed Japanese-like “a”) | 1 |
| `native-hat` | “I love your hat!” | take 1 `us` preset; take 2 custom native style asking for a bright /æ/ as in “cat” | 2 (kept take 2) |

   Measured with Praat formants (median over the vowel), compared with Kokoro `am_michael` saying “hat” and “hut” as a reference pair:

| | F1 | F2 | F2−F1 |
|---|---|---|---|
| learner “hut” (kept) | 894 | 1467 | 573 |
| native “hat” take 1 (`us`) | 882 | 1633 | 751 (between the two references, discarded) |
| native “hat” take 2 (kept) | 954 | 1802 | 847 |
| reference “hat” (Kokoro) | 664 | 1689 | 1025 |
| reference “hut” (Kokoro) | 619 | 1103 | 484 |

   The learner vowel is open and central (Japanese ア-like), nearest the /ʌ/ reference; the kept native vowel has F2 about 335 Hz higher (fronter, /æ/-like). Whisper (timestamps only) wrote “heart” for the learner take, i.e. not “hat”. Take 2 of the native line starts with an unasked “Oh,” (0–0.68 s); the mix plays it from 0.80 s so only “I love your hat!” is heard. Needs a human listen.
4. Card: 「ア」と「エ」の間で！ — hat: 口を横に大きく 「ア」と「エ」の間; hut: 短くゆるい「ア」だと hut（小屋）; learner word at 8.5 s, native word at 9.6 s.
5. App: `app-capture/Walkthrough.swift` + `hat-lesson.patch` (capture-only fixture tweak: the first daily sentence becomes “I love your hat!” and the fixture finding points at “hat” /æ/). The lesson screen, お手本 button, score card and flagged-word row are the real app (`lesson.model`, `lesson.record`, `feedback.scores` in native-ios origin/main); the sentence, the feedback wording and the score are fixture data. Cut with `scripts/app_track.sh`.
6. Sound: `scripts/mix.py` (kit Mix): boing, rewind, record scratch, freeze, a soft poof when the cabin lands, Coco (Kokoro `af_bella`) “My… hut?!”; the freeze uses 041’s desaturate layer (#9aa6b2, saturation blend; 042’s yellow multiply was that episode’s joke only); the bed stops at the freeze and returns with Mimi; voice loudest, BGM ~21 dB under.
7. Checked with `hyperframes check` and a contact sheet of the key moments ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)): captions top, bottom 400 px clear apart from the subtitle.

## Uncertain / for review

- The learner voice is the owner's (a young adult man) on the Friend.
- The flagged-word feedback text in the app shot is written for the capture; the UI is real.
