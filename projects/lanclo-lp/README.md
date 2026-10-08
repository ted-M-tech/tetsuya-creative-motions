# Lanclo landing page — open study

A runnable, pinned **pre-Astro edition** of the LP, with the decisions that produced it. This is a front-end study, not the Lanclo application or the current production build.

The production LP moved to Astro static output with TypeScript page orchestration on 2026-10-07 (upstream PRs #166 and #167, source `9bf6c361a5ac71db4b0af5f27927cb240c85277b`). Existing React/JSX interactions were preserved. This exported Vite edition intentionally retains its original source manifest and provenance; do not treat it as a current Astro reproduction kit.

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

For this published study, check out the `open-works-v1` tag before running the commands above. Verify exported files against [source-manifest.json](source-manifest.json). Later changes on main may differ. The film media is optional and distributed separately; it is not needed to run the LP.
