// Shared by both monitors: keep the screen on, full screen on tap, hide the pointer,
// show the full allergy notice, retry a failed image, and reload every 10 minutes so menu changes reach the TVs.
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

  // Allergy notice: the full FSA wording (Ryan, 2 Nov 2026), drawn over the short line baked into the boards.
  document.querySelectorAll('.board').forEach(board => {
    const note = document.createElement('div');
    note.className = 'allergy';
    note.innerHTML = '<p lang="en"><b>Food Allergies and Intolerances:</b> Before ordering please speak to our staff about your requirements.</p>'
      + '<p lang="fa" dir="rtl"><b>حساسیت و عدم تحمل غذایی:</b> لطفاً پیش از سفارش، نیازهای خود را با کارکنان ما در میان بگذارید.</p>';
    board.appendChild(note);
  });

  document.querySelectorAll('.board > img').forEach(b => b.addEventListener('error', () => setTimeout(() => { b.src = b.src.split('?')[0] + '?r=' + Date.now(); }, 60000)));

  setTimeout(() => location.reload(), 10 * 60 * 1000);
})();
