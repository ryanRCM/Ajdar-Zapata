# Christmas update brief · the TVs go all out · 2 Nov 2026

Run this in a fresh session on `ryanRCM/Ajdar-Zapata`. Read `CLAUDE.md` first: every rule there holds.

**Work on branch `christmas` only. Never push to `main` and never merge.** Ryan: "this is going to be the
last big update ... you can't put it live until [I say]". When it's finished and checked, open a draft PR
from `christmas` and tell Ryan it's ready to look at. He decides when it goes live.

## What Ryan wants (his words, 2 Nov)
- "Really go all out with this. This is going to be the first thing at Christmas."
- "Really lean into the whole animation side ... these are real pictures, so really try to animate them
  ... go really crazy." "McDonald's-like visuals moving around live, really cool, really nice. This could
  be the best aspect of our whole store."
- "It's gonna say this special offer, this, that, all the crazy things that we have. And obviously it has
  to be the menu things and sauces. Big lean in on the sauces."
- "Make sure text is all clean ... switch and all that."

## What exists now (look at it first)
- Two TVs side by side, 1920×1080 each. **Left = `site/monitor-1/`**: the whole menu at once, yellow glass
  panels on a yellow marble wall. **Right = `site/monitor-2/`**: a slideshow, one menu section at a time at
  2.4× size, the logo and a food column beside it, a full-screen band wipe between slides, a Coming soon
  slide. Maths flames (`site/flame.js`) rise behind both. Bottom bar on both = allergy notice only.
- Menu sections are lifted straight off Ryan's boards by `tools/build-walls.py` (never retyped).
- Real food photos, cut out: `site/monitor-2/photo-*.webp` (from `menu/photos/` by `tools/cut-photos.py`).
- Run `node tools/check.cjs --shots` and look at the screenshots before changing anything.

## Build this
1. **Hero food motion on the right TV, McDonald's menu-board style, using the real photos.** Each photo
   gets its own choreography, not one shared fade: slam in with a squash and settle; slow push-in
   (Ken Burns) with parallax between layered cut-outs; a sub sliced in two and the halves sliding apart;
   orbiting/rotating turntable; steam, sparks, sauce drips and crumbs as separate light layers on top;
   a shine sweeping across the bread. Big bold kinetic type over it (price-free, see rule 2).
2. **A full-screen "hero" slide between menu slides** (every 2–3 menu slides): one dish or the sauces
   filling the whole right TV, giant type, moving photo, brand colours. Make transitions feel designed
   (wipes, zooms, type smashing in), never a plain fade.
3. **Sauces: a big moment.** A dedicated hero slide for the sauce selection, made with motion: bottles,
   pours, swirls and drips in each sauce's colour, every sauce name big (English + Persian, exactly as on
   the board: Zapata Special Sauce, Garlic, Garlic & Dill, Spicy Chilli, Mushroom, Ketchup, Mayo, Cheddar
   Sauce, Green Sauce). Ryan also said "Zorad Mexican": **ask Ryan what that is** before adding it; it is
   not on the board.
4. **Special offers slide.** Build the slide and its motion, but show it only when Ryan gives the actual
   offers in writing. Until then it stays hidden. **Never invent an offer, price, deal or claim.**
5. **The left TV stays the calm, complete menu** but joins the show: gentle motion only around the
   panels (flames, sparkle on prices when the right TV shows that section), never moving the text.
6. **Christmas touch, tasteful:** light snow or sparkles drifting behind the glass, a festive glint, in
   the brand's yellow, orange, red and cream. Keep it reading as Ajdar Zapata, not a generic card.
7. **Clean text:** check every menu panel at 100% zoom on both TVs. Edges must be crisp, no fuzz or colour
   fringes from the recolouring in `tools/build-walls.py` (tune its thickening and alpha if needed).

## Hard rules (break one and it doesn't ship)
1. **Never change, retype or invent menu content.** Prices, names, numbers and Persian come only from the
   boards. No new claims ("fresh", "best", "halal"), no offers unless Ryan wrote them.
2. **Prices never move or get covered.** Motion lives beside, behind or between menu panels; overlays
   over text must be see-through and brief. `tools/check.cjs` must keep passing (it checks overlaps).
3. **Smooth on the TVs.** Animate only `transform` and `opacity`. No `mix-blend-mode`, no animated
   `filter`/`background-position`, no big blurs, no video files. Pre-decode every image before the show
   starts (motion.js already waits). Measure: Chromium at 6× CPU slowdown must stay at 30+ fps on both
   monitors (the current build is 57 left, 34–49 right). Keep total new images under ~3 MB.
4. **No watermarked photos.** Most photos Ryan sent carry "Snapp! Food" or other sites' marks: don't use
   them. Only the clean ones in `menu/photos/`. More clean photos may come from Ryan.
5. **Allergy notice stays** at the bottom of both TVs. No phone number. Don't touch the TV lock
   (`netlify/functions/screen.mjs`, `netlify/edge-functions/tv-lock.js`, the cookie code in `screen.js`).
6. Runs for hours: no growing DOM, timers cleaned up.

## Finish
- `node tools/check.cjs --shots` all ✅, the fps numbers, and screenshots of each slide type saved to
  `tools/` (gitignored).
- Write `prompts/christmas-update-result.md`: what each slide does, the fps, and open questions for Ryan
  (offers, "Zorad Mexican", more photos).
- Commit with what and why, push `christmas`, open a draft PR, and stop. Don't merge.
