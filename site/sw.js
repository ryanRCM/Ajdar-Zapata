// Service worker for the shop TVs (Nov 2026): if the Wi-Fi drops, a reload still shows the last good menu.
// Network first, always: while the shop is online every page, script and picture comes from Netlify exactly as
// before (so deploys reach the TVs untouched), and a copy is kept. Only when the network fails is the copy
// used. /api/ is never kept. One copy per address (the ?v= and ?r= on reloads is dropped), so nothing piles up.
const CACHE = 'az-tv-1';
const FONTS = ['fonts.googleapis.com', 'fonts.gstatic.com'];
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())
));
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  const own = url.origin === self.location.origin, font = FONTS.includes(url.hostname);
  if (req.method !== 'GET' || !(own || font) || url.pathname.startsWith('/api/') || url.pathname.startsWith('/.netlify/')) return;
  const key = own ? url.origin + url.pathname : req.url;
  e.respondWith(fetch(req).then(res => {
    if (res.ok || (font && res.type === 'opaque')) {
      const copy = res.clone();
      e.waitUntil(caches.open(CACHE).then(c => c.put(key, copy)).catch(() => {}));
    }
    return res;
  }).catch(() => caches.open(CACHE).then(c => c.match(key)).then(hit => hit || Promise.reject(new TypeError('offline')))));
});
