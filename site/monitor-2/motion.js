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

  // ── The flame emblem (sections without photos): the same cosine maths as the big flames (flame.js),
  // redrawn 20 times a second, only in the scene that is on screen.
  if (window.Flames) {
    const shape = { x: 0, y: 0, h: 60, w: 36, tilt: 0.04, amp: 0.13, k: 0.9, f: 1.1, ph: 0 };
    let last = 0;
    (function tick(now) {
      requestAnimationFrame(tick);
      if (now - last < 50 || document.hidden) return;
      last = now;
      document.querySelectorAll('.scene.on .mflame').forEach(el => {
        el.setAttribute('d', window.Flames.path(shape, now / 1000, Number(el.dataset.layer)));
      });
    })(0);
  }

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

  // ── The slideshow: one menu section at a time, each held for its data-hold seconds, sliding in from the
  // right as the last one slides away. The food animation beside it switches to that section's scene
  // (data-scene) with a slanted wipe; the old scene keeps its built state ('on') while it exits ('out').
  const slides = [...document.querySelectorAll('.tvslide')];
  const scenes = [...document.querySelectorAll('.scene')];
  const wipe = document.querySelector('.wipe');
  let si = 0, sc = -1, timer = null, timer2 = null, timer3 = null;

  function restart(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }

  function setScene(k) {
    if (k === sc || !scenes[k]) return;
    const cur = scenes[sc];
    sc = k;
    if (cur) { cur.classList.add('out'); restart(wipe, 'go'); }
    scenes[sc].classList.add('on');
    clearTimeout(timer2);
    if (cur) timer2 = setTimeout(() => { cur.classList.remove('on', 'out'); wipe.classList.remove('go'); }, 760);
  }

  // The whole screen changes: a bright band sweeps across, and while it covers the screen the slide, the
  // food scene and the wall's glow all switch to the next section.
  const bigwipe = document.querySelector('.bigwipe'), stage = document.getElementById('stage');
  let started = false;
  function nextSlide(k) {
    if (!started) { started = true; return showSlide(k); }
    restart(bigwipe, 'go');
    setTimeout(() => showSlide(k), 380);
  }

  function showSlide(k) {
    const prev = slides[si];
    if (prev && k !== si) {
      prev.classList.remove('on'); prev.classList.add('gone');
      clearTimeout(timer3); timer3 = setTimeout(() => prev.classList.remove('gone'), 900);
    }
    si = k;
    const s = slides[si];
    s.classList.add('on');
    if (s.dataset.accent) stage.style.setProperty('--wall-hot', s.dataset.accent);
    if (s.dataset.scene !== undefined) setScene(Number(s.dataset.scene));
    clearTimeout(timer);
    timer = setTimeout(() => nextSlide((si + 1) % slides.length), parseFloat(s.dataset.hold || 8) * 1000);
  }

  // Download and prepare everything first (every picture decoded, fonts loaded), then start: smooth from frame one.
  // Never wait longer than 8 seconds, so a slow picture can't keep the screen blank.
  const ready = Promise.all([
    ...[...document.querySelectorAll('#stage img:not([src=""])')].map(img => (img.decode ? img.decode() : Promise.resolve()).catch(() => {})),
    document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve(),
  ]);
  Promise.race([ready, new Promise(r => setTimeout(r, 8000))]).then(() => {
    fit();
    requestAnimationFrame(() => { document.body.classList.add('ready'); nextSlide(0); });
  });

  // A hidden tab pauses animations; on return, restart the current slide and scene cleanly.
  document.addEventListener('visibilitychange', () => {
    clearTimeout(timer); clearTimeout(timer2); clearTimeout(timer3);
    if (document.hidden) return;
    slides.forEach(x => x.classList.remove('on', 'gone'));
    scenes.forEach(x => x.classList.remove('on', 'out'));
    wipe.classList.remove('go');
    sc = -1;
    started = false;
    nextSlide(si);
  });
})();
