# Fable · final polish: always on, menu first, a touch nicer · Nov 2026

Run this on `ryanRCM/Ajdar-Zapata`. Read `CLAUDE.md` first: every rule there holds. Work on a new branch from `main`,
open a **draft** PR, and stop. Never push to `main` and never merge: Ryan decides when it goes live.

**Keep this small.** We're almost there. This is a tidy-up, not a redesign: one short pass, only the files named below,
no new features beyond the four jobs. If something would take more than that, write it down for Ryan instead of doing it.

## Where it is
- Two TVs in the shop, 1920×1080, running **Chrome 97 on Linux** (so nothing newer than Chrome 97).
- **Monitor 1** = the whole menu at once, always. **Monitor 2** = the cycling show: one menu section at a time, big, plus
  full-screen hero slides (sauces, sandwiches, burgers, brand) and Ryan's Santa's Robbery poster (Christmas season, 22 s).
  The running order and holds are in `site/show.js`.
- PR #6 (branch `christmas`) adds a "line-up" slide (food on wooden crates). If Ryan has merged it, build on it; if not,
  leave it alone.

## The four jobs

### 1. Remove the allergy notice from the TVs
Ryan: "we don't need the food allergens and tolerances; we're going to have it in other places." Take it off the TVs only
(it stays on the phone menu, `site/menu/`).
- `site/screen.js`: stop creating `.allergy-bar`. `site/screen.css`: drop its styles.
- `tools/build-walls.py`: monitor 2's sections no longer stop above a bottom bar (`BOTTOM2`), so give them the full height.
  Re-run `python3 tools/build-walls.py`. Then let the hero slides (`site/monitor-2/hero.css`, `.hero` height) and the side
  column use the freed space.
- `tools/check.cjs`: remove the allergy-bar checks. Keep every other check.
- Update the allergy lines in `CLAUDE.md`.

### 2. The main menu is always showcased
At any moment someone in the shop must be able to read the full menu.
- Monitor 1 shows the complete menu at all times. Nothing may ever cover its text, and no animation may move it.
- On monitor 2, menu sections must stay the main part of the loop. The heroes and poster are extras, so they should take
  well under half the loop's time. Check `site/show.js` and trim if needed. Keep the menu holds at 11–14 s.

### 3. Always working (it runs unattended all day)
Make each TV recover by itself from anything short of being switched off. Do only the cheap, solid wins:
- **Wi-Fi drops:** add a small service worker (Chrome 97 supports one) that caches the monitor pages and their pictures, so
  a reload while offline still shows the last good menu. It must never serve an old copy when online: the TVs already
  reload on each deploy (`site/screen.js`, `/api/screen`), and that must keep working.
- **A stuck show:** a watchdog in `site/monitor-2/motion.js` (or `site/show.js`). If the slide hasn't changed for much
  longer than its hold, or the page throws, reload the page. Keep it to a few lines.
- Keep what is already there: the wake lock, the hourly safety reload, the image retry, and the TV lock (don't touch
  `netlify/functions/screen.mjs`, `netlify/edge-functions/tv-lock.js` or the lock code in `screen.js`).
- In `HANDOFF.md`, add a short "Keep the TVs on" checklist for Ryan:
  - turn off auto power-off, no-signal power-off and the eco sleep timers;
  - set power-on after a power cut;
  - set the browser start page to the monitor address;
  - plug the TVs into the wall.
  - Also ask Ryan for the TVs' make and model: the browser only reports "Linux Chrome 97".
- Check that `/api/screen?status` still lists both TVs once they're on.

### 4. Ever so slightly nicer
At most **five** small visual touches, chosen by looking at `node tools/check.cjs --shots` screenshots of both TVs.
Examples of the size meant: even out a panel's empty space, align a heading, soften a harsh edge, tune a colour or a
shadow. No new slides, no new images, no font changes, no layout overhaul. Keep full-screen light effects subtle (on
the real TVs, bright sweeps show as white stripes).

## Rules (break one and it doesn't ship)
- Never change, retype or invent menu content: prices, names and Persian come only from the boards.
- Animate only `transform` and `opacity`. Keep **30+ fps at 6× CPU slowdown** on both monitors (`node tools/fps.cjs`).
- Chrome 97 safe: no standalone `translate`/`scale`/`rotate`, `:has()`, `color-mix()`, container queries, `@layer`,
  dvh/svh. Prefix masks with `-webkit-`.
- No growing DOM, timers cleaned up (the pages run for days).

## Finish
1. `node tools/check.cjs --shots`: all ✅. Run `node tools/fps.cjs` and record the numbers.
2. Write `prompts/fable-polish-result.md`: what changed (one line each), the fps, the screenshots' paths, and any
   questions for Ryan.
3. Commit with what and why, push your branch, open a draft PR, and stop.
