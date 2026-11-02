// Shared by both monitors: keep the screen on, full screen on tap, hide the pointer,
// show the full allergy notice, retry a failed image, reload by itself when a new version goes live,
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

  // Allergy notice: the full FSA wording (Ryan, 2 Nov 2026), once per TV, under the address.
  const stage = document.getElementById('stage');
  if (stage) {
    const note = document.createElement('div');
    note.className = 'allergy';
    note.innerHTML = '<p lang="en"><b>Food Allergies and Intolerances:</b> Before ordering please speak to our staff about your requirements.</p>'
      + '<p lang="fa" dir="rtl"><b>حساسیت و عدم تحمل غذایی:</b> لطفاً پیش از سفارش، نیازهای خود را با کارکنان ما در میان بگذارید.</p>';
    stage.appendChild(note);
  }

  document.querySelectorAll('#stage img').forEach(b => b.addEventListener('error', () => setTimeout(() => { b.src = b.src.split('?')[0] + '?r=' + Date.now(); }, 60000)));

  // Check in with Netlify about once a minute (netlify/functions/screen.mjs). Each TV keeps an ID in its
  // browser; Netlify says which monitor that TV should show, and which deploy is live. If the TV is on
  // the wrong monitor it moves; if a new deploy is live it reloads, so updates reach the TVs untouched.
  // Only the two locked shop TVs stay on the monitors: any other device is sent to the phone menu (/menu/).
  // Re-lock a TV by hand with ?screen=1 or ?screen=2 on the address; look without being moved with ?preview.
  const here = Number(document.body.dataset.monitor) || 0;
  const params = new URLSearchParams(location.search);
  const want = params.get('screen'), preview = params.has('preview');
  let id = '', live = '';
  try {
    id = localStorage.getItem('az-screen-id') || '';
    if (!id) { id = Math.random().toString(36).slice(2, 10) + Date.now().toString(36); localStorage.setItem('az-screen-id', id); }
  } catch (e) {}
  async function checkIn() {
    try {
      const q = new URLSearchParams({ id });
      if (want === '1' || want === '2') q.set('want', want);
      const r = await fetch('/api/screen?' + q, { cache: 'no-store' });
      if (!r.ok) return;
      const j = await r.json();
      if (!preview && here && (j.monitor === 1 || j.monitor === 2) && j.monitor !== here) { location.replace('/monitor-' + j.monitor + '/'); return; }
      if (!preview && j.monitor === 0) { location.replace('/menu/'); return; }
      if (j.version) { if (live && j.version !== live) { location.reload(); return; } live = j.version; }
    } catch (e) {}
  }
  setTimeout(checkIn, 1000 + Math.random() * 3000); // a little apart, so two TVs starting together don't collide
  setInterval(checkIn, 60 * 1000);

  // Safety net: a full reload every hour anyway (clears any memory build-up, retries anything that failed).
  setTimeout(() => location.reload(), 60 * 60 * 1000);
})();
