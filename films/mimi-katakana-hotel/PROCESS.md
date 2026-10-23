# PROCESS

## The owner's words

- 2026-10-23 request: 「動画をさらに生成していく。…まずはここに企画。リストを出して。バズるSNSかつ、必要なら機能紹介とか効果的な学習とか。フックでばずらせる構成ね。チームで議論して構成案・リストを見せて」
- 2026-10-23 approval: 「いいね。これらを作ろう。キャラとか乱発するな。基本今までのキャラメイン。メインはうさぎ二人ね。あとテンポよく。進めて。」

## Steps and decisions

1. Brief from the commander (batch 055–066): Katakana Traps episode 3 (stress), Notion ID 060, built on episode 1's branch and `source/`. The Notion idea had Coco tilting her head; changed to Mimi per the owner's cast rule (Mimi + Friend only). Commander notes from episode 1: -14 LUFS integrated; small Mimi and anything meaningful above the bottom ~400 px.
2. Beats: episode 1's ids kept (hook, slip, explain, model, cta, end); `challenge` and `reveal` added for the viewer quiz. The three words share one chip row and one card so they do not drag: each word's dots light on its own audio, and the learner take is cut into three clips with its pauses removed (0.7 s spacing).
3. Art: none drawn. Plate `lobby`; Mimi `perk` → `tilt` (head tilt with “?”), `point` on the card (bobs on every stressed syllable = the tap), `grin`, `confident`; the Friend `friend-hello`, `friend-oops`, `friend-yay`, `friend-puzzled` (challenge), `friend-amazed` (reveal).
4. Voice: `own-voice.json` → ownvoice.py, 5 lines, 7 paid generations (2 lines regenerated once; the first takes are kept in Drive `KT3_Hotel_assets/own-voice/rejected-take1/`).

| Line | Text | Direction | Takes |
|---|---|---|---|
| `learner-katakana` | “Hoteru. Gitaa. Shanpuu.” | custom style: katakana reading, Tokyo head-high accent (first syllable high, then a fall) | 2 |
| `us-hotel` | “Hotel.” | custom native style: ho-TEL, TEL louder, longer, higher | 2 |
| `us-guitar` | “Guitar.” | gui-TAR | 1 |
| `us-shampoo` | “Shampoo.” | sham-POO | 1 |
| `us-japanese` | “Japanese.” | said alone, ja-pa-NESE | 1 |

   Acoustic check (Praat via parselmouth: intensity, autocorrelation F0, voiced spans; a transcript was not used):
   - Learner take 1 rejected: in “shanpuu” the “puu” went up (F0 ≈ 225 Hz after ≈ 110–130 Hz on “shan”), an end-rising contour, i.e. not head-high. Take 2 (used):
     - ho-te-ru 0.36–0.74 s: ho 117–123 Hz, te 118 → 89 Hz, ru 79 → 69 Hz; three even ~0.10 s syllables, the pitch falls after the first: Japanese HO-te-ru.
     - gi-taa 1.78–2.20 s: gi 91–97 Hz, taa 84 → 63 Hz (long vowel, falling, slightly quieter): GI-taa.
     - shan-puu 3.12–3.70 s: shan 114 → 84 Hz at 80.7 dB, puu 78 → 61 Hz at 74.9 dB (−6 dB): SHAN-puu.
   - us-hotel take 1 rejected: “TEL” longer (0.22 vs 0.12 s) but lower (94 → 86 Hz vs 118 → 103 Hz on “ho”) and 3 dB quieter, so the stress was ambiguous. Take 2 (used): ho 0.30–0.38 s at 84–86 Hz; TEL 0.52–0.74 s at 123 → 109 Hz (+37 Hz), about twice as long, equal intensity: ho-TEL.
   - us-guitar: gui 0.30–0.38 s (short, burst); TAR 0.42–0.70 s, the loudest (84.8 dB) and rising 126 → 155 Hz vs 105 Hz on “gui”: gui-TAR.
   - us-shampoo: sham 0.40–0.60 s at 85 Hz, 79.7 dB; POO 0.66–0.82 s at 104 → 98 Hz, 82.8 dB (+3 dB, +19 Hz): sham-POO.
   - us-japanese: ja 0.36–0.46 s at 88 Hz (loud onset, secondary stress); pa short; NESE 0.58–0.74 s, the F0 peak (rising to 134 Hz) and the longest nucleus: ja-pa-NESE.
   The measured nuclei drive the dots (`LEARNER_BEATS`, `MODEL_BEATS`, `JAPANESE_BEATS` in `source/cues.json`). Needs a human listen.
