// Frame rate on a slow TV: Chromium with the CPU slowed 6x, counting frames for a few seconds per slide.
// Run: node tools/fps.cjs   (the brief: 30+ fps on both monitors)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..', 'site');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/api/screen') { res.writeHead(200, { 'content-type': 'application/json' }); return res.end('{"version":"local"}'); }
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(f).pipe(res);
}).listen(0);
(async () => {
  const base = 'http://localhost:' + server.address().port;
  const b = await chromium.launch();
  const runs = [['/monitor-1/', 'starters']].concat(['starters', 'sauces', 'hero-sauce', 'hero-sandwich', 'hero-burger', 'hero-brand', 'hotdogs'].map(id => ['/monitor-2/', id]));
  for (const [page, id] of runs) {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(base + page + '?preview&slide=' + id); await p.waitForTimeout(2500);
    const cdp = await p.context().newCDPSession(p);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 6 });
    const fps = await p.evaluate(() => new Promise(r => { let n = 0; const t0 = performance.now(); (function f(t) { n++; if (t - t0 < 4000) requestAnimationFrame(f); else r(n / ((t - t0) / 1000)); })(t0); }));
    console.log(`${fps >= 30 ? '✅' : '❌'} ${page} ${id}: ${fps.toFixed(0)} fps`);
    await p.close();
  }
  await b.close(); server.close();
})();
