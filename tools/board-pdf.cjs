// The TV menu board as a PDF, to send Ryan and Mama to check (Ryan, 26 Nov 2026: "send the menu board too so we can
// make sure"). Takes the two halves exactly as the TVs show them (/monitor-1/?half=1 left TV, ?half=2 right TV, in
// today's season) and writes menu/Ajdar_Zapata_TV_Board.pdf: page 1 both TVs side by side (one menu across the two
// screens), pages 2 and 3 each TV full size.
//   node tools/board-pdf.cjs
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..', 'site'), OUT = path.join(__dirname, '..', 'menu', 'Ajdar_Zapata_TV_Board.pdf');
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(0);
const STILL = '.word::after,.soon::after,.bigwipe,.slabs,.burst,.wipe,.sweep,.rim-stars,.live-glow,.live-sweep{display:none!important}';
(async () => {
  const base = 'http://localhost:' + server.address().port, b = await chromium.launch(), shots = [];
  for (const half of [1, 2]) {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(`${base}/monitor-1/?half=${half}&preview`, { waitUntil: 'networkidle' });
    await p.addStyleTag({ content: STILL }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(3500);
    shots.push('data:image/jpeg;base64,' + (await p.screenshot({ type: 'jpeg', quality: 90 })).toString('base64')); await p.close();
  }
  const cap = 'font:700 30px sans-serif;color:#fff;text-align:center;margin:14px 0 0';
  const html = `<!doctype html><html><head><style>@page{size:1920px 1080px;margin:0}body{margin:0;background:#111}
.pg{width:1920px;height:1080px;overflow:hidden;page-break-after:always;display:flex;align-items:center;justify-content:center}
.pg img{display:block}</style></head><body>
<div class="pg" style="gap:12px"><div><img src="${shots[0]}" style="width:950px"><p style="${cap}">LEFT TV · ajdarzapata.co.uk/tv1</p></div>
<div><img src="${shots[1]}" style="width:950px"><p style="${cap}">RIGHT TV · ajdarzapata.co.uk/tv2</p></div></div>
<div class="pg"><img src="${shots[0]}" style="width:1920px"></div><div class="pg"><img src="${shots[1]}" style="width:1920px"></div></body></html>`;
  const p = await b.newPage(); await p.setContent(html, { waitUntil: 'load' });
  await p.pdf({ path: OUT, width: '1920px', height: '1080px', printBackground: true });
  await b.close(); server.close(); console.log('wrote ' + path.relative(process.cwd(), OUT));
})();
