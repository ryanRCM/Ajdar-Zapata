// Prints the double-sided A4 to send out (menu/a4/Main.dc.html front, Back.dc.html back, made by tools/a4-menu.py)
// to menu/Ajdar_Zapata_A4_Double_Sided.pdf, and checks nothing runs off either page. With "leaflet": the A5 leaflet
// (menu/leaflet/, made by tools/leaflet.py) to menu/Ajdar_Zapata_Leaflet_A5.pdf.
// The artboards load their pictures from Ryan's Design artifacts (/_blob/...); here they are the local files named in
// <dir>/assets.json (the leaflet: logo and photo), or menu/a4/logo.png.
// Fonts: Google Fonts (Barlow Condensed, Barlow, Vazirmatn); where those are blocked (a Claude sandbox), install them
// locally first, as HANDOFF.md says, or the PDF comes out in the wrong fonts.
//   node tools/a4-pdf.cjs            (the A4)
//   node tools/a4-pdf.cjs leaflet    (the A5 leaflet)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const LOGO = /\/_blob\/[0-9a-f]+/g;
const KIND = { a4: { dir: 'menu/a4', out: 'menu/Ajdar_Zapata_A4_Double_Sided.pdf', w: 794, h: 1123, mm: ['210mm', '297mm'], clear: 20 },
  leaflet: { dir: 'menu/leaflet', out: 'menu/Ajdar_Zapata_Leaflet_A5.pdf', w: 559, h: 794, mm: ['148mm', '210mm'], clear: 6 } }[process.argv[2] || 'a4'];
const plain = f => { const s = fs.readFileSync(f, 'utf8');
  const helm = s.match(/<helmet>([\s\S]*?)<\/helmet>/)[1], body = s.match(/<\/helmet>([\s\S]*?)<\/x-dc>/)[1];
  const map = fs.existsSync(`${KIND.dir}/assets.json`) ? JSON.parse(fs.readFileSync(`${KIND.dir}/assets.json`, 'utf8')) : {};
  return `<!doctype html><html><head><meta charset="utf-8">${helm}</head><body>${body.replace(LOGO, m => 'file://' + path.resolve(map[m.split('/').pop()] || 'menu/a4/logo.png'))}</body></html>`; };
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: KIND.w, height: KIND.h } }); const parts = []; let ok = true;
  for (const side of ['Main', 'Back']) {
    const tmp = path.resolve(`tools/.a4-${process.argv[2] || 'a4'}-${side}.html`); fs.writeFileSync(tmp, plain(`${KIND.dir}/${side}.dc.html`));
    await p.goto('file://' + tmp, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
    const gap = await p.evaluate(() => { const r = document.querySelector('.pg'), kids = [...r.children].filter(c => getComputedStyle(c).position !== 'absolute');
      const foot = r.querySelector(':scope > .foot');   // the leaflet's black bar along the bottom: the text must stop above it
      return Math.round((foot || r).getBoundingClientRect()[foot ? 'top' : 'bottom'] - kids[kids.length - 1].getBoundingClientRect().bottom); });
    const fonts = await p.evaluate(() => ['Barlow Condensed', 'Vazirmatn'].map(f => document.fonts.check(`700 14px "${f}"`)));
    console.log(`${gap >= KIND.clear ? '✅' : '❌'} ${side === 'Main' ? 'front' : 'back'}: ${gap}px clear at the bottom (needs ${KIND.clear})${fonts.every(Boolean) ? '' : ' · fonts missing!'}`);
    ok = ok && gap >= KIND.clear;
    const out = path.resolve(`tools/.a4-${process.argv[2] || 'a4'}-${side}.pdf`); await p.pdf({ path: out, width: KIND.mm[0], height: KIND.mm[1], printBackground: true }); parts.push(out); }
  await b.close();
  execFileSync('pdfunite', [...parts, KIND.out]);
  console.log('wrote ' + KIND.out); process.exit(ok ? 0 : 1); })();
