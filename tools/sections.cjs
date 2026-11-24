// Screenshots each TV menu panel from tools/.sections-N.html (made by tools/make-sections.py) at 2x, see-through.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => { const b = await chromium.launch(); const sizes = {}, heads = {};
  for (const mon of [1, 2]) { const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.resolve(`tools/.sections-${mon}.html`), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    for (const el of await p.$$('.sec')) { const id = await el.getAttribute('id'); const bb = await el.boundingBox();
      const over = await el.evaluate(n => [...n.querySelectorAll('.r,.s,.h,.al')].some(r => r.scrollWidth > r.clientWidth + 1)); if (over) console.log('TOO WIDE:', mon, id);
      await el.screenshot({ path: `site/monitor-${mon}/sec-${id}.png`, omitBackground: true }); sizes[id] = [Math.round(bb.width), Math.round(bb.height)];
      // the empty gap in the heading, as fractions of the panel picture (site/monitor-1/heads.json, used by deco.js)
      if (mon === 1) heads[id] = await el.evaluate(n => { const b = n.getBoundingClientRect(), h = n.querySelector('.h'); if (!h) return null;
        const en = h.children[0].getBoundingClientRect(), fa = h.querySelector('.hf'), hb = h.getBoundingClientRect();
        if (!fa) return null; const f = fa.getBoundingClientRect(), r = v => Math.round(v * 10000) / 10000;
        return [r((en.right - b.left) / b.width), r((f.left - b.left) / b.width), r((hb.top - b.top) / b.height), r((hb.bottom - 4 - b.top) / b.height)]; }); }
    await p.close(); }
  fs.writeFileSync('tools/.sections.json', JSON.stringify(sizes)); fs.writeFileSync('site/monitor-1/heads.json', JSON.stringify(heads) + '\n'); console.log(JSON.stringify(sizes)); await b.close(); })();
