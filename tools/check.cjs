// Serves site/ locally and checks both monitors at TV sizes: three boards filling the
// screen, no side scroll, no errors, and on monitor 2 the food reel playing.
// Run: node tools/check.cjs [--shots]   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..', 'site');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png' };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  // Stand-in for the Netlify Function the TVs check in with (netlify/functions/screen.mjs).
  if (p === '/api/screen') { res.writeHead(200, { 'content-type': 'application/json' }); return res.end('{"version":"local"}'); }
  if (p === '/') p = '/monitor-1/';
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(0);

(async () => {
  const base = 'http://localhost:' + server.address().port;
  const b = await chromium.launch(); let ok = true;
  for (const page of ['/', '/monitor-1/', '/monitor-2/']) for (const [w, h] of [[1920, 1080], [1366, 768]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('requestfailed', r => { if (!r.url().includes('fonts.g') && !(r.url().includes('/api/screen') && /ABORTED/.test(r.failure()?.errorText || ''))) errs.push('failed ' + r.url()); });
    await p.goto(base + page); await p.waitForTimeout(1500);
    const r = await p.evaluate(() => ({
      imgs: [...document.querySelectorAll('.board > img')].map(i => { const b = i.getBoundingClientRect(); return i.naturalWidth > 0 && Math.round(b.height) === innerHeight && Math.abs(b.width - innerWidth / 3) < 1; }),
      wide: document.documentElement.scrollWidth > innerWidth,
      reel: document.querySelectorAll('.scene.on').length,
    }));
    let reelOk = true;
    if (page === '/monitor-2/') {
      // Wait out the first scene's own hold time (data-hold, seconds), then the reel must show another scene.
      const [first, hold] = await p.evaluate(() => { const s = document.querySelector('.scene.on'); return [s.querySelector('.label').textContent, parseFloat(s.dataset.hold || 3.6)]; });
      await p.waitForTimeout(hold * 1000 + 300);
      const next = await p.evaluate(() => document.querySelector('.scene.on:not(.out) .label')?.textContent);
      reelOk = r.reel === 1 && !!next && next !== first;
      if (process.argv.includes('--shots')) await p.screenshot({ path: path.join(__dirname, `shot-m2-${w}.png`) });
    }
    const pass = r.imgs.length === 3 && r.imgs.every(Boolean) && !r.wide && !errs.length && reelOk;
    ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} ${page} ${w}x${h}: boards fill ${r.imgs.filter(Boolean).length}/3, side scroll ${r.wide}, errors ${errs.length}${page === '/monitor-2/' ? ', reel moving ' + reelOk : ''}${errs.length ? ' ' + errs.join('; ') : ''}`);
  }
  await b.close(); server.close(); process.exit(ok ? 0 : 1);
})();
