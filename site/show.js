// The show's running order, shared by both TVs (Christmas update, 2 Nov 2026).
// Both TVs work out which slide is on from the clock, so they stay in step without talking to each other:
// the right TV shows the slide, the left TV sparkles round the same section's panel. The clock is taken
// from Netlify (the Date on a tiny request), so a TV whose own clock is off still keeps time.
//
// To add Ryan's special offers: put them in OFFERS exactly as Ryan wrote them, one { en, fa } per offer
// (fa may be ''). While OFFERS is empty the offers slide never shows. Never invent an offer, price or deal.
window.AZShow = (() => {
  const OFFERS = [];

  // [slide id, seconds on screen]. Menu sections (ids as on the boards), then a full-screen hero every
  // two or three menu slides.
  const SLIDES = [   // menu holds as on main (Ryan, 2 Nov 2026: slower, 11-14 s)
    ['starters', 14], ['sauces', 12], ['hero-sauce', 14],
    ['sandwiches', 14], ['burgers', 13], ['hero-sandwich', 11],
    ['doner', 12], ['platters', 11], ['hero-burger', 11],
    ['shawarma', 11], ['hotdogs', 13], ['drinks', 11], ['hero-brand', 11],
  ];
  if (OFFERS.length) SLIDES.push(['hero-offers', 6 + 3 * OFFERS.length]);

  const total = SLIDES.reduce((s, x) => s + x[1], 0) * 1000;
  const starts = []; SLIDES.reduce((t, x) => (starts.push(t), t + x[1] * 1000), 0);
  let offset = 0;   // Netlify's clock minus this device's clock

  // ?slide=<id> on the address starts the show at that slide (for checking one slide; the show runs on from there).
  const want = new URLSearchParams(location.search).get('slide');
  const wi = SLIDES.findIndex(x => x[0] === want);
  let shift = 0;
  if (wi >= 0) shift = ((starts[wi] - (Date.now() % total)) % total + total) % total + 50;

  const now = () => Date.now() + offset + shift;
  function at(t = now()) {
    const p = ((t % total) + total) % total;
    let i = SLIDES.length - 1;
    while (starts[i] > p) i--;
    return { i, id: SLIDES[i][0], hold: SLIDES[i][1], ends: t - p + starts[i] + SLIDES[i][1] * 1000 };
  }

  async function sync() {
    try {
      const t0 = Date.now();
      const r = await fetch('/show.js?clock=' + t0, { method: 'HEAD', cache: 'no-store' });
      const d = Date.parse(r.headers.get('date') || '');
      const t1 = Date.now();
      if (d && t1 - t0 < 3000) {
        const o = d + 500 + (t1 - t0) / 2 - t1;                 // the Date header is whole seconds: aim at the middle
        if (Math.abs(o - offset) > 1500) { offset = o; tick(); }
      }
    } catch (e) {}
  }

  // on(fn): fn(slot, reset) is called now and at every slide change (reset: start the slide afresh, e.g. after
  // the tab was hidden). One timer for the whole show.
  let timer = null, current = null;
  function tick(force) {
    clearTimeout(timer);
    const s = at();
    if (force === 'reset' || !current || s.i !== current.i) { current = s; subs.forEach(f => f(s, force === 'reset')); }
    timer = setTimeout(tick, Math.max(40, s.ends - now() + 20));
  }
  const subs = [];
  function on(fn) { subs.push(fn); if (current) fn(current); else tick(); }
  document.addEventListener('visibilitychange', () => { if (!document.hidden) tick('reset'); });

  sync(); setInterval(sync, 10 * 60 * 1000);
  return { SLIDES, OFFERS, at, on, now, resync: () => tick('reset') };
})();
