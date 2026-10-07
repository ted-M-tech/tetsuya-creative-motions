# Open Works publication — 2026-10-07

## Published

- Portfolio: https://videos.maepace.com/
- LP case: https://videos.maepace.com/works/lanclo-lp/
- Runnable demo: https://videos.maepace.com/demos/lanclo-lp/
- Companion slides: https://videos.maepace.com/slides/lanclo-making/
- Personal-site entry: https://maepace.com/#open-works

JA/EN portfolio, case and deck routes are available. Existing film routes and media remain.

Portfolio implementation merge: `95316233da9bd51c399b5d086aeb620e25513fde` (PR 1).
Worker version: `7c5cfe1b-fae7-45a1-9e02-e42145575ef8`.
MaePace Worker version: `6e45263f-5823-4354-8a5d-18b2052d412d`.

## Validation

- Node 24 clean `npm ci` and standalone LP production build passed.
- Public-file/link/private-value checks and 4 media-range tests passed.
- 36 local Chromium/WebKit combinations: 320/390/1440px across JA/EN portfolio, case, deck, demo and personal site. No horizontal document overflow, undecoded images or page exceptions after image load completion.
- 10 production checks: 390/1440px across portfolio, case, deck, demo and personal site. All returned 200; same layout/image/error checks passed.
- Production MP4 range request returned 206, exactly bytes 0–31, with Content-Range and Accept-Ranges headers.
- MaePace: Astro check/build; 42-page publication validation; 6 payment tests; 40 Learn pages checked for translations. Learn index SHA-256 remained `9114450a8c0bcb2dff21f3159c1c087c6c478db012411d7088d31ebb2056e367` before/after.
- Independent visual review requested three fixes (mobile headline wrapping, real examples in slides, redundant deck labels). The reviewer scored all three resolved. This is not a claim of automated aesthetic correctness.

## Source custody

The personal-site checkout already contained published but uncommitted Learn/payment work. Its baseline was preserved. Only this task's strip, three previews and two integration edits were committed as `7e2406d` in myPortfolioSite PR 4. That draft must not trigger a main build before the existing publication baseline is reconciled. Manual publication uploaded only five changed static assets; existing payment source was unchanged.

The reusable LP has its own source manifest, dependency lock, provenance and credits. `open-works-v1` fixes the public reproduction package. Raw QA captures and finished MP4s remain outside Git. Original code/docs are MIT; linked skills, third-party media, voice and brand rights are not relicensed.
