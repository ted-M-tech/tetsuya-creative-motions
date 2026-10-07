# Validation

Run `npm ci && npm run build` in source with Node 24. Serve the built output with `npm run preview`.

Check 320px, 390px and 1440px viewports: no document overflow, all images decode, natural Japanese wrapping, visible comparison alternatives, working keyboard navigation, no browser exceptions. Repeat with reduced motion. Check product links point to the real app rather than a missing local route.

A source build reproduces a historical marketing page, not backend functionality or study outcomes. Changes to its claims need fresh product/source verification. The original application's test count is not evidence for this independent export.

## Runnable responsive checks

[Public Playwright workflow (Japanese)](../../docs/WEB-QA.ja.md) provides a newly extracted local-preview runner for Chromium/WebKit, locales and viewport widths. It is not the original historical temporary test script. Run it after the preview server is ready, then review the screenshots and test normal motion, keyboard and CTA behavior separately.
