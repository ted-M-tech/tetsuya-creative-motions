# Pronunciation Disasters 1 — Sit / Sh*t

**English** · [日本語](README.ja.md)

Pilot of the series "Pronunciation Disasters" (one sound apart, a huge misunderstanding). In a hotel lobby Mimi's friend kindly offers a seat to a foreign guest (a bear) and says "Please sh*t down." Record scratch, the guest freezes in ice, 「シーン…」. Mimi pops up horrified: 「それ「sh★t」（うんこ）に聞こえてる〜！！」. One card: **sit** = lips spread, tongue tip (ネイティブ発音) vs **sh★t** = lips rounded and pushed (さっきの発音), with both takes in the owner's voice. Then the real Lanclo daily lesson on "Please sit down." (score, then the sound to fix in "sit"), the friend says it right, the guest sits, end card + CTA tap.

0:18 / 1080×1920, 60 fps / two cuts: Japanese only and English subtitles / 2D official Mimi style (poses and the lobby by Codex) + HyperFrames / voice: the owner's registered Lanclo voice (Gemini `gemini-3.8-flash-tts`, `kits/mimi-short/scripts/ownvoice.py`)

The word is audible (it is the joke) and censored on screen with a star: "sh★t".

![Final frames](process/00-final-frames.jpg)

Rebuild: [source/README.md](source/README.md). Process: [PROCESS.md](PROCESS.md). Prompt: [PROMPT.md](PROMPT.md). Credits: [CREDITS.md](CREDITS.md). Drafts in Lanclo's Google Drive `002.SNS/037. Pronunciation Disasters 1 - Sit or Sht/` (`Disasters1_Sit_draft_2026-10-21.mp4`, `Disasters1_Sit_draft_EN-subs_2026-10-21.mp4`, raw material in `Disasters1_Sit_assets/`).

## Series template (episodes 2–6)

Copy `source/` to `films/mimi-disaster-<word>/source/` and keep `hf/index.html`'s beats and ids; swap only the PAIR:

| Beat (time) | What to swap |
|---|---|
| Hook 0–2.75 (`#hook`, on screen from frame 1) | The hook line (place + the phrase + 「空気が凍った。」-style punch) |
| Slip 0.5–2.75 (`#say`, `#star` censor) | The phrase with the word censored, timed to the learner take's word start |
| Freeze 2.75–4.25 (scratch, `#tint`, `#frost`, ice, 「シーン…」) | The plate (`#plate`) and the cast poses (`#friend`, `#guest` / `#guest-ice`) |
| Mimi 4.25–6.3 (`mimi-scream`, `#yell`) | 「それ「…」（意味）に聞こえてる〜！！」 |
| Card 6.3–11.0 (`#col-ok` / `#col-ng`, mouth SVGs, bars) | The two words, the mouth tip for each, the two takes (learner → native) |
| App 11.0–15.1 (`#device`, `scripts/app_track.sh`) | `app-capture/*.patch` sentence + feedback target/sound, cut times |
| Fix 15.1–16.7 (`#ok-say`, `#cap-ok`) | The phrase said right and the happy ending |
| End 16.7–18.0 | unchanged |

Mouth icons (`svg.mouth`, 340×210, inline in `#col-ok` / `#col-ng`; see [process/01-mouth-card.jpg](process/01-mouth-card.jpg)): front view of lips in the card's flat style — navy outline, upper lip `#e5707f` with a cupid's bow, lower lip `#f08b99` with a white shine, opening `#6b2335`, white teeth, pink tongue — plus a cue in the column colour (outward arrows = spread, inward arrows = rounded) and, when the lips move forward or the tongue matters, a small side-profile inset (circle, bottom right). One shape per sound: **ee** = spread wide, teeth showing (like `sit`'s s); **i** (short) = relaxed, slightly open, no arrows; **r** = rounded lips + profile inset with the tongue pulled back (not touching); **l** = slightly open + profile inset with the tongue tip up behind the upper teeth; **oʊ** = rounded (like `sh`) with the opening closing toward an "oo"; **ɑ** = wide open, jaw dropped, tongue low; **sh** = pouted, small round opening, inward arrows + profile with lips pushed forward.

Voices: `own-voice.json` with a `learner` custom style that clearly says the wrong word and `us` for the model; measure word starts (silencedetect / spectral check) and move `LINE`, the star and the bars. Mimi's first person in Japanese text is 「僕」.