5. Sound (`scripts/mix.py`, kit Mix): a soft sine tick per syllable (the strong one higher), pops for the chips, a soft four-tick clock on the challenge, theme bed at kit level. Mix.write alone gave about −15.5 LUFS; a gain into a soft limiter (−1.9 dBFS) brings it to −14.3 LUFS integrated, −1.6 dBTP (measured on both rendered cuts). Voice about 15–18 dB over the bed.
6. Checked with `hyperframes check` (contrast fixed, one footnote overflow fixed) and contact sheets ([process/00-draft-frames.jpg](process/00-draft-frames.jpg)): the cast moved up and in so feet and the small Mimi stay above the bottom 400 px; the reveal footnote kept to one small line clear of the characters; EN subtitles wrapped by hand.

7. Commander review (2026-10-23): content approved, keep the `model` beat and the small JApanese FOOD note. The owner on safe zones: 「セーフティエリアって大丈夫？被ってもいいけどすべてが隠れないようにね。」 Fixed for TikTok / Reels / Shorts UI: EN subtitles moved fully above y 1500 and inside x 60–880 (34 px, max two lines); nothing with text, no bubble and no small Mimi in the right rail (x > 900, y 820–1520): the lobby cast, the 「?」, the captions, the card rows / tip / tag, the reveal answer and footnote and the CTA question marks shifted left; the first text line of every top card starts at y ≥ 200; the end card column raised so the App Store badge clears the bottom. Verified on a zone-overlay sheet every ~1.5 s of the EN cut ([process/00-draft-frames.jpg](process/00-draft-frames.jpg): purple top 200 px, orange right rail, red bottom 420 px, green subtitle box). Loudness unchanged (-14.3 LUFS, -1.6 dBTP). The first draft moved to Drive `old/` with a `_v1` suffix.

8. Voice-cut audit (commander, 2026-10-23; the owner heard clipped English in another episode): three heads were cut, the g of “Gitaa”, the sh of “Shanpuu” and the sh of the us “shampoo”. Clip bounds widened (learner clips 0.25–0.84 / 1.53–2.30 / 2.96–3.82 s, us-guitar from 0.24, us-shampoo from 0.245) and placed earlier by the same amount, so every word sounds at the same moment and the dots stay on the measured syllables (beats shifted in `cues.json`). Every voice placement now starts and ends on a 10 ms window at least 38 dB below that clip's peak (heads −38.0 to −50.4 dB, tails −38.4 dB or quieter). Loudness −14.3 LUFS, −1.5 dBTP. The previous draft moved to Drive `old/` with a `_v2` suffix.

## Uncertain / for review

- 16.2 s (the brief said about 17–18 s); kept short for tempo.
- The `model` beat (the Friend saying all three right) was added for a payoff; it reuses the model takes (the owner's voice on the Friend, as in earlier episodes).
- The footnote on JApanese FOOD is small (33 px) by design; drop it if it feels like clutter.
- The Drive folder `060. Katakana Traps 3 - Hotel Guitar Shampoo` did not exist; it was created.

## Owner approval

- 2026-10-23: 「全部OK」 (all twelve shorts of the 055–066 batch approved as delivered; the Drive cuts were renamed without `_draft_`: `KT3_Hotel_2026-10-23.mp4`, `KT3_Hotel_EN-subs_2026-10-23.mp4`).
- Earlier owner notes in the same review round (2026-10-23): 「56の英語音声少し切れている？」 (clipped English in 056; led to the voice-cut audit of every episode); 「62透過されている？」 (the see-through angry pose in 062; fixed there with a filled pose).
