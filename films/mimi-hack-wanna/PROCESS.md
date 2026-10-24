# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」
- 2026-10-23 (safe zones, batch rule): 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」
- 2026-10-23 (series look, batch rule): 「フォントの色とか変わってる？統一感出して過去と」

## Steps and decisions

1. Brief from the commander: Pronunciation Hacks episode 3, Notion ID 074, tip “want to → wanna, going to → gonna” in casual speech, with a small note that it is not for formal writing. Branch from `feat/mimi-hack-check-it-out` (episode 1, not merged yet); `source/` copied, beat ids kept (hook, slip, tip, model, fix, cta, end).
2. Story 16.9 s: hook 「ネイティブ、toを言ってない？」 with the fast line under it; the same line again in `slip`, the Friend's bubble shows the reduced words as red 「？？？」; slow-down card with two rows (slow form, the to struck through as it melts → casual form with na in blue); back in the cafe Mimi says it once more with the words readable, the Friend answers “I'm gonna try!”, high five; CTA; end card. The fast line is heard three times on purpose (listening game: can't catch → learn → catch). Plate `cafe` (casual talk) instead of episode 1's meeting room.
3. Art: library only (Mimi `talk`, `grin`, `point`, `presenter`, `highfive`; Friend `friend-amazed`, `friend-oops`, `friend-yay`, `friend-hello`), all checked on a dark background. Rejected: `friend-confused` and `friend-proud` (rice bowl), `friend-puzzled` (camera), `friend-sigh` (see-through fill).
4. Voice: `own-voice.json` → ownvoice.py, 6 lines, 1 take each, no regenerations.

| Line | Text | Direction | Takes |
|---|---|---|---|
| `us-fast` | “I wanna go. I'm gonna try.” | casual native, fast, fully reduced wanna / gonna | 1 |
| `us-want-to` | “Want to.” | slow, two separate words, clear t and “to” | 1 |
| `us-wanna` | “Wanna.” | isolated word, natural, no t | 1 |
| `us-going-to` | “Going to.” | slow, two separate words | 1 |
| `us-gonna` | “Gonna.” | isolated word, natural, no t | 1 |
| `us-im-gonna-try` | “I'm gonna try!” | the Friend's line, cheerful, reduced gonna | 1 |

   Acoustic check (20 ms RMS envelope and the >3.5 kHz band, ffmpeg silencedetect −40 / −30 dB, spectrogram: [process/01-takes-waveform.jpg](process/01-takes-waveform.jpg)); Whisper only for rough timing (it wrote “want to” for the fast take's wanna, as expected, so it was not used to judge the sound):
   - Slow “Want to.”: “want” 0.35–0.84, a stop closure 0.84–0.92 and a t burst 0.92–1.02 (high band at the full level: a released t), 0.30 s of silence, then “to” 1.37–1.79 starting with an aspirated t burst. Slow “Going to.”: “going” 0.23–1.18, 0.23 s silence, “to” 1.38–1.88.
   - “Wanna.” 0.32–0.62 and “Gonna.” 0.26–0.54: one continuous voiced stretch, no closure (no dip below −22 dB inside), the high band stays 13 dB or more under the voice: no t.
   - Fast take: “I wanna go” 0.32–0.94 with no silence inside and no burst (dips only to −22 dB at the g of “go”); 0.43 s breath; “I'm gonna try” 1.40–1.92: the only closure + burst is at 1.62–1.66 (the t of “try”). “I'm gonna try!”: the only burst is the tr of “try” at 0.76–0.84.
   - Cuts: every take is placed at measured silence (`TAKES` in `cues.json`, ≥ 40 ms pre-roll); `scripts/mix.py` asserts the first and last 10 ms of each placement are ≤ −38 dB vs the clip peak (measured −48 to −59 dB). Needs a human listen.
5. Sound (`scripts/mix.py`, kit Mix): whooshes on scene changes, a soft tap under 「聞き取れない…」, a low pop before each casual form, ding + pops on the high five, pochi on the CTA tap. Voice windows ≈ −14…−17 dB RMS, bed alone ≈ −32 dB. Loudness: the first pass already measured −14.3 LUFS but −1.5 dBTP in the WAV (−1.3 in the AAC cuts), so the post-gain + limiter step now also runs until the WAV is ≤ −2.2 dBTP; both cuts −14.2 LUFS, −2.2 dBTP.
6. Edit: words of the fast line light on their measured starts; the 「？？？」 wobble; on the card the to's strike is drawn just before the casual form pops in with na in blue. Mimi's bubbles (the fast line) sit on the right with the tail toward her; the Friend's bubble on the left. `hyperframes check` passes (layout 0 issues, contrast 33/33; the warnings are the template's nested-structure notes).
7. Series look: diffed against episode 1. Same colours (red #e5484d = the to that goes away / the unheard words, blue #2a8dff = the na and the caught words / active row, yellow #ffd84a in the note, #5b7f9f for muted text), same font, weights and sizes (hook 124/100, title 74, rows 150, note 56, bubbles 92, reaction 80, CTA 104/64). One addition: the slow form in each row at 96 px (#5b7f9f, a new line above the 150 px casual form); the rows are left-aligned and 10 px taller (340) to hold the two lines.
8. Safe zones (EN cut, overlay [process/02-safe-zones.jpg](process/02-safe-zones.jpg), frames every ~0.9 s): top text starts at y ≥ 200; EN subtitles x 60–880, box bottom y 1490; the right rail (x > 900, y 820–1520) holds no text or bubble (the card rows' backgrounds reach into it as in episode 1, their text does not); faces left of x 900. The kit end card's App Store badge stays in the bottom zone (kit layout, as in every episode).

## Uncertain / for review

- Fast line played three times (hook, slip, fix): intended as the listening game; if it feels repetitive, the hook could go silent.
- The owner's (adult male) voice on both Mimi's lines and the Friend's line, as in earlier episodes.
- Drive folder `074. Pronunciation Hacks 3 - Wanna and Gonna` did not exist; created with the name from the brief.
