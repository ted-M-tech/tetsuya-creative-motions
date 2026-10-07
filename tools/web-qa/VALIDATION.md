# Validation receipt

2026-10-07. Node 26.5.1, Playwright 1.63.0, macOS.

- Built the unchanged standalone Lanclo source with Vite and served it on loopback.
- Chromium/WebKit × ja/en/ko × 320/390/820/1440px, height 900px: 24/24 automated reduced-motion smoke checks passed.
- A separate local negative fixture containing document overflow, table-cell overflow, a broken image and a JavaScript exception detected all four conditions and exited 1.
- Skill format and public-document link/private-data checks passed.

This validates the new runner. It does not re-certify the entire LP design, normal-motion interactions, translations, physical devices or production. Screenshots and detailed reports are ignored local outputs, not committed media. Source lockfiles reproduce the tool and example; this receipt is not a complete historic invocation log.
