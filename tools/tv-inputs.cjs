// The files the TV pictures (site/tv/*.jpg) are made from. tools/tv-stills.cjs stores a fingerprint of them in
// site/tv/show.json; tools/check.cjs fails if they have changed since, so the TVs never lag behind the menu.
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const site = path.join(__dirname, '..', 'site');
const ROOTS = ['monitor-1', 'monitor-2', 'screen.css', 'show.js', 'xmas.js', 'xmas.css', 'flame.js', 'season.js', 'season.css', 'lite.js', 'marble-yellow.jpg', 'marble-orange.jpg'];
function files(p) {
  const st = fs.statSync(p);
  if (!st.isDirectory()) return [p];
  return fs.readdirSync(p).sort().flatMap(n => files(path.join(p, n)));
}
module.exports = function inputsHash() {
  const h = crypto.createHash('sha1');
  ROOTS.map(r => path.join(site, r)).filter(fs.existsSync).flatMap(files).forEach(f => {
    h.update(path.relative(site, f).split(path.sep).join('/')); h.update(fs.readFileSync(f));
  });
  h.update(fs.readFileSync(path.join(__dirname, 'tv-stills.cjs')));
  return h.digest('hex').slice(0, 12);
};
