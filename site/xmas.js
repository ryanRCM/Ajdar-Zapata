// Christmas, shared by both TVs (Christmas update, 2 Nov 2026): light snow and golden sparkles drifting
// behind the glass, in the brand's cream, yellow and orange, and on the left TV a glow and sparkles round the
// panel of the section the right TV is showing (the running order and clock are in /show.js).
// Everything is drawn on small canvases, about 16 frames a second, scaled up by the browser (like the flames in
// /flame.js): dozens of separately moving dots made the TVs composite every panel, which was slow.
(() => {
  const TAU = Math.PI * 2, rnd = (a, b) => a + Math.random() * (b - a);
  const SCALE = 0.25;   // canvas pixels per screen pixel: soft dots don't need more, and it keeps drawing light

  function star(ctx, x, y, r, a) {          // a four-point sparkle
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.beginPath();
    for (let k = 0; k < 8; k++) { const rr = k % 2 ? r * .28 : r, t = k * TAU / 8; ctx.lineTo(Math.cos(t) * rr, Math.sin(t) * rr); }
    ctx.closePath(); ctx.fill(); ctx.restore();
  }

  const layers = [];   // { box, canvas, ctx, draw(t) }
  function sizeOf(L) {
    const w = Math.round(L.box.clientWidth * SCALE), h = Math.round(L.box.clientHeight * SCALE);
    if (w && h && (w !== L.canvas.width || h !== L.canvas.height)) { L.canvas.width = w; L.canvas.height = h; }
    return w && h;
  }

  // ── Snow boxes: [data-snow] = how many flakes; a quarter as many sparkles.
  document.querySelectorAll('[data-snow]').forEach(box => {
    const n = +box.dataset.snow;
    const canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%';
    box.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    const flakes = Array.from({ length: n }, () => ({ x: Math.random(), y: Math.random(), r: rnd(.0022, .005), v: 1 / rnd(11, 20),
      sw: rnd(.005, .02), ph: rnd(0, TAU), o: rnd(.55, .95), gold: Math.random() < .3 }));
    const sparks = Array.from({ length: Math.round(n / 4) }, () => ({ x: rnd(.03, .97), y: rnd(.04, .9), r: rnd(.006, .012), d: rnd(2.6, 4.4), ph: rnd(0, 4) }));
    layers.push({ box, canvas, draw(t) {
      const W = canvas.width, H = canvas.height, u = Math.max(W, H) / 1.78;
      ctx.clearRect(0, 0, W, H);
      for (const f of flakes) {
        const y = ((f.y + t * f.v) % 1.06) - .03, x = f.x + Math.sin(t * .6 + f.ph) * f.sw;
        const fade = Math.min(1, (y + .03) / .1, (1.03 - y) / .1);
        ctx.globalAlpha = Math.max(0, f.o * fade);
        ctx.fillStyle = f.gold ? '#ffd23a' : '#fffaf0';
        ctx.beginPath(); ctx.arc(x * W, y * H, f.r * u, 0, TAU); ctx.fill();
      }
      ctx.fillStyle = '#ffe680';
      for (const s of sparks) {
        const p = ((t + s.ph) % s.d) / s.d, k = Math.max(0, Math.sin(p * Math.PI));   // grow and fade
        if (k < .02) continue;
        ctx.globalAlpha = k; star(ctx, s.x * W, s.y * H, s.r * u * k, p * 1.6);
      }
      ctx.globalAlpha = 1;
    } });
  });

  // ── Left TV only: the section the right TV is showing glows round its rim, a soft light passes down it once,
  // and golden sparkles twinkle at its corners and down its right-hand rim (the price side). Text never moves.
  let live = null, rim = null;
  if (document.body.dataset.monitor === '1' && window.AZShow) {
    const stage = document.getElementById('stage');
    const SECTION = { 'hero-sauce': 'sauces', 'hero-sandwich': 'sandwiches', 'hero-burger': 'burgers' };
    document.querySelectorAll('.card[class*="sec-"]').forEach(c => {
      const g = document.createElement('i'); g.className = 'live-glow'; c.appendChild(g);
      const w = document.createElement('i'); w.className = 'live-sweep'; c.appendChild(w);
    });
    const box = document.createElement('div');
    box.className = 'rim-stars';
    const canvas = document.createElement('canvas');
    canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%';
    box.appendChild(canvas); stage.appendChild(box);
    const ctx = canvas.getContext('2d');
    const SPOTS = [[0, 0], [1, 0], [0, 1], [1, 1], [1, .3], [1, .62], [.5, 0], [.5, 1]];
    const M = .04;   // the box reaches a little past the panel, so corner sparkles aren't cut off
    rim = { box, canvas, draw(t) {
      const W = canvas.width, H = canvas.height, u = Math.min(W, H);
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#ffd84a';
      SPOTS.forEach(([x, y], k) => {
        const d = 2.4 + (k % 3) * .5, p = ((t + k * .45) % d) / d, s = Math.max(0, Math.sin(p * Math.PI));
        if (s < .02) return;
        ctx.globalAlpha = s;
        star(ctx, (M + x * (1 - 2 * M)) * W, (M + y * (1 - 2 * M)) * H, u * .06 * s + 2, p * 1.6);
      });
      ctx.globalAlpha = 1;
    } };
    function place() {
      if (!live) return;
      const r = live.getBoundingClientRect(), mx = r.width * M / (1 - 2 * M), my = r.height * M / (1 - 2 * M);
      Object.assign(box.style, { left: r.left - mx + 'px', top: r.top - my + 'px', width: r.width + 2 * mx + 'px', height: r.height + 2 * my + 'px' });
      const w = Math.round((r.width + 2 * mx) * .5), h = Math.round((r.height + 2 * my) * .5);
      if (w !== canvas.width || h !== canvas.height) { canvas.width = w; canvas.height = h; }
    }
    window.AZShow.on(slot => {
      const card = document.querySelector('.card.sec-' + (SECTION[slot.id] || slot.id));
      if (card === live) return;
      if (live) live.classList.remove('live');
      live = card;
      box.classList.toggle('on', !!card);
      if (card) { void card.offsetWidth; card.classList.add('live'); place(); }
    });
    addEventListener('resize', place);
  }

  // ── One loop for every canvas: about 16 frames a second (snow drifts slowly), only boxes that are on screen.
  let last = 0;
  (function loop(now) {
    requestAnimationFrame(loop);
    if (now - last < 60 || document.hidden) return;
    last = now;
    const t = now / 1000;
    for (const L of layers) if (L.box.offsetParent && sizeOf(L)) L.draw(t);
    if (rim && live) rim.draw(t);
  })(0);
})();
