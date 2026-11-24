// Pictures for the shop TVs' page (/tv/). Each half of the menu (/monitor-1/?half=1 and ?half=2) becomes one looping
// animated picture (12 s, 8 frames a second): the menu still, the little pictures in the headings coming and going
// (site/monitor-1/deco.js; Mama, 24 Nov 2026: "come and go, play"), and in the Christmas look the lights, snow
// and twinkles. The TVs show it in a plain <img>, so it moves with no code on the TV. Writes, in site/tv/:
// tv1.<hash>.webp, tv2.<hash>.webp (left / right TV, plain), tv1x / tv2x (Christmas look, 1 Nov - 6 Jan),
// all.<hash>.jpg (the whole menu, still, for a shop TV not yet told which it is) and show.json. Each name carries
// its picture's fingerprint, so a TV can never show an old copy. Re-run after any menu or design change
// (tools/check.cjs fails until you do):
//   node tools/tv-stills.cjs
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');
const inputsHash = require('./tv-inputs.cjs');
const root = path.join(__dirname, '..', 'site'), out = path.join(root, 'tv');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.json': 'application/json' };
const T = 12, FPS = 8;   // the loop: every animation on the halves repeats within T seconds (deco.css)
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/api/screen') { res.writeHead(200, { 'content-type': 'application/json' }); return res.end('{}'); }
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(f).pipe(res);
}).listen(0);
// nothing half-way through a transition: hide the wipes, and the left TV's "live" glow (it would stick on one panel)
const STILL = '.word::after,.soon::after,.bigwipe,.slabs,.burst,.wipe,.sweep,.rim-stars,.live-glow,.live-sweep{display:none!important}';
(async () => {
  const base = 'http://localhost:' + server.address().port;
  const b = await chromium.launch();
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'tv-'));
  const final = {};   // temp name -> name with its fingerprint
  const keep = async (url, name, wait) => {
    const t = path.join(tmp, name + '.jpg');
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(base + url); await p.addStyleTag({ content: STILL }); await p.waitForTimeout(wait);
    await p.screenshot({ path: t, type: 'jpeg', quality: 86 });
    await p.close();
    const h = crypto.createHash('sha1').update(fs.readFileSync(t)).digest('hex').slice(0, 10);
    final[name] = `${name}.${h}.jpg`;
  };
  // one looping animated picture per half and look, made side by side
  const anim = async (url, name) => {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(base + url); await p.waitForFunction(() => window.__decoReady === true, null, { timeout: 30000 });
    await p.addStyleTag({ content: STILL });
    // the flames behind the glass stand still (only the little pictures and the Christmas bits move)
    await p.evaluate(() => document.querySelectorAll('canvas').forEach(c => { const i = new Image(); i.src = c.toDataURL(); i.className = c.className; i.style.cssText = c.style.cssText; c.replaceWith(i); }));
    await p.waitForTimeout(400);
    const dir = path.join(tmp, name); fs.mkdirSync(dir);
    for (let i = 0; i < T * FPS; i++) {
      await p.evaluate(t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }), i * 1000 / FPS);
      await p.screenshot({ path: path.join(dir, String(i).padStart(4, '0') + '.png') });
    }
    await p.close();
    const file = path.join(tmp, name + '.webp');
    require('child_process').execFileSync('python3', [path.join(__dirname, 'webp-anim.py'), dir, file, String(FPS)], { stdio: 'ignore' });
    const h = crypto.createHash('sha1').update(fs.readFileSync(file)).digest('hex').slice(0, 10);
    final[name] = `${name}.${h}.webp`;
  };
  await Promise.all([[1, 'none', ''], [2, 'none', ''], [1, 'christmas', 'x'], [2, 'christmas', 'x']]
    .map(([half, look, x]) => anim(`/monitor-1/?preview&season=${look}&half=${half}`, `tv${half}${x}`)));
  await keep('/monitor-1/?preview&season=none', 'all', 3000);   // a shop TV not yet told which it is: the whole menu
  // swap the new pictures in, and take away the old ones
  fs.readdirSync(out).filter(f => /\.(jpg|webp)$/.test(f) && !/^awake\./.test(f)).forEach(f => fs.unlinkSync(path.join(out, f)));
  Object.entries(final).forEach(([n, f]) => fs.copyFileSync(path.join(tmp, f.replace(/\.[0-9a-f]{10}\./, '.')), path.join(out, f)));
  fs.rmSync(tmp, { recursive: true, force: true });
  const files = Object.values(final);
  let screens = {}; try { screens = JSON.parse(fs.readFileSync(path.join(out, 'show.json'))).screens || {}; } catch (e) {}
  const show = { screens, v: crypto.createHash('sha1').update(files.join(',')).digest('hex').slice(0, 10), inputs: inputsHash(), tv1: final.tv1, tv2: final.tv2, tv1x: final.tv1x, tv2x: final.tv2x, all: final.all };
  fs.writeFileSync(path.join(out, 'show.json'), JSON.stringify(show) + '\n');
  require('child_process').execFileSync('node', [path.join(__dirname, 'tv-page.cjs')], { stdio: 'inherit' });   // and the page's version
  console.log('site/tv:', files.length, 'pictures, version', show.v);
  await b.close(); server.close();
})();
