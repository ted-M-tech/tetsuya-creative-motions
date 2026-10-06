# Lanclo — Your voice. Your daily English.

[日本語](README.md) · **English**

[![Lanclo](../../site/posters/lanclo-daily.jpg)](https://videos.maepace.com/en/films/lanclo-daily/)

**1:09 · 1920×1080 · 30fps · Japanese audio**

A product film about learning with your own AI voice, personalized ten-question lessons, and daily news that becomes English learning material.

[Watch & read the making of](https://videos.maepace.com/en/films/lanclo-daily/) · [Editable source](source/) · [Timeline](TIMING.json)

## Creative decisions

- Catch attention with a question in the first second, then introduce the learner's own AI voice.
- Show the full experience: record, hear the voice model, and speak.
- Turn analysis into ten sentence cards so the benefit of automatic lesson assembly is visible. This illustrates selecting and assembling candidate sentences, not unrestricted real-time sentence generation.
- Bridge into news with “And your daily news becomes your English learning material,” followed by overnight discovery and morning delivery.
- Keep the research claim specific: approximately 1.3× the average gain on an intonation test. It is not a claim about general learning efficiency or Lanclo's effectiveness.

## Production

HTML/SVG and GSAP animation, rendered with HyperFrames. unDraw characters, navy opening titles, and an ivory/teal palette. Japanese narration uses Gemini 3.8 Flash TTS / Leda at 1.2× playback with pitch preserved. The two English demonstration lines use the same synthetic Aoede take; they are not actual learner recordings.

## Production files

The following are original production artifacts, primarily in Japanese. The English making-of page explains the creative intent while preserving these inputs for reference.

| File | Contents |
|---|---|
| [PROMPT.md](PROMPT.md) | Consolidated final brief, not a single original input |
| [NARRATION.md](NARRATION.md) | Full current narration script |
| [TTS-PROMPTS.json](TTS-PROMPTS.json) | Historical generation inputs; see the timeline for selected takes |
| [TIMING.json](TIMING.json) | Scene and audio placement |
| [CREDITS.md](CREDITS.md) | Research sources, assets, and licensing conditions |
| [MEDIA.json](MEDIA.json) | Audio files needed for re-editing; audio is excluded from Git |
| [source/](source/) | Current editable composition |

## Research context

Li, Lian, and Yodkamlue (2020) compared two groups of 33 learners over 12 weeks. Mean intonation-test gains were 65.52 points for the native-speaker model and 86.61 for the self-voice model: 86.61 ÷ 65.52 ≈ 1.3. This is a ratio of score gains, not final scores or learning speed. The study evaluated a different system. Full citation and before/after scores appear in [CREDITS.md](CREDITS.md).

## Bonus and history

- [Osaka-dialect bonus](https://videos.maepace.com/en/films/lanclo-daily/#extras): a comic narration experiment using the early visuals. [Original production files](extras/osaka/).
- [Early version](https://videos.maepace.com/en/films/lanclo-daily/#history): compare the opening, lesson explanation, and news transition. [Archived files](history/r18/).

For re-editing, follow the [Japanese reproduction guide](../../docs/REPRODUCE.md). Supply licensed audio separately; original recordings, API credentials, and private voice identifiers are not included.
