// Serves site/ locally and checks both TVs at TV sizes before every push:
// every menu panel and picture loads, panels sit fully on screen and never overlap, nothing else
// (reel, coming soon, address, logo) covers a panel, no side scroll, no errors,
// and on monitor 2 the slideshow moves on with a food scene playing. Also checks the phone menu page loads,
// that no light effect crosses the left TV's text, that the menu is the main part of the loop, that a
// reload with the network down still shows the menu (/sw.js), and that the watchdog reloads a stuck show.
// Run: node tools/check.cjs [--shots]   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..', 'site');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp' };

let down = false;   // true = the Wi-Fi is off: every request dies
const server = http.createServer((req, res) => {
  if (down) return req.socket.destroy();
  let p = decodeURIComponent(req.url.split('?')[0]);
  // Stand-in for the Netlify Function the TVs check in with (netlify/functions/screen.mjs).
  if (p === '/api/screen') { res.writeHead(200, { 'content-type': 'application/json' }); return res.end('{"version":"local"}'); }
  if (p === '/') p = '/monitor-1/';
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  if (req.method === 'HEAD') return res.end();   // the clock check (/show.js) only reads the Date header
  fs.createReadStream(f).pipe(res);
}).listen(0);

(async () => {
  const base = 'http://localhost:' + server.address().port;
  const b = await chromium.launch(); let ok = true;
  for (const page of ['/', '/monitor-1/', '/monitor-2/']) for (const [w, h] of [[1920, 1080], [1366, 768]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('requestfailed', r => { if (!r.url().includes('fonts.g') && !(/\/api\/screen|\/show\.js\?clock/.test(r.url()) && /ABORTED/.test(r.failure()?.errorText || ''))) errs.push('failed ' + r.url()); });
    // monitor 2 starts on its first slide (?slide=), so the run is the same every time
    await p.goto(base + page + (page === '/monitor-2/' ? '?slide=starters' : '')); await p.waitForTimeout(1500);
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
      const others = [...document.querySelectorAll('.side')];
      if (document.querySelector('.allergy-bar')) bad.push('allergy notice is back on a TV (it belongs on /menu/ only)');
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
      const [first, left] = await p.evaluate(() => [document.querySelector('.tvslide.on, .hero.on')?.dataset.id, AZShow.at().ends - AZShow.now()]);
      if (process.argv.includes('--shots')) await p.screenshot({ path: path.join(__dirname, `shot-m2-${w}.png`) });
      await p.waitForTimeout(left + 1200);
      const next = await p.evaluate(() => document.querySelector('.tvslide.on, .hero.on')?.dataset.id);
      reelOk = r.reel === 1 && !!next && next !== first;
    }
    if (page === '/monitor-1/') {   // the whole menu, always readable: nothing sweeps over the text, no panel is moved
      const m1 = await p.evaluate(() => [
        ...[...document.querySelectorAll('.sweep, .live-sweep')].filter(e => getComputedStyle(e).display !== 'none').map(e => e.className + ' passes over the menu text'),
        ...[...document.querySelectorAll('.card, .card > img')].filter(e => getComputedStyle(e).transform !== 'none' || getComputedStyle(e).animationName !== 'none').map(e => e.className + ' is moved'),
      ]);
      r.bad.push(...m1);
    }
    if (page === '/monitor-1/' && process.argv.includes('--shots')) await p.screenshot({ path: path.join(__dirname, `shot-m1-${w}.png`) });
    const pass = r.n >= 4 && !r.bad.length && !r.wide && !errs.length && reelOk;
    ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} ${page} ${w}x${h}: sections ${r.n}, problems ${r.bad.length}, side scroll ${r.wide}, errors ${errs.length}${page === '/monitor-2/' ? ', slideshow moving ' + reelOk : ''}${r.bad.length ? ' ' + r.bad.join('; ') : ''}${errs.length ? ' ' + errs.join('; ') : ''}`);
    await p.close();
  }
  // --shots: a screenshot of every slide on the right TV (tools/shot-m2-<slide>.png), taken a few seconds in,
  // and the left TV while each section is live (tools/shot-m1-live.png).
  if (process.argv.includes('--shots')) {
    const ids = ['starters', 'sauces', 'hero-sauce', 'sandwiches', 'burgers', 'hero-sandwich', 'doner', 'platters', 'hero-burger', 'shawarma', 'hotdogs', 'drinks', 'hero-brand'];
    for (const id of ids) {
      const p = await b.newPage({ viewport: { width: 1920, height: 1080 } }); const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto(base + '/monitor-2/?preview&slide=' + id); await p.waitForTimeout(id.startsWith('hero') ? 3600 : 2000);
      await p.screenshot({ path: path.join(__dirname, `shot-m2-${id}.png`) });
      const on = await p.evaluate(() => document.querySelector('.tvslide.on, .hero.on')?.dataset.id);
      const pass = on === id && !errs.length; ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} shot /monitor-2/ ${id}: showing ${on}${errs.length ? ' ' + errs.join('; ') : ''}`);
      await p.close();
    }
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(base + '/monitor-1/?preview&slide=hero-sauce'); await p.waitForTimeout(1600);
    await p.screenshot({ path: path.join(__dirname, 'shot-m1-live.png') });
    const live = await p.evaluate(() => document.querySelector('.card.live')?.className);
    const pass = /sec-sauces/.test(live || ''); ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} /monitor-1/ sparkles round the section the right TV shows: ${live}`);
    await p.close();
  }
  // The menu is the main part of the right TV's loop: menu holds 11-14 s, heroes and poster under 40% of the time
  // (in the Christmas season, when the poster is in).
  {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(base + '/monitor-2/?preview&season=christmas'); await p.waitForTimeout(500);
    const sl = await p.evaluate(() => AZShow.SLIDES);
    const menu = sl.filter(x => !x[0].startsWith('hero')), sum = a => a.reduce((t, x) => t + x[1], 0);
    const share = 1 - sum(menu) / sum(sl);
    const pass = menu.length === 9 && menu.every(x => x[1] >= 11 && x[1] <= 14) && share < 0.4; ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} loop: ${sum(sl)} s, menu ${sum(menu)} s, heroes and poster ${(share * 100).toFixed(0)}% (must stay under 40%), menu holds ${Math.min(...menu.map(x => x[1]))}-${Math.max(...menu.map(x => x[1]))} s`);
    await p.close();
  }
  // Always on. (1) Wi-Fi down: after one normal load and reload, a reload with the server gone still shows the
  // menu, every picture included. (2) A stuck show: stop the slides changing; the watchdog reloads the page.
  for (const page of ['/monitor-1/', '/monitor-2/']) {
    const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } }); const p = await ctx.newPage();
    await p.goto(base + page + '?preview&slide=starters');
    await p.evaluate(() => navigator.serviceWorker.ready); await p.waitForTimeout(500);
    await p.reload(); await p.waitForTimeout(2500);   // this load goes through the service worker, which keeps a copy
    down = true;
    await p.goto(base + page + '?preview&slide=starters&v=offline').catch(() => {}); await p.waitForTimeout(2500);
    const off = await p.evaluate(() => {
      const imgs = [...document.querySelectorAll('#stage img:not([src=""])')];
      return { cards: document.querySelectorAll('.card[class*="sec-"]').length, imgs: imgs.length, loaded: imgs.filter(i => i.naturalWidth > 0).length,
        css: getComputedStyle(document.getElementById('stage')).position, showing: document.body.dataset.monitor === '1' || !!document.querySelector('.tvslide.on, .hero.on') };
    }).catch(() => ({}));
    down = false;
    const pass = off.cards === 9 && off.imgs > 8 && off.loaded === off.imgs && off.css === 'fixed' && off.showing; ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} ${page} with the network down: sections ${off.cards}, pictures ${off.loaded}/${off.imgs}, showing ${off.showing}`);
    await ctx.close();
  }
  {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(base + '/monitor-2/?preview&slide=starters'); await p.waitForTimeout(2500);
    // stop the page's clock, so the slide never changes; then put it forward one whole loop (same slide, 3 minutes on)
    const before = await p.evaluate(() => { window.__old = true; const t = Date.now(); window.__t = t; Date.now = () => window.__t; return document.querySelector('.tvslide.on')?.dataset.id; });
    await p.waitForTimeout(16000);
    await p.evaluate(() => { window.__t += AZShow.SLIDES.reduce((t, x) => t + x[1], 0) * 1000; });
    await p.waitForTimeout(18000);
    const reloaded = await p.evaluate(() => !window.__old).catch(() => false);
    const pass = before === 'starters' && reloaded; ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} /monitor-2/ watchdog: a show stuck on "${before}" reloads itself: ${reloaded}`);
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
