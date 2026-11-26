// Prints the double-sided A4 to send out (menu/a4/Main.dc.html front, Back.dc.html back, made by tools/a4-menu.py)
// to menu/Ajdar_Zapata_A4_Double_Sided.pdf, and checks nothing runs off either page.
// The artboards load their logo from Ryan's Design artifact (/_blob/...); here it is menu/a4/logo.png.
// Fonts: Google Fonts (Barlow Condensed, Barlow, Vazirmatn); where those are blocked (a Claude sandbox), install them
// locally first, as HANDOFF.md says, or the PDF comes out in the wrong fonts.
//   node tools/a4-pdf.cjs
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const LOGO = /\/_blob\/[0-9a-f]+/g;
const plain = f => { const s = fs.readFileSync(f, 'utf8');
  const helm = s.match(/<helmet>([\s\S]*?)<\/helmet>/)[1], body = s.match(/<\/helmet>([\s\S]*?)<\/x-dc>/)[1];
  return `<!doctype html><html><head><meta charset="utf-8">${helm}</head><body>${body.replace(LOGO, 'file://' + path.resolve('menu/a4/logo.png'))}</body></html>`; };
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } }); const parts = []; let ok = true;
  for (const side of ['Main', 'Back']) {
    const tmp = path.resolve(`tools/.a4-${side}.html`); fs.writeFileSync(tmp, plain(`menu/a4/${side}.dc.html`));
    await p.goto('file://' + tmp, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
    const gap = await p.evaluate(() => { const r = document.querySelector('.pg'), kids = [...r.children].filter(c => getComputedStyle(c).position !== 'absolute');
      return Math.round(r.getBoundingClientRect().bottom - kids[kids.length - 1].getBoundingClientRect().bottom); });
    const fonts = await p.evaluate(() => ['Barlow Condensed', 'Vazirmatn'].map(f => document.fonts.check(`700 14px "${f}"`)));
    console.log(`${gap >= 20 ? '✅' : '❌'} ${side === 'Main' ? 'front' : 'back'}: ${gap}px clear at the bottom (needs 20)${fonts.every(Boolean) ? '' : ' · fonts missing!'}`);
    ok = ok && gap >= 20;
    const out = path.resolve(`tools/.a4-${side}.pdf`); await p.pdf({ path: out, width: '210mm', height: '297mm', printBackground: true }); parts.push(out); }
  await b.close();
  execFileSync('pdfunite', [...parts, 'menu/Ajdar_Zapata_A4_Double_Sided.pdf']);
  console.log('wrote menu/Ajdar_Zapata_A4_Double_Sided.pdf'); process.exit(ok ? 0 : 1); })();
