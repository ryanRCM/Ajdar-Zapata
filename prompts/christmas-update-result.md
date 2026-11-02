# Christmas update · result · 2 Nov 2026

Branch `christmas` (main merged in up to 04251ce: TV lock, swapped monitors, 11-14 s holds, fire and fireworks, real platter/shawarma/sauce photos).
Note the swap: monitor 2 (the cycling show with the heroes) is now on the LEFT TV, monitor 1 (full menu) on the right. **Not live.** Ryan decides when it merges.
Every menu word, number and price still comes from the boards. No new claims, no offers.

## What each slide does (monitor 2, the cycling TV)
Running order, same for both TVs (`site/show.js`, about 2 minutes a loop):
Menu slides hold 11–14 s as on main. starters → sauces → **SAUCES hero** → sandwiches → burgers → **SANDWICHES hero** → doner → platters →
**BURGERS hero** → shawarma → hot dogs → drinks → **AJDAR ZAPATA / MERRY CHRISTMAS hero** → (offers hero, only once Ryan writes offers).

- **Menu slides:** as before (the panel glides in, a band wipe between them, the food reel beside them).
- **Into a hero:** three slanted slabs (red, orange, yellow) sweep across. **Out of a hero:** it punches outwards and a golden ring bursts.
- **SAUCES hero** (13 s): giant "SAUCE SELECTION" smashes in letter by letter. Zapata Special Sauce gets its own wide card: a big
  bottle upside down squeezes a stream into a turning swirl. The other 8 cards each draw a zig-zag of their sauce's colour and drip.
  Every name, English and Persian, is a picture lifted straight off the board PDF at 3x (`tools/build-sauces.py`), so nothing is retyped.
- **SANDWICHES hero** (10 s): slow Ken Burns push-in. Two subs drift behind (parallax). The front sub slides in, a light slash cuts
  it in two, the halves part with steam, crumbs and sauce drips, close again, and a shine runs over the bread. "SANDWICHES", No. 11–15 and the Persian.
- **BURGERS hero** (10 s): the front sub slams down with a squash and settle, a shock ring and sparks. Behind it, a second one turns on
  a glowing turntable. "BURGERS", No. 16–20 and the Persian. (The photos are the same two the reel already uses for burgers.)
- **AJDAR ZAPATA hero** (9 s): the logo (re-cut sharp from the PDF) zooms in, three subs orbit it in front and behind, gold stars twinkle, "MERRY CHRISTMAS".
- **Special offers hero:** built, but hidden. To switch it on, put Ryan's written offers into `OFFERS` in `site/show.js`.
- **Christmas:** snow and gold sparkles drift over each hero slide. Sunburst rays sit behind every hero. Main's fire, sparks and fireworks run behind the glass.
- **Sauce pots:** the real photos of spicy chilli, cheddar and garlic & dill (from main) drop into their cards on the sauce hero.

## Monitor 1 (the full-menu TV)
Stays the calm, complete menu; the text never moves. The panel of the section monitor 2 is showing glows round its rim, a soft
light passes down it once, and gold sparkles twinkle at its corners and down its price-side rim. Both TVs work this out from the
clock (taken from Netlify), so they stay in step without talking to each other. No snow behind its panels: they cover nearly all
the wall, and drawing snow behind them cost a third of the frame rate.

## Checks
- `node tools/check.cjs --shots`: **all ✅** (both monitors at 1920×1080 and 1366×768, heroes never cover the allergy notice,
  every slide shows, monitor 1 sparkles round the right section). Screenshots: `tools/shot-m2-<slide>.png`, `tools/shot-m1-live.png`.
- `node tools/fps.cjs` (Chromium, CPU slowed 6x): this container gave very different numbers from run to run (main's own cycling TV
  read 32 one minute and 19 the next), so I measured main and this branch back to back. See "fps" below.
- New images: about 0.9 MB (sauce names 84 KB, big logo 94 KB, food cut-outs enlarged to 1200–1500 px for the full-screen heroes).

## fps (6x slower CPU, measured alternately against main 04251ce)
Three runs each, alternating main / this branch, same machine, same minutes:

| Screen | main | christmas |
|---|---|---|
| Full-menu TV (monitor 1) | 47 · 52 · 36 | 43 · 39 · 39 ✅ |
| Cycling TV (monitor 2), menu slide | 31 · 26 · 29 | 27 · 26 · 30 |
| SAUCES hero | – | 33 · 30 · 30 |
| AJDAR ZAPATA hero | – | 29 · 36 · 29 |

The cycling TV now runs at main's level (around 30; this container swings a lot between runs). Earlier single runs:
SANDWICHES hero 28, BURGERS hero 30.

What I removed to get there: the turning sunburst (now still), the sauce cards' spotlight pulse, the small travelling bottles, snow on
either TV's wall (main's new fire, sparks and fireworks already fill it; snow stays inside the hero slides); snow and sparkles are drawn on small canvases instead of as dozens of moving dots; everything under a hero stops drawing.

## Chrome 97 (the shop TVs)
Grepped all new CSS/JS: no standalone `translate`/`scale`/`rotate`, `:has()`, `color-mix()`, container queries, `@layer`, `@property`, dvh/svh,
`text-wrap` or logical assignment. Masks carry the `-webkit-` prefix Chrome 97 needs. `aspect-ratio`, `inset` and flex `gap` are all older than 97.

## Not done / second pass
- **Ryan's later asks (relayed after the first version):** realistic rendered sauce pots for the other six sauces, rendered art for
  every section (drinks, fries, doner GDK-style), GDK-style product cards and header bars, bigger name/price type on the full-menu TV.
  Main's drawn pictures (`art-*.png`) fill the reel meanwhile.
- **Sharper menu text on monitor 2.** Main now blows each section up 2.45x to 4.19x from a 1094 px picture, which is soft.
  I had a version that renders the PDF at 3x and makes each picture at exactly the TV's pixel size (crisp), but it clashed with
  main's new layout, so I took main's and left this for a second pass.
- The real TVs have a graphics chip; the headless test does not. Watch the sauce hero on the real TV.

## Questions for Ryan
1. **Special offers:** what are they, exactly as you want them written (English, and Persian if wanted)? The slide stays hidden until then.
2. **"Zorad Mexican"** (you mentioned it with the sauces): what is it? It's not on the board, so it's not on the TVs.
3. **"MERRY CHRISTMAS"** on the logo slide: OK as it is? Want a Persian line under it (send the wording)?
4. **More clean photos** (no watermarks): especially burgers, doner, shawarma, hot dogs, fries. They'd get their own hero slides.
