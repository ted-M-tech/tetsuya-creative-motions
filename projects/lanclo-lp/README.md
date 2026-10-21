# Lanclo landing page — open study

A runnable front-end study of the approved navy LP published on 2026-10-08, upstream source `ffc2ca7` (PR189). Includes three illustrated practice steps, personalized practice and news, research, pricing, and two developer voices over the Canadian Rockies.

Production uses Astro static output. This export uses Vite with the React/TypeScript components for a standalone API-free study. It is not the Lanclo application or backend. The original edition remains at `open-works-v1`.

## Create this page with your agent

[Copy the creation prompt (Japanese)](CREATE.ja.md) · [English](CREATE.en.md). The prompt starts from this complete fixed kit and takes you through a working preview.

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

For this updated study, check out the `lanclo-lp-create-v3` tag before running the commands above. Verify exported files against [source-manifest.json](source-manifest.json). Later changes on main may differ. The film media is optional and distributed separately; it is not needed to run the LP.

## Search ownership

The public demo entry URLs `/demos/lanclo-lp`, `/demos/lanclo-lp/` and `/demos/lanclo-lp/index.html` permanently redirect (301) to `https://lanclo.app/lp/` through `site/_redirects`. Cloudflare preserves query parameters, including `lang`, because the destination has no query. Keep the source and assets for archival study; the official product page owns search traffic.

Production uses the dedicated `lanclo-demo-redirect` Worker from `wrangler.redirect.jsonc`, scoped to `videos.maepace.com/demos/lanclo-lp*`. It redirects only the three entry paths; all other requests, including assets and Range requests, pass unchanged to the existing `tetsuya-creative-motions` service binding. This allows retiring the demo without rebuilding or publishing unrelated video assets. The static rules above are retained for future asset publications. Deploy the redirect independently; do not run the full site's deploy command for this change.

Published 2026-10-21 with owner approval: redirect Worker version `207cf184-ace3-453c-8cb7-3942f1f3b7a7`. Original static Worker remains `e8802879-50f5-4ef4-af1c-56b41e7481b3`; no video assets were uploaded. Nine live path/query cases return 301 to the official landing and an existing demo SVG remains 200. Unit coverage includes pass-through asset Range requests. Google index replacement awaits recrawling.
