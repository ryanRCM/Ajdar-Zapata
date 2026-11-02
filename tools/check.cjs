// Serves site/ locally and checks both TVs at TV sizes before every push:
// every menu panel and picture loads, panels sit fully on screen and never overlap, nothing else
// (reel, coming soon, address, logo) covers a panel, no side scroll, no errors,
// and on monitor 2 the slideshow moves on with a food scene playing. Also checks the phone menu page loads.
// Run: node tools/check.cjs [--shots]   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..', 'site');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp' };

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
    const r = await p.evaluate(() => {
      const box = el => el.getBoundingClientRect();
      const meets = (a, c) => a.left < c.right - 1 && c.left < a.right - 1 && a.top < c.bottom - 1 && c.top < a.bottom - 1;
      const secs = [...document.querySelectorAll('.card[class*="sec-"]:not(.tvslide)')];
      const slides = [...document.querySelectorAll('.tvslide')]; // the right TV's slideshow: slides share one space
      // where each slide comes to rest (its layout box, ignoring the glide-in transform)
      const rest = el => ({ left: el.offsetLeft, top: el.offsetTop, right: el.offsetLeft + el.offsetWidth, bottom: el.offsetTop + el.offsetHeight });
      const imgs = [...document.querySelectorAll('#stage img:not([src=""])')];
      const bad = [];
      imgs.forEach(i => { if (!(i.naturalWidth > 0)) bad.push((i.className || i.parentNode.className) + ' not loaded'); });
      secs.forEach(c => { const r = box(c); if (r.left < 0 || r.top < 0 || r.right > innerWidth + 1 || r.bottom > innerHeight + 1) bad.push(c.className + ' off screen'); });
      // panels never overlap each other; nothing that moves or the address/logo covers a menu panel
      const others = [...document.querySelectorAll('.side, .allergy-bar')];
      slides.forEach(c => { const r = rest(c); if (r.left < -1 || r.top < -1 || r.right > innerWidth + 1 || r.bottom > innerHeight + 1) bad.push(c.className + ' off screen'); });
      others.forEach(o => slides.forEach(c => { if (meets(box(o), rest(c))) bad.push((o.className || 'frame') + ' covers ' + c.className); }));
      secs.forEach((a, i) => secs.slice(i + 1).forEach(c => { if (meets(box(a), box(c))) bad.push(a.className + ' overlaps ' + c.className); }));
      others.forEach(o => secs.forEach(c => { if (meets(box(o), box(c))) bad.push((o.className || 'frame') + ' covers ' + c.className); }));
      // the address frame stops short of the logo
      const f = document.querySelector('.address .frame'), l = document.querySelector('.logo');
      if (f && l && meets(box(f), box(l))) bad.push('address runs under the logo');
      return { n: secs.length + slides.length, bad, wide: document.documentElement.scrollWidth > innerWidth, reel: document.querySelectorAll('.scene.on').length };
    });
    let reelOk = true;
    if (page === '/monitor-2/') {
      // the slideshow moves on after the first slide's hold, and a food scene is playing
      const [first, hold] = await p.evaluate(() => { const s = document.querySelector('.tvslide.on'); return [s.className, parseFloat(s.dataset.hold || 8)]; });
      if (process.argv.includes('--shots')) await p.screenshot({ path: path.join(__dirname, `shot-m2-${w}.png`) });
      await p.waitForTimeout(hold * 1000 + 1200);
      const next = await p.evaluate(() => document.querySelector('.tvslide.on')?.className);
      reelOk = r.reel === 1 && !!next && next !== first;
    }
    if (page === '/monitor-1/' && process.argv.includes('--shots')) await p.screenshot({ path: path.join(__dirname, `shot-m1-${w}.png`) });
    const pass = r.n >= 4 && !r.bad.length && !r.wide && !errs.length && reelOk;
    ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} ${page} ${w}x${h}: sections ${r.n}, problems ${r.bad.length}, side scroll ${r.wide}, errors ${errs.length}${page === '/monitor-2/' ? ', slideshow moving ' + reelOk : ''}${r.bad.length ? ' ' + r.bad.join('; ') : ''}${errs.length ? ' ' + errs.join('; ') : ''}`);
    await p.close();
  }
  const m = await b.newPage({ viewport: { width: 390, height: 844 } }); const merrs = [];
  m.on('pageerror', e => merrs.push(e.message));
  await m.goto(base + '/menu/'); await m.waitForTimeout(800);
  const mm = await m.evaluate(() => ({ imgs: [...document.images].filter(i => i.naturalWidth > 0 || i.loading === 'lazy').length, wide: document.documentElement.scrollWidth > innerWidth }));
  const mpass = mm.imgs === 3 && !mm.wide && !merrs.length; ok = ok && mpass;
  console.log(`${mpass ? '✅' : '❌'} /menu/ 390x844: boards ${mm.imgs}/3, side scroll ${mm.wide}, errors ${merrs.length}`);
  await b.close(); server.close(); process.exit(ok ? 0 : 1);
})();
