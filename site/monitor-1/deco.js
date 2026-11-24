// The moving bits on the two halves of the menu (see deco.css). Builds, once the panels are laid out: a small
// picture show in the empty middle of each heading (positions from heads.json, made by tools/sections.cjs), and
// in the Christmas season lights, snow caps and twinkles. Sets window.__decoReady when done (tools/tv-stills.cjs
// waits for it). Every animation repeats within T seconds.
(() => {
  const root = document.documentElement;
  if (!root.classList.contains('half-1') && !root.classList.contains('half-2')) return;
  const T = 12;
  // Mama, 24 Nov 2026: "a fire picture, the shawarma picture, the doner picture, a drink, a hot dog, coming and going".
  // Only real photos of what is on the menu (no drink or fries photo yet: the flame).
  const PICS = {
    starters: ['flame'], sauces: ['sauce-garlic-dill', 'sauce-spicy-chilli'],
    sandwiches: ['beef-salami-baguette', 'chicken-salami-baguette', 'mixed-salami-baguette'], burgers: ['beef-patty-sub', 'chicken-fillet-sub'],
    doner: ['doner-meat', 'flame'], platters: ['doner-platter', 'flame'], shawarma: ['shawarma-wraps', 'flame'], hotdogs: ['salami-sub', 'flame'],
    drinks: ['flame'],
  };
  const FRAMED = { 'doner-meat': 1 };
  const stage = document.getElementById('stage');
  const xmas = root.dataset.season === 'christmas';

  // one keyframe rule per number of pictures: each is on for T/k seconds, sliding in and out
  const style = document.createElement('style');
  style.textContent = [2, 3].map(k => {
    const on = 100 / k, edge = 0.5 / T * 100;
    // pops up from the heading line with a little bounce and shrinks away again: it never leaves its gap
    return `@keyframes deco-cyc-${k} { 0% { opacity: 0; transform: scale(.45) rotate(-8deg); } ${edge.toFixed(2)}% { opacity: 1; transform: scale(1.08) rotate(2deg); }
      ${(edge * 1.7).toFixed(2)}% { opacity: 1; transform: none; } ${(on - edge).toFixed(2)}% { opacity: 1; transform: none; }
      ${on.toFixed(2)}% { opacity: 0; transform: scale(.45) rotate(8deg); } 100% { opacity: 0; transform: scale(.45); } }`;
  }).join('\n');
  document.head.appendChild(style);

  function flameSvg() {
    const shape = { x: 0, y: 0, h: 60, w: 36, tilt: 0.04, amp: 0.13, k: 0.9, f: 1.1, ph: 0 };
    const d = l => window.Flames ? window.Flames.path(shape, 0.6, l) : '';
    return `<svg viewBox="-30 -64 60 68"><path fill="#e02010" d="${d(0)}"/><path fill="#ff8a00" d="${d(1)}"/><path fill="#ffd34d" d="${d(2)}"/></svg>`;
  }
  // where a panel's picture really sits inside its card (object-fit: contain)
  function shown(img) {
    const r = img.getBoundingClientRect(), s = Math.min(r.width / img.naturalWidth, r.height / img.naturalHeight);
    const w = img.naturalWidth * s, h = img.naturalHeight * s;
    return { left: r.left + (r.width - w) / 2, top: r.top + (r.height - h) / 2, width: w, height: h };
  }
  const waits = [];
  function build(heads) {
    Object.keys(PICS).forEach(id => {
      const card = document.querySelector('.card.sec-' + id), g = heads[id];
      if (!card || !card.offsetParent || !g) return;
      const b = shown(card.querySelector('img'));
      const x0 = b.left + g[0] * b.width, x1 = b.left + g[1] * b.width, y0 = b.top + g[2] * b.height, y1 = b.top + g[3] * b.height;
      // as tall as the room from the heading line up to just over the panel's top edge (a little into the empty
      // bottom of the panel above, or the screen's top), so it never covers any menu text
      const cr = card.getBoundingClientRect(), gap = innerHeight * 12 / 1080, pad = innerHeight * 0.0148;
      const above = [...document.querySelectorAll('#stage .card')].some(o => o !== card && o.offsetParent && (() => { const r = o.getBoundingClientRect();
        return r.bottom <= cr.top + 1 && r.bottom > cr.top - gap * 3 && r.left < cr.right && cr.left < r.right; })());
      const top = above ? cr.top - gap - pad * 0.5 : Math.max(2, cr.top - gap * 0.8);
      const gw = x1 - x0, hh = y1 - 1 - top;
      const box = document.createElement('div');
      box.className = 'deco';
      Object.assign(box.style, { left: x0 + gw * 0.07 + 'px', width: gw * 0.86 + 'px', top: top + 'px', height: hh + 'px' });
      const list = PICS[id], k = list.length;
      list.forEach((name, i) => {
        const pic = document.createElement('div');
        pic.className = 'pic' + (k === 1 ? ' only' : '');
        if (k > 1) { pic.style.animation = `deco-cyc-${k} ${T}s linear infinite`; pic.style.animationDelay = (i * T / k - T) + 's'; }
        const bob = document.createElement('div'); bob.className = 'bob'; bob.style.animationDelay = (-i * 0.75) + 's';
        if (name === 'flame') bob.innerHTML = flameSvg();
        else {
          const im = new Image(); im.src = '/monitor-2/photo-' + name + '.webp'; if (FRAMED[name]) im.className = 'framed';
          waits.push(im.decode ? im.decode().catch(() => {}) : Promise.resolve()); bob.appendChild(im);
        }
        pic.appendChild(bob); box.appendChild(pic);
      });
      stage.appendChild(box);
    });
    if (xmas) christmas();
    fitNote();
    Promise.all(waits).then(() => { window.__decoReady = true; });
  }

  // the allergy notice: as big as fits its space, never cut
  function fitNote() {
    const n = document.querySelector('.note'); if (!n || !n.offsetParent) return;
    for (let f = 1; f > 0.5; f -= 0.04) { n.style.fontSize = ''; n.querySelectorAll('b, p').forEach(e => e.style.zoom = f); if (n.scrollHeight <= n.clientHeight + 1) break; }
  }

  function christmas() {
    const W = innerWidth, H = innerHeight, NS = 'http://www.w3.org/2000/svg';
    // lights: a wire sagging between hooks along the very top, warm bulbs twinkling in turn
    const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'xmas-lights');
    const hh = H * 0.024, span = W / 8; let d = `M0 ${hh * 0.15}`;
    for (let i = 0; i < 8; i++) d += ` Q${i * span + span / 2} ${hh * 0.85} ${(i + 1) * span} ${hh * 0.15}`;
    svg.innerHTML = `<defs><radialGradient id="glow"><stop offset="0" stop-color="#fff6d0" stop-opacity=".95"/><stop offset="1" stop-color="#ffd24a" stop-opacity="0"/></radialGradient></defs>`
      + `<path d="${d}" fill="none" stroke="#3b2a12" stroke-width="${Math.max(1.5, H * 0.0016)}" opacity=".75"/>`;
    const colors = ['#fff1b8', '#ffcf3a', '#ff8a3d', '#fff1b8', '#ff5a3a'];
    for (let i = 0; i < 8; i++) for (let j = 1; j <= 5; j++) {
      const t = j / 6, x = i * span + span * t, y = hh * 0.15 + (hh * 0.85 - hh * 0.15) * 2 * t * (1 - t) * 2 * 0.5 + hh * 0.18;
      const r = H * 0.0045, c = colors[(i * 5 + j) % colors.length], dl = -((i * 5 + j) % 6) * 0.5;
      svg.innerHTML += `<g class="bulb" style="animation-delay:${dl}s"><circle cx="${x}" cy="${y}" r="${r * 3}" fill="url(#glow)"/><ellipse cx="${x}" cy="${y}" rx="${r * 0.8}" ry="${r}" fill="${c}"/></g>`;
    }
    stage.appendChild(svg);
    // snow on the top edge of every panel, and a twinkle on some corners
    document.querySelectorAll('#stage .card').forEach((card, n) => {
      if (!card.offsetParent) return;
      const r = card.getBoundingClientRect(), h = H * 0.013, s = document.createElementNS(NS, 'svg');
      s.setAttribute('class', 'snowcap'); s.setAttribute('viewBox', `0 0 ${r.width} ${h * 2}`); s.setAttribute('preserveAspectRatio', 'none');
      Object.assign(s.style, { left: r.left + r.width * 0.04 + 'px', width: r.width * 0.92 + 'px', top: r.top - h * 0.55 + 'px', height: h * 2 + 'px' });
      let p = `M0 ${h}`; const bumps = Math.max(4, Math.round(r.width / (H * 0.06)));
      for (let i = 0; i < bumps; i++) { const x0 = r.width * i / bumps, x1 = r.width * (i + 1) / bumps, up = h * (0.35 + 0.45 * ((i * 7 + n * 3) % 5) / 4); p += ` Q${(x0 + x1) / 2} ${h - up} ${x1} ${h}`; }
      p += ` L${r.width} ${h * 1.25} Q${r.width / 2} ${h * 1.55} 0 ${h * 1.25}Z`;
      s.innerHTML = `<path d="${p}" fill="#fffdf6" stroke="rgba(150,180,210,.55)" stroke-width="1"/>`;
      stage.appendChild(s);
      if (n % 2 === 0) {
        const tw = document.createElement('div'); tw.className = 'twinkle';
        tw.innerHTML = '<svg viewBox="-10 -10 20 20" width="100%" height="100%"><path d="M0-10 L2-2 10 0 2 2 0 10-2 2-10 0-2-2Z" fill="#ffd84a"/></svg>';
        Object.assign(tw.style, { left: r.right - r.width * 0.03 + 'px', top: r.top + 'px', animationDelay: -(n % 4) + 's' });
        stage.appendChild(tw);
      }
    });
  }

  const go = () => fetch('/monitor-1/heads.json').then(r => r.json()).then(build).catch(() => { window.__decoReady = true; });
  // wait until the panels' pictures are in (positions need their sizes)
  const imgs = [...document.querySelectorAll('#stage .card > img')];
  Promise.all(imgs.map(i => i.decode ? i.decode().catch(() => {}) : Promise.resolve()))
    .then(() => (document.fonts && document.fonts.ready) || null).then(go);
})();
