// Shared by both moving monitor pages: keep the screen on, full screen on tap, hide the pointer,
// draw the flames, retry a failed image, reload once an hour.
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
  if (stage && !window.AZ_LITE) {   // lite mode (/lite.js): no flames
    if (window.Flames) {
      const c = document.createElement('canvas');
      c.className = 'flames'; c.width = 384; c.height = 216; // the whole screen, drawn small and scaled up: light on the TVs
      stage.insertBefore(c, stage.firstChild);
      window.Flames.canvas(c, { count: 14, height: 0.42 });
    }
  }

  document.querySelectorAll('#stage img:not([src=""])').forEach(b => b.addEventListener('error', () => setTimeout(() => { b.src = b.src.split('?')[0] + '?r=' + Date.now(); }, 60000)));

  // A full reload, from a fresh address so no old copy can stick.
  function freshReload(v) {
    const p = new URLSearchParams(location.search);
    p.set('v', v || Date.now().toString(36));
    location.replace(location.pathname + '?' + p);
  }
  // (Until 24 Nov 2026 these pages checked in with a Netlify function that locked the shop TVs. The TVs now use
  // /tv1 and /tv2 (site/tv/index.html), and Netlify is just the host, so these pages are for previews and for
  // making the TV pictures, tools/tv-stills.cjs.)

  // Safety net: a full reload every hour anyway (clears any memory build-up, retries anything that failed).
  setTimeout(() => freshReload(), 60 * 60 * 1000);
})();
