# Lanclo landing page — open study

A runnable front-end study of the approved navy LP published on 2026-10-08, upstream source `e133711` (PR179). Includes the two-layer pointer-responsive wave, three illustrated practice steps, current pricing presentation and shared navy palette.

Production uses Astro static output. This export uses Vite with the React/TypeScript components for a standalone API-free study. It is not the Lanclo application or backend. The original edition remains at `open-works-v1`.

## Run

Use Node 24 and npm. From this repository:

```sh
cd projects/lanclo-lp/source
npm ci
npm run dev
# Production build
npm run build
npm run preview
```

No API keys, Firebase project, recordings or paid generation are required. Product buttons open the real Lanclo site. Scores are illustrative; pricing and availability are the historical LP copy, not a promise that the offer remains available.

## Reproduce the process

1. Read [the brief](BRIEF.md) and replace the product facts with your own.
2. Read [actual prompt excerpts](PROMPTS.md), then use the explicitly reconstructed prompt.
3. Review [decisions](DECISIONS.md) before changing the implementation.
4. Read [skills and provenance](SKILLS.md) and [asset credits](CREDITS.md).
5. Build with the committed lockfile; use [the validation checklist](VALIDATION.md).

[provenance.json](provenance.json) records the original source revision, export boundaries and local skill fingerprints. AI generation is not deterministic: the committed source and dependency lock reproduce the implementation; a prompt alone does not reproduce identical pixels.

The root MIT license covers original code and documentation. Third-party media and Lanclo branding retain their own terms; see credits before adapting.

## Fixed edition

For this updated study, check out the `lanclo-lp-navy-v2` tag before running the commands above. Verify exported files against [source-manifest.json](source-manifest.json). Later changes on main may differ. The film media is optional and distributed separately; it is not needed to run the LP.
