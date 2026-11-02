# Christmas update · result · 2 Nov 2026

Branch `christmas` (main merged in, including the TV lock 9651e56). **Not live.** Ryan decides when it merges.
Every menu word, number and price still comes from the boards. No new claims, no offers.

## What each slide does (right TV)
Running order, same for both TVs (`site/show.js`, about 2 minutes a loop):
starters → sauces → **SAUCES hero** → sandwiches → burgers → **SANDWICHES hero** → doner → platters →
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
- **Christmas:** light snow and gold sparkles drift behind the glass on the right TV. Sunburst rays sit behind every hero.

## Left TV
Stays the calm, complete menu; the text never moves. The panel of the section the right TV is showing glows round its rim, a soft
light passes down it once, and gold sparkles twinkle at its corners and down its price-side rim. Both TVs work this out from the
clock (taken from Netlify), so they stay in step without talking to each other. No snow on the left TV: its panels cover nearly all
the wall, and drawing snow behind them cost a third of the frame rate.

## Checks
- `node tools/check.cjs --shots`: **all ✅** (both monitors at 1920×1080 and 1366×768, heroes never cover the allergy notice,
  every slide shows, the left TV sparkles round the right section). Screenshots: `tools/shot-m2-<slide>.png`, `tools/shot-m1-live.png`.
- `node tools/fps.cjs` (Chromium, CPU slowed 6x): this container gave very different numbers from run to run (main's own right TV
  read 32 one minute and 19 the next), so I measured main and this branch back to back. See "fps" below.
- New images: about 0.9 MB (sauce names 84 KB, big logo 94 KB, food cut-outs enlarged to 1200–1500 px for the full-screen heroes).

## fps (6x slower CPU, measured alternately against main)
Three runs each, alternating main / this branch, same machine, same minutes:

| Screen | main | christmas |
|---|---|---|
| Left TV | 51 · 50 · 47 | 48 · 41 · 45 ✅ |
| Right TV, menu slide (starters) | 28 · 20 · 23 | 17 · 20 · 21 |
| Right TV, menu slide (hot dogs) | (same) | 17 · 18 · 17 |
| SAUCES hero | – | 21 · 22 · 25 |
| SANDWICHES hero | – | 21 · 24 · 26 |
| BURGERS hero | – | 23 · 28 · 30 |
| AJDAR ZAPATA hero | – | 27 · 21 · 27 |

**Honest read:** in this container even main's right TV is under the brief's 30 fps bar (20–28; it measured 32–34 earlier
in the day, before the machine got busy). The heroes run at main's level; the right TV's menu slides are a few frames slower
than main (the snow behind the glass). If the real TV stutters, first switch off the right TV's snow
(`data-snow` on `.snow` in `site/monitor-2/index.html` → remove the div).

What I removed to get there: the turning sunburst (now still), the sauce cards' spotlight pulse, the small travelling bottles, snow on
the left TV; snow and sparkles are drawn on small canvases instead of as dozens of moving dots; everything under a hero stops drawing.

## Not done / second pass
- **Sharper menu text on the right TV.** Main now blows each section up 2.45x to 4.19x from a 1094 px picture, which is soft.
  I had a version that renders the PDF at 3x and makes each picture at exactly the TV's pixel size (crisp), but it clashed with
  main's new layout, so I took main's and left this for a second pass.
- The real TVs have a graphics chip; the headless test does not. Watch the sauce hero on the real TV.

## Questions for Ryan
1. **Special offers:** what are they, exactly as you want them written (English, and Persian if wanted)? The slide stays hidden until then.
2. **"Zorad Mexican"** (you mentioned it with the sauces): what is it? It's not on the board, so it's not on the TVs.
3. **"MERRY CHRISTMAS"** on the logo slide: OK as it is? Want a Persian line under it (send the wording)?
4. **More clean photos** (no watermarks): especially burgers, doner, shawarma, hot dogs, fries. They'd get their own hero slides.
