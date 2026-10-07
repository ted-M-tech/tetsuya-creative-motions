import { chromium, webkit } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { parseArgs } from 'node:util';

const { values } = parseArgs({ options: {
  url: { type: 'string', default: 'http://127.0.0.1:4173/' },
  widths: { type: 'string', default: '320,390,820,1440' },
  locales: { type: 'string', default: 'ja,en,ko' },
  browsers: { type: 'string', default: 'chromium,webkit' },
  out: { type: 'string', default: '../../.local/web-qa' }
}});
const url = new URL(values.url);
if (!['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)) {
  throw new Error('Use a local preview. This tool is not a production audit or a sandbox for untrusted pages.');
}
await fetch(url, {signal: AbortSignal.timeout(5000)}).catch(() => {
  throw new Error('Preview is not ready. Start the built preview server before running QA.');
});
const widths = values.widths.split(',').map(Number);
if (widths.some(w => !Number.isInteger(w) || w < 240 || w > 3840)) throw new Error('Invalid viewport width');
const locales = values.locales.split(',');
if (locales.some(l => !/^[a-zA-Z0-9-]+$/.test(l))) throw new Error('Invalid locale');
const engines = { chromium, webkit };
const browsers = values.browsers.split(',');
if (browsers.some(b => !engines[b])) throw new Error('Use chromium,webkit');
const out = resolve(values.out);
await mkdir(out, { recursive: true });
const results = [];
for (const engine of browsers) {
  const browser = await engines[engine].launch();
  try {
    for (const locale of locales) for (const width of widths) {
      const context = await browser.newContext({viewport: {width, height: 900}, reducedMotion: 'reduce'});
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      const name = `${engine}-${locale}-${width}`;
      try {
        const target = new URL(url);
        target.searchParams.set('lang', locale);
        const response = await page.goto(target.href, { waitUntil: 'networkidle', timeout: 30000 });
        await page.evaluate(() => document.fonts.ready);
        // Reveal in-view sections and lazy images before taking a full-page capture.
        for (let y = 0; y < await page.evaluate(() => document.documentElement.scrollHeight); y += 700) {
          if (y > 50000) throw new Error('Page exceeds bounded capture height');
          await page.evaluate(y => scrollTo(0, y), y);
          await page.waitForTimeout(60);
        }
        await page.evaluate(() => scrollTo(0, 0));
        await page.waitForTimeout(250);
        const observations = await page.evaluate(async () => {
          const images = await Promise.all([...document.images].map(async img => {
            try { await img.decode(); return null; }
            catch { return img.getAttribute('src') || '(missing src)'; }
          }));
          const cells = [...document.querySelectorAll('th,td')].filter(e =>
            e.getClientRects().length && e.scrollWidth > e.clientWidth + 2
          ).map(e => e.textContent.trim().slice(0, 100));
          return {
            documentOverflow: document.documentElement.scrollWidth > innerWidth + 2,
            overflowingCells: cells,
            brokenImages: images.filter(Boolean),
            renderedLang: document.documentElement.lang,
            reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
            headings: [...document.querySelectorAll('h1,h2')].map(e => e.textContent.trim())
          };
        });
        await page.screenshot({path: resolve(out, `${name}.png`), fullPage: true});
        const passed = response?.ok() && !errors.length && !observations.documentOverflow
          && !observations.overflowingCells.length && !observations.brokenImages.length;
        results.push({name, viewport: {width, height:900}, requestedLocale:locale, status:response?.status(), passed:Boolean(passed), errors, ...observations});
        console.log(`${passed ? 'PASS' : 'FAIL'} ${name}`);
      } catch (e) {
        results.push({name, passed:false, errors:[...errors,e.message]});
        console.log(`FAIL ${name}: ${e.message}`);
      } finally { await context.close(); }
    }
  } finally { await browser.close(); }
}
await writeFile(resolve(out, 'report.json'), JSON.stringify({
  checkedAt: new Date().toISOString(), url:url.href,
  scope:'Local responsive smoke checks with reduced motion. Screenshots require human review; viewport emulation is not a physical-device test.',
  results
}, null, 2));
if (results.some(r => !r.passed)) process.exitCode = 1;
