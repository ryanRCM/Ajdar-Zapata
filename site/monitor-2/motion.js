// Monitor 2 motion: plays the food reel and seeds the ambient embers.
// Everything is built once at load (no DOM growth); one timer chain drives the reel.
(() => {
  // ── Kinetic type: split each category name into letters, keeping the accent word orange.
  document.querySelectorAll('.word').forEach(w => {
    const text = w.dataset.text, accent = w.dataset.accent || '';
    const start = accent ? text.indexOf(accent) : -1;
    const frag = document.createDocumentFragment();
    [...text].forEach((ch, i) => {
      const el = document.createElement('i');
      el.textContent = ch === ' ' ? ' ' : ch;
      el.style.setProperty('--i', i);
      if (ch === ' ') el.className = 'sp';
      else if (start >= 0 && i >= start && i < start + accent.length) el.className = 'a';
      frag.appendChild(el);
    });
    w.textContent = '';
    w.appendChild(frag);
  });

  // ── Embers: a fixed set per container, each with its own random path baked into custom properties.
  const rnd = (a, b) => a + Math.random() * (b - a);
  document.querySelectorAll('[data-embers]').forEach(box => {
    const n = +box.dataset.embers, rise = box.dataset.rise || '40vh';
    for (let i = 0; i < n; i++) {
      const e = document.createElement('i');
      e.className = 'ember';
      const s = e.style;
      s.setProperty('--x', rnd(8, 88) + '%');
      s.setProperty('--s', rnd(.28, .6) + 'vh');
      s.setProperty('--d', rnd(7, 14) + 's');
      s.setProperty('--delay', -rnd(0, 14) + 's');
      s.setProperty('--o', rnd(.5, .95));
      s.setProperty('--drift', rnd(-1.2, 1.2) + 'vw');
      s.setProperty('--rise', rise);
      box.appendChild(e);
    }
  });

  // ── Flame licks along the bottom of the blank strips on boards one and three.
  const NS = 'http://www.w3.org/2000/svg';
  document.querySelectorAll('.hearth').forEach(h => {
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 200 20');
    svg.setAttribute('preserveAspectRatio', 'none');
    svg.style.height = '48%'; svg.style.top = 'auto';
    // Each lick fades from warm orange at the base to nothing at the tip.
    const id = 'lk' + Math.random().toString(36).slice(2, 7);
    svg.innerHTML = `<defs><linearGradient id="${id}" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f07c1a" stop-opacity=".7"/><stop offset=".55" stop-color="#ffb347" stop-opacity=".35"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></linearGradient></defs>`;
    for (let k = 0; k < 16; k++) {
      const x = 4 + k * 12.3 + rnd(-3, 3), w = rnd(9, 16), t = rnd(1, 12);
      const f = document.createElementNS(NS, 'path');
      f.setAttribute('d', `M${x - w / 2} 20 Q${x - w / 3} ${t + 5} ${x} ${t} Q${x + w / 3} ${t + 5} ${x + w / 2} 20 Z`);
      f.setAttribute('fill', `url(#${id})`);
      f.setAttribute('class', 'lick');
      f.style.setProperty('--d', rnd(.35, .7) + 's');
      f.style.setProperty('--ph', -rnd(0, 1) + 's');
      svg.appendChild(f);
    }
    h.appendChild(svg);
  });

  // ── Fit each category name (and its number line) to the width it has, at any screen size.
  function fit() {
    document.querySelectorAll('.words').forEach(box => {
      const room = box.clientWidth;
      box.querySelectorAll('.word, .meta').forEach(el => {
        el.style.fontSize = '';
        el.style.setProperty('--fit', 1);
        const need = el.scrollWidth;
        if (need > room) el.style.setProperty('--fit', (room / need * 0.97).toFixed(3));
      });
    });
  }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  addEventListener('resize', fit);

  // ── The reel: each scene builds, holds for its data-hold, then a slanted wipe hands over to the next.
  // The old scene keeps its built state ('on') while it exits ('out'), so the food leaves as a whole.
  const scenes = [...document.querySelectorAll('.scene')];
  const wipe = document.querySelector('.wipe');
  const hls = {};
  document.querySelectorAll('.hl').forEach(h => hls[h.dataset.for] = h);
  let i = 0, timer = null, timer2 = null;

  function restart(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }

  function show(scene) {
    scene.classList.add('on');
    const h = hls[scene.dataset.hl];
    if (h) restart(h, 'on');
    timer = setTimeout(next, parseFloat(scene.dataset.hold || 6.4) * 1000);
  }

  function next() {
    const cur = scenes[i];
    i = (i + 1) % scenes.length;
    cur.classList.add('out');
    restart(wipe, 'go');
    show(scenes[i]);
    clearTimeout(timer2);
    timer2 = setTimeout(() => { cur.classList.remove('on', 'out'); wipe.classList.remove('go'); }, 760);
  }

  show(scenes[0]);

  // A hidden tab pauses animations; on return, restart the current scene cleanly.
  document.addEventListener('visibilitychange', () => {
    clearTimeout(timer); clearTimeout(timer2);
    if (document.hidden) return;
    scenes.forEach(s => s.classList.remove('on', 'out'));
    wipe.classList.remove('go');
    show(scenes[i]);
  });
})();
