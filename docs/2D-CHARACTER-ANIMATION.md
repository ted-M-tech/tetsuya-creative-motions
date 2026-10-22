# 2D character animation

**English** · [日本語](2D-CHARACTER-ANIMATION.ja.md)

How to make vertical 2D character shorts in a character's own art style, as done for the Mimi (Lanclo) series: the films in `films/mimi-*/`, each with `PROCESS.md` (making-of, Japanese), `PROMPT.md` and `source/README.md` (rebuild steps). The first one, 「自分の声、むり」, is [films/mimi-jibun-no-koe](../films/mimi-jibun-no-koe/PROCESS.md). The shared parts are the [Mimi shorts kit](../kits/mimi-short/README.md). For 3D see the [3D character workflow](3D-CHARACTER-WORKFLOW.md).

## 2D or 3D

2D for expression, the exact brand art, fast series production and in-app reuse (Rive); 3D for turns, camera moves and spatial scenes. For Mimi the owner compared the same three poses in 3D, 3D toon and 2D and chose 2D. Duolingo also ships its in-app characters as 2D Rive.

## Two motion routes

| | Rive bones (early films) | Pose swap + GSAP (current default) |
|---|---|---|
| How | Each pose rigged with a mesh and bones, acted with keys, rendered to frames, then placed in HyperFrames | Cut-out poses (WebP) placed in the HyperFrames edit; acting is swapping poses on the beat plus GSAP squash, hop, shake, slide and pop |
| Films | jibun-no-koe, think-sink, michi, nikki, shashin, daily, action-add (swipe: one Rive shot) | roleplay, debate, voice, tuning, frozen-abroad, quitter, watching, the Pronunciation Disasters and most others |
| Use when | A shot needs continuous body acting or lip-sync on the character | Fast series work, retiming without re-rendering, several characters on screen |

Start with pose swap; add a Rive shot only where a held pose looks dead.

## Tools

Codex (`codex-p exec --image ... - < prompt.txt`) for art and reviews, HyperFrames for the edit (one GSAP timeline, `npx hyperframes check`, render, and Kokoro TTS through `npx hyperframes tts`), ffmpeg / ImageMagick / Python (`uv`) for cut-outs, encoding and sound, the Xcode simulator for app takes. Rive route only: Rive CLI (`brew install --cask rive-app/tap/rive-cli`, `rive update`; look up `rive docs` / `rive schema`, the format is newer than model training).

## Steps

1. **Story and hook** as a timed beat table (see Story shapes). Check every product claim against the app's code first; show only what exists.
2. **Poses**: reuse the library's and earlier episodes' poses first. New ones: codex-p with the cast references attached every time (template in [cast/README.md](../kits/mimi-short/cast/README.md)): same line, colours, proportions, accessory side, three-quarter direction, scale, white background, no text.
3. **Cut out** with `kits/mimi-short/scripts/cutout.sh` (flood-fill white from the corners → trimmed transparent WebP). Plates are resized to 1080×1920; a counter front can be cropped from the plate and layered in front of a character.
4. **Scale** by head size, not drawing height; plant the feet on the same spot (kit plates put the feet point at (480, 1330)).
5. **Voices and the app take** (sections below).
6. **Sound**: `scripts/mix.py` builds a `sfx.Mix` from the cue sheet; its times are shared with `hf/index.html`.
7. **Edit** in HyperFrames: `kits/mimi-short/stage.sh <hf>` copies the kit look (`hf/kit.css`, `hf/kit.js`), brand and fonts; poses, captions, bubbles, the phone, cards and the end card are timed on one GSAP timeline.
8. **Check and render**: `npx hyperframes check`, key frames, a final AI review, listen through; `kits/mimi-short/render-cuts.sh <hf> <name>` renders both cuts.

