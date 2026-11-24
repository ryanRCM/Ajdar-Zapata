// Pictures for the shop TVs' page (/tv/, 24 Nov 2026: "make it static"; "the menu in two parts, one on each
// monitor, always fixed"). Takes a 1920x1080 picture of each half of the menu (/monitor-1/?half=1 and ?half=2) and
// writes site/tv/tv1.<hash>.jpg (left TV: items 1-21 and the sauces), site/tv/tv2.<hash>.jpg (right TV: 22-43),
// site/tv/all.<hash>.jpg (the whole menu, for a shop TV not yet told which it is) and site/tv/show.json. Each name carries its picture's fingerprint, so a TV can never show an old copy. Re-run after
// any menu or design change (tools/check.cjs fails until you do):
//   node tools/tv-stills.cjs
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');
const inputsHash = require('./tv-inputs.cjs');
const root = path.join(__dirname, '..', 'site'), out = path.join(root, 'tv');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp' };
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
  for (const half of [1, 2]) await keep(`/monitor-1/?preview&season=none&half=${half}`, `tv${half}`, 3000);
  await keep('/monitor-1/?preview&season=none', 'all', 3000);   // a shop TV not yet told which it is: the whole menu
  // swap the new pictures in, and take away the old ones
  fs.readdirSync(out).filter(f => /\.jpg$/.test(f)).forEach(f => fs.unlinkSync(path.join(out, f)));
  Object.entries(final).forEach(([n, f]) => fs.copyFileSync(path.join(tmp, n + '.jpg'), path.join(out, f)));
  fs.rmSync(tmp, { recursive: true, force: true });
  const files = Object.values(final);
  const show = { v: crypto.createHash('sha1').update(files.join(',')).digest('hex').slice(0, 10), inputs: inputsHash(), tv1: final.tv1, tv2: final.tv2, all: final.all };
  fs.writeFileSync(path.join(out, 'show.json'), JSON.stringify(show) + '\n');
  console.log('site/tv:', files.length, 'pictures, version', show.v);
  await b.close(); server.close();
})();
