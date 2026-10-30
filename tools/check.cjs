// Opens site/index.html at TV size and checks all three boards load full height with no errors.
// Run: node tools/check.cjs   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch(); let ok = true;
  for (const [w, h] of [[1920, 1080], [1366, 768]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + path.join(__dirname, '..', 'site', 'index.html')); await p.waitForTimeout(500);
    const imgs = await p.evaluate(() => [...document.images].map(i => ({ loaded: i.naturalWidth > 0, h: Math.round(i.getBoundingClientRect().height) })));
    const wide = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    const pass = imgs.length === 3 && imgs.every(i => i.loaded && i.h === h) && !wide && !errs.length;
    ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} ${w}x${h}: ${imgs.filter(i => i.loaded).length}/3 boards, full height ${imgs.every(i => i.h === h)}, no side scroll ${!wide}, errors ${errs.length}`);
  }
  await b.close(); process.exit(ok ? 0 : 1);
})();