Rive route, between steps 3 and 7: rig (grid + Delaunay mesh, weights from position, five bones: head, ears, two paws, contact), lip-sync (an open-mouth skin shown on syllable peaks, `rig2d.lipsync()`), one `rive --screenshot --advance=N` per frame (`scripts/render_rive.sh`). Pitfalls: the first sibling draws on top; one screenshot per invocation; screenshots are opaque; opacity is property 18, bone rotation 15, position 90/91. Reference episode: [films/mimi-think-sink](../films/mimi-think-sink/PROCESS.md).

## The cast

A series has a fixed cast in [kits/mimi-short/cast/](../kits/mimi-short/cast/README.md): two main characters (Mimi and her Friend) carry every story, the Android bunny appears now and then, and every other role (a native speaker, staff, a date) is played by the small recurring side cast (Bruno the bear, Pippa the duck, Coco the cat), each with a fixed Kokoro voice. No character is made for one episode; a new recurring one is proposed to the owner first. Role outfits are fine. The Lanclo-specific text rules are there too (Mimi's Japanese first person is 「僕」).

## Voices

- **Side cast and other parts**: Kokoro, locally: `npx hyperframes tts "<line>" -v <voice> -o assets/voice/<file>.wav` (see any `source/scripts/voices.sh`). These WAVs are committed. Kokoro's Japanese was garbled, so Japanese lines are speech bubbles and captions, not voice.
- **The learner's and the model's English**: the owner's own voice, registered with Gemini TTS, through `kits/mimi-short/scripts/ownvoice.py` and the episode's `own-voice.json`. Accents `us`, `uk`, `learner` (a Japanese beginner) and `native` (with `language`); `style` replaces the preset (for example a learner who clearly says the wrong word). The voice is biometric: the WAVs never go in Git, only to the episode's Drive folder; Git keeps `own-voice.receipt.json` (text, style, hashes, no voice ID). Each call is a paid generation in the owner's voice: generate only the lines needed (existing clips are skipped; `--force <id>` regenerates one).
- **Checking a mispronunciation**: a transcript is not proof. Whisper's language model "corrects" the wrong word back to the intended one. Use Whisper for word timestamps only, then check the sound itself (formants with Praat, a fricative's spectral centre, silencedetect for word starts) and have a person listen. Examples: the take notes in [mimi-disaster-coke](../films/mimi-disaster-coke/PROCESS.md) and the US/UK check in [mimi-tuning](../films/mimi-tuning/PROCESS.md).

## Showing the real app

Record the product in its simulator with QA fixture data (no personal data, the same screens every time) while a walkthrough UI test taps through the feature: `kits/mimi-short/app-capture/capture.sh <walkthrough.swift> <UITests file it replaces> <Class/testMethod> <out.mov>`. The app checkout and build are cached, so only the first run builds from scratch.

