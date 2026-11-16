# Fable · final polish · result · 16 Nov 2026

Branch `claude/new-session-3ammxs`, from `main` (e258124). Draft PR, not merged: Ryan decides when it goes live.
PR #6 (`christmas`, the line-up slide) was not merged, so it is left alone. It will need `python3 tools/build-walls.py`
re-run and its line-up slide checked against the taller screen if it merges after this.

## What changed
1. **Allergy notice off the TVs.** `screen.js` no longer makes `.allergy-bar`, its styles are gone from `screen.css`, `build-walls.py` gives monitor 2 the full height (sections 2.45x-4.19x the boards; Starters and Sauces grew about 9%), heroes and the side column fill the freed space. `check.cjs` now fails if the bar comes back. Still on `/menu/`.
2. **Menu always showcased.** Left TV: the shine band and the Christmas light pass no longer cross its text (rim glow and sparkles stay). Right TV: hero holds 14/11/11/11 s → 12/10/10/10 s; menu holds untouched (11-14 s). Heroes and poster are now 37% of the Christmas loop (was 38%), 27% outside Christmas. `check.cjs` holds it under 40%.
3. **Always working.**
   - `site/sw.js`: offline copy of the pages and pictures. Network first, so online it changes nothing; with the Wi-Fi down a reload shows the last good menu. One copy per address, `/api/` never kept.
   - `screen.js`: one guarded reload (`AZReload`) for the hourly reload and for a thrown script error: it fetches the page first, so a TV never swaps a working menu for the browser's error page, and never loops. The wake lock is asked for again every minute.
   - `motion.js`: watchdog, reloads if the same slide has been up 90 s (longest hold is 22 s).
   - Kept as they were: image retry, deploy reload, TV lock (`screen.mjs`, `tv-lock.js` and the lock code untouched).
   - `HANDOFF.md`: the "Keep the TVs on" checklist.
   - Live `/api/screen?status` (16 Nov): `locked: true`, `locked_monitors: ["1","2"]`, `active: []` (no TV was on when checked). Look again when the shop is open: both should be listed.
4. **Slightly nicer (3 touches of the 5 allowed).**
   - Left TV: each column's height is shared so the text is one size down the column; the Doner/Platters/Hot dogs panels now fill their width and the Sauce list is bigger (was uneven empty space).
   - Right TV: the glint across the section name beside the menu is softer (it showed as a hard white bar).
   - Left TV: no light sweeps at all (same change as job 2).

## Checks
`node tools/check.cjs --shots`: all ✅ (both TVs at 1920x1080 and 1366x768, every slide, loop share, both TVs with the network down, watchdog, phone menu).

`node tools/fps.cjs` (6x CPU slowdown, needs 30+):

| Page | Slide | fps |
|---|---|---|
| monitor 1 | all | 56 |
| monitor 2 | starters | 47 |
| monitor 2 | sauces | 52 |
| monitor 2 | hero-sauce | 48 |
| monitor 2 | hero-sandwich | 55 |
| monitor 2 | hero-burger | 52 |
| monitor 2 | hero-brand | 57 |
| monitor 2 | hotdogs | 56 |

Screenshots (not committed; made by `node tools/check.cjs --shots`): `tools/shot-m1-1920.png`, `tools/shot-m1-1366.png`, `tools/shot-m1-live.png`, `tools/shot-m2-1920.png`, `tools/shot-m2-1366.png`, `tools/shot-m2-<slide>.png` for all 13 slides.

## Not checked
- Nothing was run on the real TVs (Chrome 97): the checks use a current Chromium. The service worker uses only features Chrome 97 has.
- The Santa's Robbery poster has no screenshot in `--shots` (as before).

## Questions for Ryan
1. **TV make and model?** Needed to name the exact power settings.
2. **Poster hold.** The poster's 22 s is the biggest extra. Heroes and poster are 37% of the loop. Want less? Cutting the poster to 15 s gives 34%.
3. **The light pass on the left TV** (Christmas, down the live panel) is off because it crossed the text. Say if you want it back.
