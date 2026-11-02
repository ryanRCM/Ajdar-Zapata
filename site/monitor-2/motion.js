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
      if (now - last < 50 || document.hidden || document.getElementById('stage').classList.contains('hero-mode')) return;
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

  // ── Special offers: built once from Ryan's written offers in /show.js (none yet, so the slide never shows).
  const offerList = document.querySelector('.offer-list');
  if (offerList && window.AZShow) window.AZShow.OFFERS.forEach((o, k) => {
    const row = document.createElement('div');
    row.className = 'offer'; row.style.setProperty('--k', k);
    const en = document.createElement('span'); en.className = 'en'; en.textContent = o.en || '';
    const fa = document.createElement('span'); fa.className = 'fa'; fa.textContent = o.fa || ''; fa.lang = 'fa';
    row.append(en, fa); offerList.appendChild(row);
  });

  // ── Sauce names (pictures lifted off the board): all at one size, shrunk only if a long name needs it.
  function sizeSauces() {
    const px = innerHeight / 1080;
    document.querySelectorAll('.sauce').forEach(card => {
      const box = card.querySelector('.names'), en = card.querySelector('.en'), fa = card.querySelector('.fa-img');
      if (!box.clientWidth || !en.naturalWidth) return;
      const want = card.classList.contains('feature') ? 1.3 : .82;
      const s = Math.min(want, box.clientWidth / (en.naturalWidth * px), box.clientWidth / (fa.naturalWidth * px));
      en.style.height = (en.naturalHeight * s / 10.8) + 'vh';
      fa.style.height = (fa.naturalHeight * s / 10.8) + 'vh';
    });
  }
  addEventListener('resize', sizeSauces);

  // ── The show. The running order and timing come from /show.js, which works them out from the clock so the
  // left TV can sparkle round the same section. Menu sections glide in after a bright band sweeps across;
  // a full-screen hero arrives under three sweeping slabs and leaves with a punch-out and a golden burst.
  // The food animation beside a menu section switches to that section's scene (data-scene).
  const slides = new Map([...document.querySelectorAll('#stage [data-id]')].map(el => [el.dataset.id, el]));
  const scenes = [...document.querySelectorAll('.scene')];
  const wipe = document.querySelector('.wipe');
  const bigwipe = document.querySelector('.bigwipe'), slabs = document.querySelector('.slabs'), burst = document.querySelector('.burst');
  const stage = document.getElementById('stage');
  let cur = null, sc = -1, timer = null, timer2 = null, timer3 = null, timer4 = null;
  const isHero = el => el.classList.contains('hero');

  function restart(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }

  function setScene(k) {
    if (k === sc || !scenes[k]) return;
    const old = scenes[sc];
    sc = k;
    if (old) { old.classList.add('out'); restart(wipe, 'go'); }
    scenes[sc].classList.add('on');
    clearTimeout(timer2);
    if (old) timer2 = setTimeout(() => { old.classList.remove('on', 'out'); wipe.classList.remove('go'); }, 760);
  }

  function show(el) {
    el.classList.remove('gone', 'leave');
    el.classList.add('on');
    const hero = isHero(el);
    stage.classList.toggle('hero-mode', hero);
    stage.classList.remove('settled');
    clearTimeout(timer4);
    if (hero) timer4 = setTimeout(() => stage.classList.add('settled'), 700);   // the column has slid away: stop drawing it
    if (hero) sizeSauces();
    if (el.dataset.accent) stage.style.setProperty('--wall-hot', el.dataset.accent);
    if (el.dataset.scene !== undefined) setScene(Number(el.dataset.scene));
  }
  function hide(el) {
    el.classList.remove('on');
    if (!isHero(el)) { el.classList.add('gone'); clearTimeout(timer3); timer3 = setTimeout(() => el.classList.remove('gone'), 900); }
  }

  function go(slot, reset) {
    const next = slides.get(slot.id);
    if (!next) return;
    clearTimeout(timer);
    const prev = cur;
    cur = next;
    if (reset || !prev) {
      slides.forEach(x => x.classList.remove('on', 'gone', 'leave'));
      scenes.forEach(x => x.classList.remove('on', 'out'));
      [wipe, bigwipe, slabs, burst].forEach(x => x.classList.remove('go'));
      sc = -1;
      return show(next);
    }
    if (prev === next) return;
    if (isHero(next)) {                       // slabs sweep across; the hero switches on while they cover the screen
      restart(slabs, 'go');
      timer = setTimeout(() => { hide(prev); show(next); }, 440);
    } else if (isHero(prev)) {                // the hero punches out, a golden ring bursts, the menu glides in
      prev.classList.remove('on'); prev.classList.add('leave');
      restart(burst, 'go');
      show(next);
      timer = setTimeout(() => prev.classList.remove('leave'), 650);
    } else {                                  // menu to menu: a bright band sweeps across
      restart(bigwipe, 'go');
      timer = setTimeout(() => { hide(prev); show(next); }, 380);
    }
  }

  // Download and prepare everything first (every picture decoded, fonts loaded), then start: smooth from frame one.
  // Never wait longer than 8 seconds, so a slow picture can't keep the screen blank.
  const ready = Promise.all([
    ...[...document.querySelectorAll('#stage img:not([src=""])')].map(img => (img.decode ? img.decode() : Promise.resolve()).catch(() => {})),
    document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve(),
  ]);
  Promise.race([ready, new Promise(r => setTimeout(r, 8000))]).then(() => {
    fit();
    requestAnimationFrame(() => {
      document.body.classList.add('ready');
      if (window.AZShow) window.AZShow.on(go);
    });
  });
  // (A hidden tab: /show.js calls go() with reset when the tab is shown again, so the slide starts cleanly.)
})();
