// Christmas, shared by both TVs (Christmas update, 2 Nov 2026): fills every [data-snow] box with drifting
// snow and golden sparkles (built once, no DOM growth), and on the left TV makes the panel of the section
// the right TV is showing glow and sparkle (the running order and clock are in /show.js).
(() => {
  const rnd = (a, b) => a + Math.random() * (b - a);
  document.querySelectorAll('[data-snow]').forEach(box => {
    const n = +box.dataset.snow;
    for (let i = 0; i < n; i++) {
      const e = document.createElement('i'), s = e.style;
      e.className = 'flake' + (Math.random() < .3 ? ' gold' : '');
      s.setProperty('--x', rnd(1, 99) + '%');
      s.setProperty('--s', rnd(.5, 1.2) + 'vh');
      s.setProperty('--d', rnd(11, 20) + 's');
      s.setProperty('--delay', -rnd(0, 20) + 's');
      s.setProperty('--o', rnd(.55, .95));
      s.setProperty('--sway', rnd(-3, 3) + 'vw');
      box.appendChild(e);
    }
    for (let i = 0; i < Math.round(n / 4); i++) {
      const e = document.createElement('i'), s = e.style;
      e.className = 'twinkle';
      s.setProperty('--x', rnd(3, 97) + '%'); s.setProperty('--y', rnd(4, 90) + '%');
      s.setProperty('--s', rnd(1.4, 2.6) + 'vh'); s.setProperty('--d', rnd(2.6, 4.4) + 's'); s.setProperty('--delay', -rnd(0, 4) + 's');
      box.appendChild(e);
    }
  });

  // ── Left TV only: sparkle round the section the right TV is showing.
  if (document.body.dataset.monitor !== '1' || !window.AZShow) return;
  const stage = document.getElementById('stage');
  // a hero slide on the right TV lights up the section it is about
  const SECTION = { 'hero-sauce': 'sauces', 'hero-sandwich': 'sandwiches', 'hero-burger': 'burgers' };
  document.querySelectorAll('.card[class*="sec-"]').forEach(c => {
    const g = document.createElement('i'); g.className = 'live-glow'; c.appendChild(g);
    const w = document.createElement('i'); w.className = 'live-sweep'; c.appendChild(w);
  });
  // one fixed set of rim sparkles, moved to the live panel: corners and down the right-hand rim (the price side)
  const stars = document.createElement('div');
  stars.className = 'rim-stars';
  const SPOTS = [[0, 0], [100, 0], [0, 100], [100, 100], [100, 30], [100, 62], [50, 0], [50, 100]];
  SPOTS.forEach(([x, y], k) => {
    const t = document.createElement('i'); t.className = 'twinkle';
    t.style.cssText = `--x:${x}%;--y:${y}%;--d:${2.4 + (k % 3) * .5}s;--delay:${-k * .45}s`;
    stars.appendChild(t);
  });
  stage.appendChild(stars);
  let live = null;
  function place() {
    if (!live) return;
    const r = live.getBoundingClientRect();
    Object.assign(stars.style, { left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px' });
  }
  window.AZShow.on(slot => {
    const id = SECTION[slot.id] || slot.id;
    const card = document.querySelector('.card.sec-' + id);
    if (card === live) return;
    if (live) live.classList.remove('live');
    live = card;
    stars.classList.toggle('on', !!card);
    if (card) { void card.offsetWidth; card.classList.add('live'); place(); }
  });
  addEventListener('resize', place);
})();
