<div align="center">

# Tetsuya Open Works

[日本語](README.ja.md) · **English**

**Websites, films, slides — and how they were made.**

A public collection of finished work, creative decisions, prompts and runnable source. Learn from the artifact, then make the next one your own.

[▶ Watch the gallery](https://videos.maepace.com/en/) · [Films](#films) · [Styles](styles/README.md) · [Re-edit a film](docs/REPRODUCE.md)

</div>


## Web, slides & reproducible process

[Lanclo LP: runnable source and making of](projects/lanclo-lp/README.md) · [Companion slides](https://videos.maepace.com/slides/lanclo-making/) · [Open handoff skill](skills/open-creative-handoff/SKILL.md)

The portfolio now includes websites, films and teaching slides. One project can have several formats. Historical film claims are preserved as creative records, not current product specifications.

To build the whole site: `npm ci --prefix projects/lanclo-lp/source`, then `npm run check && npm test && npm run build`. Media-inclusive deployment still uses the separately licensed release MP4s described below.

## Install the LP skill bundle

From this checkout, run `python3 scripts/install-lp-skills.py` to install **lp-create + Impeccable + Taste Skill** together. Requires Python 3.9+ and Git. The same command updates managed installations to the reviewed, pinned bundle; locally edited skills are preserved. [Installation and maintenance](docs/LP-SKILL-INSTALL.ja.md).

## Films

[![Lanclo](site/posters/lanclo-daily.jpg)](https://videos.maepace.com/en/films/lanclo-daily/)

**Lanclo — Your voice. Your daily English.** · 1:09 · Japanese audio

Your own AI voice, ten personalized questions, and daily news that becomes English learning material.

[Watch & read the making of](https://videos.maepace.com/en/films/lanclo-daily/) · [Production files](films/lanclo/README.md)

The visuals are authored in HTML/SVG and GSAP, then rendered with HyperFrames. Characters come from unDraw and narration uses Gemini TTS.

**Lanclo One line — one line shows it all.** · 0:26 promo (16:9) + feature shorts (9:16) · Japanese type, English subtitles

[Source, reproduction prompt & style](films/lanclo-one-line/README.md)

Borrows the structure of Duolingo's spec ad "The Path": one line and a camera flight through the features. Every frame and sound is generated in Python (pycairo, numpy).

**Mimi 3D — the mascot as a soft vinyl toy.** · Blender, 3D character

[Process, prompts & reviews](films/mimi-3d/README.md) · [3D character workflow](docs/3D-CHARACTER-WORKFLOW.md)

The 2D mascot rebuilt in Blender from Python alone, finished through nine Claude Code × Codex review rounds.

### Mimi shorts (2D, vertical, 15–25 s)

Lanclo's mascot Mimi and her friend in the official 2D style (Codex art + HyperFrames), most beside the real app recorded in the simulator. Every film keeps its process, prompts and runnable source. How to make one, or your own series: [2D character animation guide](docs/2D-CHARACTER-ANIMATION.md) · [Mimi shorts kit](kits/mimi-short/README.md) · [the cast](kits/mimi-short/cast/README.md).

- **First shorts (Rive bones)** — [My own voice? No way](films/mimi-jibun-no-koe/README.md) · ["think" turns into "sink"](films/mimi-think-sink/README.md) · [Asked the way, she freezes](films/mimi-michi/README.md) · [The diary ends on day three](films/mimi-nikki/README.md)
- **Real app** — [Describe a photo](films/mimi-shashin/README.md) · [Tsundoku](films/mimi-daily/README.md) · [Lost an argument in English](films/mimi-debate/README.md) · [Keep talking for 3 minutes](films/mimi-freespeech/README.md) · [Talked for 180 seconds](films/mimi-180/README.md) · [One month to IELTS](films/mimi-ielts/README.md) · [AI chat never knows what to talk about](films/mimi-topics/README.md) · [I stopped shadowing native speakers](films/mimi-no-shadowing/README.md)
- **Action Button** — [① Add a phrase](films/mimi-action-add/README.md) · [② Start review](films/mimi-action-review/README.md) · [③ Today's lesson](films/mimi-action-lesson/README.md)
- **Roleplay** — [Frozen at the café](films/mimi-roleplay/README.md) · [Frozen abroad](films/mimi-frozen-abroad/README.md)
- **AI voice** — [AI voice in 1 minute](films/mimi-voice/README.md) · [Voice tuning](films/mimi-tuning/README.md) · [US vs UK in my own voice](films/mimi-us-uk/README.md) · [Your voice in every language](films/mimi-multilang/README.md)
- **My Notes** — [Mimi eats your files](films/mimi-import/README.md) · [I fed my flashcards to Mimi](films/mimi-flashcards/README.md) · [Swipe review](films/mimi-swipe/README.md)
- **Habit and Mimi's report** — [One loop in Lanclo](films/mimi-loop/README.md) · [Mimi is always watching](films/mimi-watching/README.md) · [Watched by Mimi for a month](films/mimi-month/README.md) · [How a quitter kept going](films/mimi-quitter/README.md)
- **Pronunciation Disasters** (punchline first) — [1 Sit](films/mimi-disaster-sit/README.md) · [2 Beach](films/mimi-disaster-beach/README.md) · [3 Rice](films/mimi-disaster-rice/README.md) · [4 Election](films/mimi-disaster-election/README.md) · [5 Coke](films/mimi-disaster-coke/README.md) · [6 Peace](films/mimi-disaster-peace/README.md)

## Use my filmmaking workflow

[Install the reusable skill and follow the walkthrough](docs/VIDEO-WORKFLOW.md). Learn from Lanclo, then apply the workflow to your own project. The skill guides creative decisions and production records; rendering tools and voice access are separate.

## Explore the work

1. **Watch** — Start with the finished film and its creative intent.
2. **Read** — `PROMPT.md` describes the final brief, `NARRATION.md` contains the script, and `TTS-PROMPTS.json` records voice-generation inputs.
3. **Adapt** — Use the style notes as a starting point with your own subject, brand, and licensed materials.
4. **Re-edit** — Open the source using the [reproduction guide, in Japanese](docs/REPRODUCE.md).

The consolidated prompt records decisions made during production. It is not a claim that the film was produced from a single prompt. Original scripts and generation inputs retain their original languages; private voice identifiers are excluded.

## Run the gallery

The static site lives in [`site/`](site/). It is published at [videos.maepace.com](https://videos.maepace.com/en/).

```sh
npm run dev
# http://localhost:4173/en/
```

Finished media is distributed separately from Git. Place `lanclo-daily-r26.mp4` (current), `lanclo.mp4` (early version), and `lanclo-osaka.mp4` (bonus) in `site/media/`. See the [publishing guide, in Japanese](docs/PUBLISHING.md).

## Repository layout

```text
films/
  lanclo/    Project overview, current script and prompts
    source/  Current editable composition
    extras/  Bonus experiments, including the Osaka remix
    history/ Earlier versions and production records
skills/      Reusable filmmaking workflow
styles/      Reusable visual direction
site/        Japanese gallery and English pages under en/
scripts/     Build and publication checks
docs/        Reproduction, publishing, and licensing guides
templates/   Starting point for the next project
```

One project gets one gallery entry. Revisions stay within that project; alternate narration belongs under extras. See [how to add a film, in Japanese](docs/ADDING-A-FILM.md).

## Inspiration and licensing

The presentation draws inspiration from [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar): show the film, the style, and the prompts together. This portfolio has its own copy and site implementation.

Original code and documentation use the [MIT license](LICENSE). Films, third-party assets, brand materials, and personal voices have separate conditions. Consult each film's `CREDITS.md` and the [licensing scope, in Japanese](docs/LICENSING.md).

## Web production standard

[Workflow: Astro + TypeScript, static-first (Japanese)](docs/WEB-WORKFLOW.ja.md) · [Installable Web skill](skills/lp-create/SKILL.md) · [Reproduction record](templates/web/REPRODUCTION.md)

Impeccable is the primary design aid; Taste Skill supports alternatives and critique when useful. Record actual usage, revisions, prompts and pinned source. Existing works retain their documented implementation and historical provenance.
