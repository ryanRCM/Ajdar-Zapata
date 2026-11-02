// Flames drawn from maths (Ryan, 2 Nov 2026: "imagine a cosine wave, but thicker, with a little pivot tilt;
// two of them coming together almost like a triangle make a really nice flame").
//
// One flame, from its base (t = 0) to its tip (t = 1), at time τ:
//   centre  c(t) = x0 + tilt·h·t + A·h·t·sin(2π(k·t − f·τ) + φ)        a cosine-family wave that travels up
//                                                                     and swings wider towards the tip
//   width   w(t) = w0 · (1 − t)^0.85 · (1 + 0.18·cos(2π(2k·t − 1.3f·τ) + φ))   a triangle that narrows to
//                                                                     the tip, rippling as it goes
// The left edge is c − w/2, the right edge c + w/2: two waves meeting at the tip. Three layers (deep red,
// orange, golden core) nest inside each other. Everything is drawn on one small canvas at 20 frames a
// second and scaled up by the browser, so it stays light on the TVs.
window.Flames = (() => {
  const TAU = Math.PI * 2;
  function edges(p, time, layer) {
    const L = [], R = [];
    const h = p.h * (1 - layer * 0.18), w0 = p.w * (1 - layer * 0.3);
    for (let i = 0; i <= 24; i++) {
      const t = i / 24;
      const c = p.x + p.tilt * h * t + p.amp * h * t * Math.sin(TAU * (p.k * t - p.f * time) + p.ph + layer * 0.6);
      const w = w0 * Math.pow(1 - t, 0.85) * (1 + 0.18 * Math.cos(TAU * (2 * p.k * t - 1.3 * p.f * time) + p.ph));
      const y = p.y - t * h * (1 + 0.06 * Math.sin(TAU * p.f * time * 0.7 + p.ph));
      L.push([c - w / 2, y]); R.push([c + w / 2, y]);
    }
    return [L, R];
  }
  // A flame as an SVG path (used for small flames inside the food art, e.g. the doner burner).
  function path(p, time, layer = 0) {
    const [L, R] = edges(p, time, layer);
    const pts = L.concat(R.reverse());
    return 'M' + pts.map(([x, y]) => x.toFixed(1) + ' ' + y.toFixed(1)).join('L') + 'Z';
  }
  // A row of flames on a canvas behind the menu. opts: { count, height (0-1 of canvas), colours }.
  function canvas(el, opts = {}) {
    const ctx = el.getContext('2d');
    const W = el.width, H = el.height;
    const n = opts.count || 14;
    const cols = opts.colours || [['rgba(150,10,0,.95)', 'rgba(210,30,0,.7)', 'rgba(255,90,0,0)'],
                                  ['rgba(235,70,0,.95)', 'rgba(255,120,0,.75)', 'rgba(255,170,0,0)'],
                                  ['rgba(255,200,40,.95)', 'rgba(255,230,120,.7)', 'rgba(255,240,180,0)']];
    const rnd = (a, b) => a + Math.random() * (b - a);
    const flames = Array.from({ length: n }, (_, i) => ({
      x: (i + 0.5) * W / n + rnd(-W / n / 4, W / n / 4), y: H + 4,
      h: H * (opts.height || 0.9) * rnd(0.55, 1), w: (W / n) * rnd(1.1, 1.7),
      tilt: rnd(-0.12, 0.12), amp: rnd(0.07, 0.14), k: rnd(0.7, 1.1), f: rnd(0.55, 0.9), ph: rnd(0, TAU),
    }));
    const grads = cols.map(c => { const g = ctx.createLinearGradient(0, H, 0, 0); g.addColorStop(0, c[0]); g.addColorStop(0.55, c[1]); g.addColorStop(1, c[2]); return g; });
    let last = 0, on = true;
    function draw(now) {
      if (!on) return;
      requestAnimationFrame(draw);
      if (now - last < 50) return; // 20 frames a second is plenty for fire, and light on the TVs
      last = now;
      const time = now / 1000;
      ctx.clearRect(0, 0, W, H);
      for (let layer = 0; layer < 3; layer++) {
        ctx.fillStyle = grads[layer];
        ctx.beginPath();
        for (const p of flames) {
          const [L, R] = edges(p, time, layer);
          ctx.moveTo(L[0][0], L[0][1]);
          for (const [x, y] of L) ctx.lineTo(x, y);
          for (let i = R.length - 1; i >= 0; i--) ctx.lineTo(R[i][0], R[i][1]);
          ctx.closePath();
        }
        ctx.fill();
      }
    }
    requestAnimationFrame(draw);
    document.addEventListener('visibilitychange', () => { on = !document.hidden; if (on) requestAnimationFrame(draw); });
  }
  return { path, canvas };
})();
