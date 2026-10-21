# Pronunciation Disasters 1 — Sit / Sh*t

**English** · [日本語](README.ja.md)

Pilot of the series "Pronunciation Disasters" (one sound apart, a huge misunderstanding). It opens on the punchline: frame 1 is Mimi screaming 「それ、Sh★tに聞こえてる！」 over the frozen guest, with a cute poop, then a rewind (◀◀) to how it happened. In a hotel lobby Mimi's friend kindly offers a seat to a foreign guest (a bear) and says "Please sh*t down." Record scratch, the guest freezes in ice, 「シーン…」. Mimi pops up horrified: 「それ「sh★t」（うんこ）に聞こえてる〜！！」. One card: **sit** vs **sh★t**, each with two illustrated panels (唇（正面）: lips spread vs rounded and pushed; 舌の位置（横から）: a head cross-section, tongue tip right behind the upper teeth vs the tongue rising further back), with both takes in the owner's voice. Then the real Lanclo daily lesson on "Please sit down." (score, then the sound to fix in "sit"), the friend says it right, the guest sits, end card + CTA tap.

0:18.7 / 1080×1920, 60 fps / two cuts: Japanese only and English subtitles / 2D official Mimi style (poses and the lobby by Codex) + HyperFrames / voice: the owner's registered Lanclo voice (Gemini `gemini-3.8-flash-tts`, `kits/mimi-short/scripts/ownvoice.py`)

The word is audible (it is the joke) and censored on screen with a star: "sh★t".

![Final frames](process/00-final-frames.jpg)

Rebuild: [source/README.md](source/README.md). Process: [PROCESS.md](PROCESS.md). Prompt: [PROMPT.md](PROMPT.md). Credits: [CREDITS.md](CREDITS.md). Drafts in Lanclo's Google Drive `002.SNS/037. Pronunciation Disasters 1 - Sit or Sht/` (`Disasters1_Sit_draft_2026-10-21.mp4`, `Disasters1_Sit_draft_EN-subs_2026-10-21.mp4`, raw material in `Disasters1_Sit_assets/`).

## Series template (episodes 2–6)

Copy `source/` to `films/mimi-disaster-<word>/source/` and keep `hf/index.html`'s beats and ids; swap only the PAIR. The story keeps its own clock through `T()` in `scripts/mix.py` (and the same shifted numbers in `hf/index.html`): the flash-forward takes 0–1.5, then the story runs from 1.5.

| Beat (film time) | What to swap |
|---|---|
| **Punchline-first hook** 0–1.5 (`#ff`: frozen scene, `#ff-hook`, `#ff-mimi`, `#ff-poop`, rewind `#rew` at 1.2) | Mimi's punchline as the first line, censored with ★ (「それ、Sh★tに聞こえてる！」), and the episode's **object gag** (here a cute poop = the meaning of the wrong word; e.g. lice → a cute louse, b*tch → a cute dog). No voice; SFX: freeze, boing, pop, reversed whoosh |
| Setup 1.5–4.25 (`#hook`) | The situation line (place + the phrase + 「空気が凍った。」) |
| Slip 2.0–4.25 (`#say`, `#star`) | The phrase with the word censored, timed to the learner take's word start |
| Freeze 4.25–5.75 (scratch, `#tint`, `#frost`, ice, 「シーン…」) | The plate (`#plate`) and the cast (`#friend`, `#guest` / `#guest-ice`) |
| Mimi 5.75–7.0 (`mimi-scream`, `#yell`, `#yell-poop`) | 「それ「…」（意味）に聞こえてる〜！！」 + the object gag |
| Card 7.0–11.7 (`#col-ok` / `#col-ng`, `.panel`s, `#card-poop`) | The two words, four panel images, the tips, the two takes (learner → native) |
| App 11.7–15.8 (`#device`, `scripts/app_track.sh`) | `app-capture/*.patch` sentence + feedback target/sound, cut times |
| Fix 15.8–17.4 (`#ok-say`, `#cap-ok`) | The phrase said right and the happy ending |
| End 17.4–18.7 | unchanged |

**Card panels** (see [process/01-mouth-card.jpg](process/01-mouth-card.jpg)): per word two panels with a navy header (`.panel .ph`: 唇（正面） / 舌の位置（横から）) over an image in a soft, semi-realistic medical-education style: a front view of the lower face (nose, lips, chin) and a side cross-section of the head facing left (nose, lips, teeth, palate, pink/red tongue with a dashed surface line), pale cream background, coloured arrows (teal for the right sound, coral for the wrong one), no text in the images. Generate them with codex-p from [prompts/02-codex-mouth-panels-and-poop.txt](prompts/02-codex-mouth-panels-and-poop.txt) (a web image was attached as a style reference only; the drawings are original), resize to 900 px WebP. Shapes per sound: **ee** = lips spread wide, teeth showing, tongue high and front; **i** (short) = relaxed, slightly open, tongue a little lower; **r** = lips slightly rounded, tongue pulled back and bunched, tip not touching; **l** = slightly open, tongue tip up on the ridge behind the upper teeth; **oʊ** = lips rounded, closing toward "oo"; **ɑ** = wide open, jaw dropped, tongue low and back; **s** = spread, tongue tip right behind the upper teeth (narrow groove); **sh** = rounded and pushed forward, the tongue blade raised further back.

Voices: `own-voice.json` with a `learner` custom style that clearly says the wrong word and `us` for the model; measure word starts (silencedetect / spectral check) and move `LINE`, the star and the marks. Mimi's first person in Japanese text is 「僕」.
