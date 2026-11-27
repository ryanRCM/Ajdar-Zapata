// Serves site/ locally and checks both TVs at TV sizes before every push:
// every menu panel and picture loads, panels sit fully on screen and never overlap, nothing else
// (reel, coming soon, address, logo) covers a panel, no side scroll, no errors,
// and on monitor 2 the slideshow moves on with a food scene playing. Also checks the phone menu page loads, and the
// shop TVs' page (/tv1, /tv2, the plain address): its pictures are up to date with the menu, each TV shows its
// own half of the menu, still (the halves together are the whole menu, once), it remembers which TV it is, the
// keep-awake video plays, it never reloads, and Netlify's script never runs.
// Run: node tools/check.cjs [--shots]   (needs Playwright + Chromium)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..', 'site');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.json': 'application/json', '.webm': 'video/webm', '.mp4': 'video/mp4', '.txt': 'text/plain' };
const tvInputs = require('./tv-inputs.cjs');
const tvPage = require('./tv-page.cjs');
let fakePage = '', fakeScreens = null;   // stand-ins for show.json   // when set, the stand-in show.json says a new TV page is live

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  // As Netlify: the injected badge script (a stand-in that only leaves a mark), and the addresses in site/_redirects.
  if (p === '/.netlify/scripts/hud') { res.writeHead(200, { 'content-type': 'text/javascript' }); return res.end('window.__netlifyRan = true;'); }
  if (p === '/' || p === '/tv1' || p === '/tv2') p = '/tv/';
  if (p === '/tv/show.json' && fakeScreens) { res.writeHead(200, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ ...JSON.parse(fs.readFileSync(path.join(root, 'tv', 'show.json'))), screens: fakeScreens })); }
  if (p === '/tv/show.json' && fakePage) { res.writeHead(200, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ ...JSON.parse(fs.readFileSync(path.join(root, 'tv', 'show.json'))), page: fakePage })); }
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  if (req.method === 'HEAD') return res.end();   // the clock check (/show.js) only reads the Date header
  if (f.endsWith('.html')) return res.end(fs.readFileSync(f, 'utf8') + '\n<script async src="/.netlify/scripts/hud?variant=public" data-nf-variant="public"></script>');
  fs.createReadStream(f).pipe(res);
}).listen(0);

