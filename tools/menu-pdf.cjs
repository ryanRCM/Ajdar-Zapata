const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + require('path').resolve('menu/menu.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => { const f = pg.querySelector('.foot').getBoundingClientRect().top; const cols = [...pg.querySelectorAll('.col')].map(c => c.getBoundingClientRect().bottom); return [i + 1, Math.round(Math.max(...cols) - f)]; }));
  console.log('overflow px (must be < 0):', JSON.stringify(over));
  await p.pdf({ path: 'menu/Ajdar_Zapata_Menu.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close(); })();
