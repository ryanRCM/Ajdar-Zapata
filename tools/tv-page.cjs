// Stamps the TV page's own version (a fingerprint of site/tv/index.html) into the page and into site/tv/show.json
// ("page"). An open TV page reads show.json every 2 minutes and reloads itself when the versions differ, so a
// change to the page reaches the TVs by itself (Ryan, 24 Nov 2026: "make it refresh automatically").
// Run after any change to site/tv/index.html (tools/tv-stills.cjs runs it too; tools/check.cjs fails until you do):
//   node tools/tv-page.cjs
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const page = path.join(__dirname, '..', 'site', 'tv', 'index.html'), json = path.join(__dirname, '..', 'site', 'tv', 'show.json');
const STAMP = /var PAGE = '[^']*';/;
const version = html => crypto.createHash('sha1').update(html.replace(STAMP, "var PAGE = '';")).digest('hex').slice(0, 10);
module.exports = { version, STAMP };
if (require.main === module) {
  const html = fs.readFileSync(page, 'utf8');
  if (!STAMP.test(html)) throw new Error('no PAGE line in site/tv/index.html');
  const v = version(html);
  fs.writeFileSync(page, html.replace(STAMP, `var PAGE = '${v}';`));
  const show = JSON.parse(fs.readFileSync(json, 'utf8'));
  show.page = v;
  fs.writeFileSync(json, JSON.stringify(show) + '\n');
  console.log('TV page version', v);
}