- **Capture-only patches**: when a fixture cannot show what the story needs (another scene's lines, a 30-day streak), write a small text-matched patch and pass `PATCH=<file>`; `apply-patch.py` applies it to the capture checkout, and it is reverted afterwards and never committed to the app. Clear `PATCH` between takes (`env -u PATCH`).
- **Shared simulator**: other sessions use the same simulator, so hold the lock while recording: `until mkdir /tmp/lanclo-capture.lock 2>/dev/null; do sleep 15; done`, record, `rmdir /tmp/lanclo-capture.lock`. Reusing an earlier take from Drive is fine when the screens have not changed.
- `app-capture/cut.sh` resamples the variable-frame-rate take to 60 fps and cuts clips; each episode's `scripts/app_track.sh` holds the measured times on the film's clock.
- Mask fixture-only text (「デモデータ」, QA titles) in the edit; zoom and add a large card for the one point that matters. Screens that are unstable to record (Home Screen widgets, Lock Screen) can be drawn in HTML after the app's code and wording, with a note on the copy card. Examples: [mimi-frozen-abroad](../films/mimi-frozen-abroad/PROCESS.md), [mimi-quitter](../films/mimi-quitter/PROCESS.md), [mimi-shashin](../films/mimi-shashin/PROCESS.md).

## Story shapes

- **Hook first**: the hook text is on screen from frame 1 and stops the viewer within 1.5 s; 15–25 s in all, fast. Then the relatable failure, the real app solving it, the payoff, the end card.
- **Punchline first** ("Pronunciation Disasters"): frame 1 is the punchline (Mimi's reaction, the word censored with ★, an object gag), a rewind, then the slip, the freeze, a mouth card (lips and tongue for the right and the wrong sound, both takes), the app lesson and the fix. Beat table and what to swap per episode: [films/mimi-disaster-sit/README.md](../films/mimi-disaster-sit/README.md#series-template-episodes-26).
- **Two cuts**: Japanese only, and English subtitles (`.sub` clips, hidden by `<body class="no-subs">`), both rendered by `render-cuts.sh`.
- **Sound**: the voice leads; the theme BGM is ducked under it and SFX are softened and kept low; nothing loud. A film without voice may need one gain for the whole film instead of the kit's loudnorm ([mimi-watching](../films/mimi-watching/PROCESS.md)).
- **End card**: `k.end(at)`, then `k.tapCta(at + 0.6)` taps the CTA button; pair it with `sfx.pochi()`.
- **Screen**: captions at the top; keep the bottom ~400 px clear for platform UI; phone UI is atmosphere, meaning goes in large labels; never cover a face.

## Make your own series with your own character

The kit is Lanclo's, but the shape is general. Copy `kits/mimi-short/` to `kits/<your-series>/` and swap:

| Swap | In the kit |
|---|---|
| Character library | `library/` (poses, props, backgrounds, official art). `sync-library.sh` pulls Lanclo's; fill yours by hand or with your own sync |
| Cast | `cast/`: your main character(s) and their reference images, the side cast and their Kokoro voices, and the codex-p prompt template with your character's markings |
| Brand | `brand/` (end-card character, logo, store badge) and the end-card text in `hf/kit.js` (`endCard`, `tapCta`) and `hf/kit.css` |
| BGM | `library/bgm/everyone-get-up.mp3` (`THEME` in `scripts/sfx.py`; not in Git, the theme is licensed separately); without it `sfx.py` plays its code-made bed |
| Voice | Kokoro for everyone, or your own registered voice in place of `ownvoice.py` (its account and voice name are Lanclo's) |

Minimum steps, end to end:

1. Collect the approved character art: a reference sheet in `cast/`, poses in `library/poses/`.
2. Write the story as a beat table with a frame-1 hook.
3. Draw the missing poses with codex-p from the references; `cutout.sh`.
4. Make the voices (Kokoro or your own) and, if you show an app, record it.
5. Copy an episode's `source/` (for example `films/mimi-disaster-sit/source/`) to `films/<id>/source/` point its `kits/mimi-short` paths at your kit, and replace the art, lines and times in `scripts/mix.py` and `hf/index.html`.
6. `stage.sh`, `npx hyperframes check`, `render-cuts.sh`; review and listen.
7. Write the record (below).

## Keep every work reproducible

Each work keeps, in `films/<id>/`: `README.md` / `README.ja.md` (what it is, format, where the finals are), `PROMPT.md` (consolidated prompt), `PROCESS.md` (owner directions verbatim, decisions, fixes, lessons), `prompts/` (verbatim codex-p prompts and logs), `process/` (light JPG frames), `source/` (`README.md` with the rebuild commands, scripts, art, `own-voice.json` and its receipt, the edit) and `CREDITS.md`. Not in Git: own-voice WAVs, simulator takes, `hf/assets/`, renders and the BGM; the source README says where they are (for Lanclo, the episode's Drive folder named after its Notion Content Calendar ID). See [Adding a film](ADDING-A-FILM.md).

## Automating it

For Lanclo SNS shorts the whole flow (intake, fixed rules, build, Drive / Notion delivery, finalize, YouTube and gallery publishing, batch mode) is one agent skill: [lanclo-sns-short](../skills/lanclo-sns-short/SKILL.md).
