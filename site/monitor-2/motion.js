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

  // ── Flame licks along the bottom of the free space under the drinks: plain elements, so they stay smooth.
  document.querySelectorAll('.hearth').forEach(h => {
    for (let k = 0; k < 14; k++) {
      const f = document.createElement('i');
      f.className = 'lick';
      const w = rnd(5, 9);
      f.style.cssText = `left:${(k + .5) * (100 / 14) - w / 2 + rnd(-1.5, 1.5)}%;width:${w}%;height:${rnd(22, 48)}%;--d:${rnd(.4, .75)}s;--ph:${-rnd(0, 1)}s`;
      h.appendChild(f);
    }
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

  // Download and prepare everything first (every picture decoded, fonts loaded), then start: smooth from frame one.
  // Never wait longer than 8 seconds, so a slow picture can't keep the screen blank.
  const ready = Promise.all([
    ...[...document.querySelectorAll('#stage img:not([src=""])')].map(img => (img.decode ? img.decode() : Promise.resolve()).catch(() => {})),
    document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve(),
  ]);
  Promise.race([ready, new Promise(r => setTimeout(r, 8000))]).then(() => {
    fit();
    requestAnimationFrame(() => { document.body.classList.add('ready'); show(scenes[0]); });
  });

  // A hidden tab pauses animations; on return, restart the current scene cleanly.
  document.addEventListener('visibilitychange', () => {
    clearTimeout(timer); clearTimeout(timer2);
    if (document.hidden) return;
    scenes.forEach(s => s.classList.remove('on', 'out'));
    wipe.classList.remove('go');
    show(scenes[i]);
  });
})();