(async () => {
  const base = 'http://localhost:' + server.address().port;
  const b = await chromium.launch(); let ok = true;
  for (const page of ['/monitor-1/', '/monitor-2/']) for (const [w, h] of [[1920, 1080], [1366, 768]]) {
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
    if (page === '/monitor-1/' && process.argv.includes('--shots')) await p.screenshot({ path: path.join(__dirname, `shot-m1-${w}.png`) });
    const pass = r.n >= 4 && !r.bad.length && !r.wide && !errs.length && reelOk;
    ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} ${page} ${w}x${h}: sections ${r.n}, problems ${r.bad.length}, side scroll ${r.wide}, errors ${errs.length}${page === '/monitor-2/' ? ', slideshow moving ' + reelOk : ''}${r.bad.length ? ' ' + r.bad.join('; ') : ''}${errs.length ? ' ' + errs.join('; ') : ''}`);
    await p.close();
  }
  // --shots: a screenshot of every slide on the right TV (tools/shot-m2-<slide>.png), taken a few seconds in,
  // and the left TV while each section is live (tools/shot-m1-live.png).
  if (process.argv.includes('--shots')) {
    const ids = ['starters', 'sauces', 'hero-sauce', 'sandwiches', 'burgers', 'hero-sandwich', 'doner', 'platters', 'hero-burger', 'shawarma', 'hero-lineup', 'hotdogs', 'drinks', 'hero-brand', 'hero-robbery'];
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
  // The two halves of the menu (/monitor-1/?half=1, ?half=2; the TVs show pictures of them): each half's panels sit
  // on screen, never overlap and load; both in the same yellow; together they are the whole menu, once.
  {
    const seen = {};
    for (const half of [1, 2]) {
      const p = await b.newPage({ viewport: { width: 1920, height: 1080 } }); const errs = [];
      p.on('pageerror', e => errs.push(e.message));
      await p.goto(base + '/monitor-1/?preview&half=' + half); await p.waitForTimeout(1500);
      const r = await p.evaluate(() => {
        const box = el => el.getBoundingClientRect();
        const meets = (a, c) => a.left < c.right - 1 && c.left < a.right - 1 && a.top < c.bottom - 1 && c.top < a.bottom - 1;
        const secs = [...document.querySelectorAll('.card[class*="sec-"]')].filter(c => c.offsetParent);
        const bad = [];
        secs.forEach(c => { const r = box(c); if (r.left < 0 || r.top < 0 || r.right > innerWidth + 1 || r.bottom > innerHeight + 1) bad.push(c.className + ' off screen');
          const i = c.querySelector('img'); if (!(i && i.naturalWidth > 0)) bad.push(c.className + ' not loaded'); });
        secs.forEach((a, k) => secs.slice(k + 1).forEach(c => { if (meets(box(a), box(c))) bad.push(a.className + ' overlaps ' + c.className); }));
        const note = document.querySelector('.note');
        if (note && note.offsetParent) {
          const r = box(note); if (r.top < 0 || r.bottom > innerHeight + 1 || note.scrollHeight > note.clientHeight + 1) bad.push('allergy notice cut off');
          secs.forEach(c => { if (meets(r, box(c))) bad.push('allergy notice overlaps ' + c.className); }); }
        return { names: secs.map(c => (c.className.match(/sec-(\w+)/) || [])[1]), bad, note: !!(note && note.offsetParent), orange: secs.every(c => /\/monitor-2\//.test(c.querySelector('img').src)) };
      });
      seen[half] = r.names; seen['note' + half] = r.note;
      const pass = r.names.length >= 4 && !r.bad.length && !errs.length && !r.orange; ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} half ${half} of the menu: ${r.names.join(', ')}${r.bad.length ? ' ' + r.bad.join('; ') : ''}${errs.length ? ' ' + errs.join('; ') : ''}`);
      await p.close();
    }
    const all = ['starters', 'sauces', 'sandwiches', 'burgers', 'doner', 'platters', 'shawarma', 'hotdogs', 'drinks'];
    const both = seen[1].filter(n => seen[2].includes(n)), none = all.filter(n => !seen[1].includes(n) && !seen[2].includes(n));
    const notes = (seen.note1 ? 1 : 0) + (seen.note2 ? 1 : 0);
    const pass = !both.length && !none.length && notes >= 1; ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} the two halves are the whole menu, once, with the allergy notice on ${notes}${both.length ? ', on both: ' + both.join(' ') : ''}${none.length ? ', missing: ' + none.join(' ') : ''}`);
  }
  // The shop TVs' page. (1) Its pictures (the two halves and the whole menu) were made from the menu as it is now.
  {
    const show = JSON.parse(fs.readFileSync(path.join(root, 'tv', 'show.json')));
    const listed = [show.tv1, show.tv2, show.tv1x, show.tv2x, show.all];
    const missing = listed.filter(f => !fs.existsSync(path.join(root, 'tv', f)));
    const stray = fs.readdirSync(path.join(root, 'tv')).filter(f => /\.(jpg|webp)$/.test(f) && !/^awake\./.test(f) && !listed.includes(f));
    const html = fs.readFileSync(path.join(root, 'tv', 'index.html'), 'utf8');
    const stamped = (html.match(tvPage.STAMP) || [''])[0] === `var PAGE = '${tvPage.version(html)}';` && show.page === tvPage.version(html);
    if (!stamped) console.log('❌ TV page version not stamped (run: node tools/tv-page.cjs)');
    ok = ok && stamped;
    const fresh = show.inputs === tvInputs();
    const pass = fresh && !missing.length && !stray.length && ['awake.webm', 'awake.mp4', 'ping.txt'].every(f => fs.existsSync(path.join(root, 'tv', f)));
    ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} TV pictures: ${listed.length}, up to date with the menu ${fresh}${fresh ? '' : ' (run: node tools/tv-stills.cjs)'}${missing.length ? ', missing ' + missing.join(' ') : ''}${stray.length ? ', unused ' + stray.join(' ') : ''}`);
  }
  // (2) Each TV on its own address, then the plain address on the same TV (it remembers), a phone and a laptop
  // on the plain address (the phone menu), a look with ?preview (not remembered), and ?screen=0 (forgets).
  const PHONE = 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36';
  // the shop TVs' own browser, as Netlify's log saw it on 24 Nov 2026
  const SHOP = 'Mozilla/5.0 (Linux; Android 9; t963_ak301 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.87 Safari/537.36';
  const visit = async (ctx, url, wait) => {
    const p = await ctx.newPage(); const errs = [], asked = []; let loads = 0;
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/Content Security Policy|hud/.test(m.text())) errs.push(m.text()); });
    p.on('domcontentloaded', () => loads++); p.on('request', r => asked.push(new URL(r.url()).pathname));
    await p.goto(base + url); await p.waitForTimeout(wait);
    const st = await p.evaluate(() => ({ path: location.pathname, on: (document.querySelector('img.on') || { getAttribute: () => '' }).getAttribute('src'),
      video: !!document.querySelector('video') && !document.querySelector('video').paused, netlify: !!window.__netlifyRan })).catch(() => ({}));
    await p.close();
    return { ...st, errs, loads, asked };
  };
  const tvCase = async (label, ctx, url, want, wait = 6000, loads = 1) => {
    const r = await visit(ctx, url, wait);
    const shows = /\/tv\/tv1x?\./.test(r.on || '') ? 1 : /\/tv\/tv2x?\./.test(r.on || '') ? 2 : /\/tv\/all\./.test(r.on || '') ? 'all' : 0;
    const bad = r.asked.filter(a => /^\/(api|\.netlify\/functions)\//.test(a));
    const pass = want === 'menu' ? r.path === '/menu/' && !r.errs.length
      : shows === want && r.loads === loads && r.video && !r.netlify && !r.errs.length && !bad.length;
    ok = ok && pass;
    console.log(`${pass ? '✅' : '❌'} ${label}: ${want === 'menu' ? 'went to ' + r.path : 'shows monitor ' + shows + ', page loads ' + r.loads + ', keep-awake video playing ' + r.video + ', Netlify script ran ' + r.netlify}${r.errs.length ? ', errors ' + r.errs.join('; ') : ''}${bad.length ? ', asked Netlify ' + bad.join(' ') : ''}`);
  };
  {
    const left = await b.newContext({ viewport: { width: 1920, height: 1080 } }), right = await b.newContext({ viewport: { width: 1920, height: 1080 } });
    await tvCase('left TV /tv1', left, '/tv1', 1);
    await tvCase('right TV /tv2', right, '/tv2', 2);
    { // still: the right TV keeps its one picture
      const p = await right.newPage(); await p.goto(base + '/tv2');
      const first = await p.evaluate(() => new Promise(r => setTimeout(() => r(document.querySelector('img.on')?.getAttribute('src')), 3000)));
      await p.waitForTimeout(20000);
      const then = await p.evaluate(() => document.querySelector('img.on')?.getAttribute('src'));
      const pass = !!first && first === then; ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} right TV stays still: ${first} -> ${then}`);
      await p.close();
    }
    await tvCase('left TV, plain address afterwards', left, '/', 1);
    await tvCase('right TV, plain address afterwards', right, '/', 2);
    await tvCase('right TV lands on the phone menu: back to its page', right, '/menu/', 2);
    await tvCase('right TV told to forget (?screen=0)', right, '/?screen=0', 'menu', 1500);
    await tvCase('right TV after forgetting, plain address', right, '/', 'menu', 1500);
    const laptop = await b.newContext({ viewport: { width: 1440, height: 900 } });
    await tvCase('a laptop, plain address', laptop, '/', 'menu', 1500);
    await tvCase('a laptop looking at /tv2?preview', laptop, '/tv2?preview', 2);
    await tvCase('the same laptop, plain address (not remembered)', laptop, '/', 'menu', 1500);
    const phone = await b.newContext({ viewport: { width: 390, height: 844 }, userAgent: PHONE });
    await tvCase('a phone opening /tv2', phone, '/tv2', 2);
    await tvCase('the same phone, plain address (not remembered)', phone, '/', 'menu', 1500);
    // a shop TV that doesn't know which it is yet: the whole menu on the plain address (never the phone menu),
    // then 2 on its remote makes it the right TV, remembered
    const shop = await b.newContext({ viewport: { width: 1920, height: 1080 }, userAgent: SHOP });
    await tvCase('a shop TV not yet told which it is, plain address', shop, '/', 'all');
    await tvCase('the same shop TV on the phone menu: back to the whole menu', shop, '/menu/', 'all');
    {
      const p = await shop.newPage(); await p.goto(base + '/'); await p.waitForTimeout(3000);
      await p.keyboard.press('2'); await p.waitForTimeout(3000);
      const on = await p.evaluate(() => document.querySelector('img.on')?.getAttribute('src') || '');
      const where = await p.evaluate(() => location.pathname);
      const pass = /\/tv\/tv2x?\./.test(on) && where === '/tv2'; ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} pressing 2 on the shop TV's remote: shows ${on}, address ${where}`);
      await p.close();
    }
    await tvCase('the same shop TV after pressing 2, plain address', shop, '/', 2);
    {
      const p = await shop.newPage(); await p.goto(base + '/'); await p.waitForTimeout(2500);
      await p.keyboard.press('1'); await p.waitForTimeout(3000);
      const on = await p.evaluate(() => document.querySelector('img.on')?.getAttribute('src') || '');
      const pass = /\/tv\/tv1x?\./.test(on); ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} then pressing 1: shows ${on}`);
      await p.close();
    }
    { // a new version of the TV page goes live: an open TV reloads onto it once, and never loops
      const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } }); const p = await ctx.newPage(); let loads = 0;
      p.on('domcontentloaded', () => loads++);
      fakePage = 'newer';
      await p.goto(base + '/tv2'); await p.waitForTimeout(8000);
      const r = await p.evaluate(() => ({ where: location.pathname, on: document.querySelector('img.on')?.getAttribute('src') || '' }));
      fakePage = '';
      const pass = loads === 2 && r.where === '/tv2' && /\/tv\/tv2x?\./.test(r.on); ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} a new TV page goes live: the open TV reloads onto it once (page loads ${loads}), stays ${r.where}, shows ${r.on}`);
      await ctx.close();
    }
    { // no remote: show.json's "screens" gives a shop TV its half by its ID
      const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, userAgent: SHOP }); const p = await ctx.newPage();
      await p.goto(base + '/'); await p.waitForTimeout(2000);
      const tid = await p.evaluate(() => localStorage.getItem('az-screen-id'));
      fakeScreens = { [tid]: 2 }; await p.close();
      const q = await ctx.newPage(); await q.goto(base + '/'); await q.waitForTimeout(3000);
      const r = await q.evaluate(() => ({ on: document.querySelector('img.on')?.getAttribute('src') || '', where: location.pathname }));
      fakeScreens = null;
      const pass = /\/tv\/tv2x?\./.test(r.on) && r.where === '/tv2'; ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} a shop TV given half 2 in show.json by its ID: shows ${r.on}, address ${r.where}`);
      await ctx.close();
    }
    for (const c of [left, right, laptop, phone, shop]) await c.close();
  }
  // The temporary bridge for the TVs still on the 16:16 page (netlify/edge-functions/tv-old.js): each TV told apart by
  // when its request arrives (a drifting straight line) and its clock reading, checked on real requests from Netlify's
  // log of 26-27 Nov; each gets its half and the az_tv cookie; the current page (p=) and other times are left alone.
  {
    const src = fs.readFileSync(path.join(__dirname, '..', 'netlify', 'edge-functions', 'tv-old.js'), 'utf8');
    const fn = (await import('data:text/javascript,' + encodeURIComponent(src))).default;
    const show = JSON.parse(fs.readFileSync(path.join(root, 'tv', 'show.json')));
    const realNow = Date.now, realLog = console.log;
    const ask = async (now, q) => { Date.now = () => now; console.log = () => {};
      try {
        const r = await fn(new Request('https://x/tv/show.json?' + q), { next: async () => new Response(JSON.stringify(show)) });
        return r ? { all: (await r.json()).all, cookie: (r.headers.get('set-cookie') || '').split(';')[0] } : { all: 'untouched', cookie: '' };
      } finally { Date.now = realNow; console.log = realLog; } };
    const want = (now, half) => { const d = new Date(now), mo = d.getUTCMonth() + 1, x = mo === 11 || mo === 12 || (mo === 1 && d.getUTCDate() <= 6);
      return { all: (x && show['tv' + half + 'x']) || show['tv' + half], cookie: 'az_tv=' + half }; };
    const T0 = Date.UTC(2026, 10, 27, 13, 45), in2 = T0 + 2 * 86400000, at2 = in2 - (in2 % 120000) + 93592;   // left's line, 2 days on
    const cases = [
      ['left TV, 27 Nov 13:45', 1795787150009, 't=1795787154341', 1], ['right TV, 27 Nov 13:45', 1795787148915, 't=1795787155241', 2],
      ['left TV, 26 Nov 15:05 (before its clock jumped)', 1795705557823, 't=1795705571111', 1], ['right TV, 26 Nov 15:05', 1795705556965, 't=1795705560719', 2],
      ['left TV in 2 days, clock corrected', at2, 't=' + (at2 + 7777), 1], ['between the two', 1795787149462, 't=1795787150000', 0],
      ['another time', 1795787100000, 't=1795787100000', 0], ['the current page', 1795787150009, 't=1795787154341&p=x', 0]];
    for (const [name, now, q, half] of cases) {
      const got = await ask(now, q), exp = half ? want(now, half) : { all: 'untouched', cookie: '' };
      const pass = got.all === exp.all && got.cookie === exp.cookie; ok = ok && pass;
      console.log(`${pass ? '✅' : '❌'} bridge for the 16:16 page, ${name}: ${got.all}${got.cookie ? ', ' + got.cookie : ''}`);
    }
  }
  const m = await b.newPage({ viewport: { width: 390, height: 844 } }); const merrs = [];
  m.on('pageerror', e => merrs.push(e.message));
  await m.goto(base + '/menu/'); await m.waitForTimeout(800);
  const mm = await m.evaluate(() => ({ imgs: [...document.images].filter(i => i.naturalWidth > 0 || i.loading === 'lazy').length, wide: document.documentElement.scrollWidth > innerWidth }));
  const mpass = mm.imgs === 4 && !mm.wide && !merrs.length; ok = ok && mpass;
  console.log(`${mpass ? '✅' : '❌'} /menu/ 390x844: pages ${mm.imgs}/4, side scroll ${mm.wide}, errors ${merrs.length}`);
  await b.close(); server.close(); process.exit(ok ? 0 : 1);
})();
