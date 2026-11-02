// The two shop TVs only ever see their monitor, on any address of ajdarzapata.co.uk (Ryan, 2 Nov 2026:
// "we're going to use this domain for a lot of different things ... make sure these TVs only see this,
// no matter what"). A TV carries a cookie, az_tv=1 or az_tv=2, set by site/screen.js once /api/screen has
// confirmed it is a locked shop TV. Any page it asks for is answered with its monitor page instead.
// Devices without the cookie (phones, laptops, anyone else) are untouched. Pictures, scripts and the
// check-in API are never touched (excludedPath), so this only runs for pages.
export default async (request, context) => {
  const tv = context.cookies.get('az_tv');
  if (tv !== '1' && tv !== '2') return;                         // not a shop TV: carry on as normal
  if (request.method !== 'GET') return;
  if (!(request.headers.get('accept') || '').includes('text/html')) return;
  const url = new URL(request.url);
  const home = `/monitor-${tv}/`;
  if (url.pathname === home || url.pathname === home + 'index.html') return;
  return context.rewrite(home + url.search);                    // same address in the TV's bar, its monitor on screen
};

export const config = {
  path: '/*',
  excludedPath: ['/api/*', '/.netlify/*', '/*.css', '/*.js', '/*.png', '/*.jpg', '/*.jpeg', '/*.webp', '/*.svg', '/*.ico', '/*.json', '/*.txt', '/*.woff2'],
};
