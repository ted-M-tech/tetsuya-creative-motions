# Lanclo landing page — open study

A runnable export of the published LP, with the decisions that produced it. This is a front-end study, not the Lanclo application.

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
