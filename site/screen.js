// Shared by both monitors: keep the screen on, full screen on tap, hide the pointer,
// draw the flames, retry a failed image, reload by itself when a new version goes live,
// and make sure each TV shows its own monitor.
(() => {
  let lock = null, cursorTimer = null;
  async function keepAwake() {
    try { if (!lock && navigator.wakeLock) { lock = await navigator.wakeLock.request('screen'); lock.addEventListener('release', () => lock = null); } } catch (e) {}
  }
  document.addEventListener('visibilitychange', () => { if (!document.hidden) keepAwake(); });
  keepAwake();

  document.addEventListener('click', () => {
    try { if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(() => {}); } catch (e) {}
  });

  function wake() { document.body.classList.remove('hide-cursor'); clearTimeout(cursorTimer); cursorTimer = setTimeout(() => document.body.classList.add('hide-cursor'), 3000); }
  document.addEventListener('mousemove', wake); wake();

  // The flames behind the glass (flame.js). No bottom bar: the allergy notice is off the TVs (Ryan, Nov 2026:
  // "we're going to have it in other places"; it stays on the phone menu).
  const stage = document.getElementById('stage');
  if (stage) {
    if (window.Flames) {
      const c = document.createElement('canvas');
      c.className = 'flames'; c.width = 384; c.height = 216; // the whole screen, drawn small and scaled up: light on the TVs
      stage.insertBefore(c, stage.firstChild);
      window.Flames.canvas(c, { count: 14, height: 0.42 });
    }
  }

  document.querySelectorAll('#stage img:not([src=""])').forEach(b => b.addEventListener('error', () => setTimeout(() => { b.src = b.src.split('?')[0] + '?r=' + Date.now(); }, 60000)));

  // Check in with Netlify about once a minute (netlify/functions/screen.mjs). Each TV keeps an ID in its
  // browser; Netlify says which monitor that TV should show, and which deploy is live. If the TV is on
  // the wrong monitor it moves; if a new deploy is live it reloads, so updates reach the TVs untouched.
  // Only the two locked shop TVs stay on the monitors: any other device is sent to the phone menu (/menu/).
  // Re-lock a TV by hand with ?screen=1 or ?screen=2 on the address; look without being moved with ?preview.
  const here = Number(document.body.dataset.monitor) || 0;
  const params = new URLSearchParams(location.search);
  const want = params.get('screen'), preview = params.has('preview');
  let id = '', live = '';
  const loadedAt = Date.now();
  function freshReload(v) {
    const p = new URLSearchParams(location.search);
    p.set('v', v || Date.now().toString(36));
    location.replace(location.pathname + '?' + p);
  }
  // The TV's ID lives in two places (browser storage and a long-lived cookie), so it survives either being cleared.
  const cookie = name => (document.cookie.match('(?:^|; )' + name + '=([^;]*)') || [])[1] || '';
  const setCookie = (name, v) => { document.cookie = name + '=' + v + '; Max-Age=' + (v ? 5 * 365 * 86400 : 0) + '; Path=/; SameSite=Lax; Secure'; };
  try { id = localStorage.getItem('az-screen-id') || ''; } catch (e) {}
  if (!/^[a-z0-9]{8,40}$/i.test(id)) id = cookie('az_id');
  if (!/^[a-z0-9]{8,40}$/i.test(id)) id = Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  try { localStorage.setItem('az-screen-id', id); } catch (e) {}
  setCookie('az_id', id);
  // az_tv=1 or 2 marks a locked shop TV: the edge function (netlify/edge-functions/tv-lock.js) then shows
  // it its monitor on every address of the domain. Cleared again if the TV is no longer locked.
  let lastErr = '';
  addEventListener('error', e => { lastErr = String((e && e.message) || 'error').slice(0, 120) + ' @' + String((e && e.filename) || '').split('/').pop() + ':' + ((e && e.lineno) || 0); });
  async function checkIn() {
    try {
      const q = new URLSearchParams({ id, up: Math.round((Date.now() - loadedAt) / 60000), s: Math.round((Date.now() - loadedAt) / 1000) });
      if (lastErr) { q.set('err', lastErr); lastErr = ''; }
      if (want === '1' || want === '2') q.set('want', want);
      const r = await fetch('/api/screen?' + q, { cache: 'no-store' });
      if (!r.ok) return;
      const j = await r.json();
      if (!preview && (j.monitor === 1 || j.monitor === 2)) { if (cookie('az_tv') !== String(j.monitor)) setCookie('az_tv', String(j.monitor)); }
      if (!preview && j.monitor === 0 && cookie('az_tv')) setCookie('az_tv', '');
      if (!preview && here && (j.monitor === 1 || j.monitor === 2) && j.monitor !== here) { location.replace('/monitor-' + j.monitor + '/'); return; }
      if (!preview && j.monitor === 0) { location.replace('/menu/'); return; }
      // A new version is live: load the page again from a fresh address, so no browser or TV can show an old copy.
      if (j.version) { if (live && j.version !== live) { freshReload(j.version); return; } live = j.version; }
    } catch (e) {}
  }
  setTimeout(checkIn, 1000 + Math.random() * 3000); // a little apart, so two TVs starting together don't collide
  // Diagnostic (Ryan, 17 Nov 2026: "it keeps kicking it out"): two extra check-ins early on, so the logs show how long
  // the page survives on the TV (s = seconds since it opened), and the page's last error, if any.
  setTimeout(checkIn, 15 * 1000); setTimeout(checkIn, 35 * 1000);
  setInterval(checkIn, 60 * 1000);

  // Safety net: a full reload every hour anyway (clears any memory build-up, retries anything that failed).
  setTimeout(() => freshReload(), 60 * 60 * 1000);
})();
