// Screenshots each TV menu panel from tools/.sections-N.html (made by tools/make-sections.py) at 2x, see-through.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => { const b = await chromium.launch(); const sizes = {};
  for (const mon of [1, 2]) { const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.resolve(`tools/.sections-${mon}.html`), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    for (const el of await p.$$('.sec')) { const id = await el.getAttribute('id'); const bb = await el.boundingBox();
      const over = await el.evaluate(n => [...n.querySelectorAll('.r,.s,.h')].some(r => r.scrollWidth > r.clientWidth + 1)); if (over) console.log('TOO WIDE:', mon, id);
      await el.screenshot({ path: `site/monitor-${mon}/sec-${id}.png`, omitBackground: true }); sizes[id] = [Math.round(bb.width), Math.round(bb.height)]; }
    await p.close(); }
  fs.writeFileSync('tools/.sections.json', JSON.stringify(sizes)); console.log(JSON.stringify(sizes)); await b.close(); })();
