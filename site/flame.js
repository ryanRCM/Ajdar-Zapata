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
  // The fire behind the menu: one small canvas, scaled up by the browser, drawn 20 times a second.
  //  - a hot glow along the bottom that breathes
  //  - the cosine flames in three layers (red, orange, white-gold core), added together
  //    like light ('lighter'), so where flames overlap they burn brighter, as real fire does
  //  - sparks: tiny hot specks that shoot up out of the fire, wobble, cool from white to red and die
  //  - fireworks: every few seconds a shell bursts high up into a ring of falling, fading stars
  // Everything sits behind the glass panels, so it never covers a price. opts: { count, height }.
  function canvas(el, opts = {}) {
    const ctx = el.getContext('2d');
    const W = el.width, H = el.height;
    const n = opts.count || 14;
    const fireH = H * (opts.height || 0.35);
    const rnd = (a, b) => a + Math.random() * (b - a);
    const flames = Array.from({ length: n }, (_, i) => ({
      x: (i + 0.5) * W / n + rnd(-W / n / 4, W / n / 4), y: H + 4,
      h: fireH * rnd(0.55, 1), w: (W / n) * rnd(1.2, 1.8),
      tilt: rnd(-0.12, 0.12), amp: rnd(0.08, 0.15), k: rnd(0.7, 1.1), f: rnd(0.6, 1.0), ph: rnd(0, TAU),
    }));
    const lay = [['rgba(140,8,0,.9)', 'rgba(200,24,0,.55)', 'rgba(255,60,0,0)'],
                 ['rgba(210,30,0,.9)', 'rgba(255,100,0,.5)', 'rgba(255,140,0,0)'],
                 ['rgba(255,150,20,.7)', 'rgba(255,190,60,.45)', 'rgba(255,220,120,0)'],
                 ['rgba(255,250,220,.75)', 'rgba(255,230,140,.4)', 'rgba(255,240,200,0)']];
    const grads = lay.map(c => { const g = ctx.createLinearGradient(0, H, 0, H - fireH); g.addColorStop(0, c[0]); g.addColorStop(0.5, c[1]); g.addColorStop(1, c[2]); return g; });
    const glow = ctx.createLinearGradient(0, H, 0, H - fireH * 0.7);
    glow.addColorStop(0, 'rgba(255,120,0,.55)'); glow.addColorStop(1, 'rgba(255,80,0,0)');
    const sparks = [], stars = [];
    const MAX_SPARKS = 36, MAX_STARS = 90;
    let nextShell = performance.now() + 1500, last = 0, on = true;
    function shell(now) {
      const x = rnd(W * 0.08, W * 0.92), y = rnd(H * 0.08, H * 0.4);
      const hue = [[255, 210, 60], [255, 120, 30], [255, 70, 40], [255, 245, 200]][Math.floor(rnd(0, 4))];
      const count = 32;
      for (let k = 0; k < count && stars.length < MAX_STARS; k++) {
        const a = (k / count) * TAU + rnd(-0.05, 0.05), v = rnd(0.9, 1.25) * H * 0.0065;
        stars.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 1, c: hue });
      }
      nextShell = now + rnd(2600, 5200);
    }
    function draw(now) {
      if (!on) return;
      requestAnimationFrame(draw);
      if (now - last < 50) return;            // 20 frames a second: plenty for fire, light on the TVs
      const dt = Math.min(3, (now - last) / 33); last = now;
      const time = now / 1000;
      ctx.globalCompositeOperation = 'source-over';
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      // glow
      ctx.globalAlpha = 0.75 + 0.25 * Math.sin(time * 2.3);
      ctx.fillStyle = glow; ctx.fillRect(0, H - fireH * 0.7, W, fireH * 0.7);
      ctx.globalAlpha = 1;
      // flames
      for (let layer = 1; layer < 4; layer++) {
        ctx.fillStyle = grads[layer];
        ctx.beginPath();
        for (const p of flames) {
          const [L, R] = edges(p, time, Math.min(layer, 2) + (layer === 3 ? 0.6 : 0));
          ctx.moveTo(L[0][0], L[0][1]);
          for (const [x, y] of L) ctx.lineTo(x, y);
          for (let q = R.length - 1; q >= 0; q--) ctx.lineTo(R[q][0], R[q][1]);
          ctx.closePath();
        }
        ctx.fill();
      }
      // sparks out of the fire
      for (let k = 0; k < 2 && sparks.length < MAX_SPARKS; k++)
        if (Math.random() < 0.55) sparks.push({ x: rnd(0, W), y: H - rnd(0, fireH * 0.4), vx: rnd(-0.6, 0.6), vy: -rnd(1.2, 3.2) * H / 400, life: 1, w: rnd(0, TAU) });
      ctx.lineCap = 'round';
      for (let k = sparks.length - 1; k >= 0; k--) {
        const s = sparks[k];
        s.w += 0.25 * dt; s.x += (s.vx + Math.sin(s.w) * 0.35) * dt; s.y += s.vy * dt; s.vy *= 0.995; s.life -= 0.012 * dt;
        if (s.life <= 0 || s.y < 0) { sparks.splice(k, 1); continue; }
        const g = Math.floor(120 + 135 * s.life), b = Math.floor(200 * s.life * s.life);
        ctx.strokeStyle = `rgba(255,${g},${b},${0.9 * s.life})`;
        ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(s.x - s.vx * 2.5, s.y - s.vy * 2.5); ctx.stroke();
      }
      // fireworks
      if (now > nextShell && opts.fireworks !== false) shell(now);
      for (let k = stars.length - 1; k >= 0; k--) {
        const s = stars[k];
        s.x += s.vx * dt; s.y += s.vy * dt; s.vx *= 0.985; s.vy = s.vy * 0.985 + 0.012 * dt; s.life -= 0.011 * dt;
        if (s.life <= 0) { stars.splice(k, 1); continue; }
        const [r, g, b] = s.c;
        ctx.strokeStyle = `rgba(${r},${g},${b},${s.life})`;
        ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(s.x, s.y); ctx.lineTo(s.x - s.vx * 3, s.y - s.vy * 3); ctx.stroke();
      }
    }
    requestAnimationFrame(draw);
    document.addEventListener('visibilitychange', () => { on = !document.hidden; if (on) { last = performance.now(); requestAnimationFrame(draw); } });
  }
  return { path, canvas };
})();
