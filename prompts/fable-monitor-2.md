# Fable brief · Monitor 2 motion · 2 Nov 2026

Paste into a Fable session on `ryanRCM/Ajdar-Zapata`, or run it as written.

---

You are making **Monitor 2** of the Ajdar Zapata TV menu look absolutely amazing. Ajdar Zapata is a sandwich, burger and doner shop at 864 High Road, London N12 9RH. Read `CLAUDE.md` first: its rules hold.

## What exists
- `site/monitor-2/index.html` plays on a horizontal 16:9 TV, full screen, all day. It shows the three portrait menu boards (`/board-1..3.png`, rendered from `menu/Ajdar_Zapata_Boards.pdf`), each a third of the screen at full height, plus motion:
  - a food reel in the empty strip of the middle board (sandwiches, burgers, doner, shawarma, hot dogs)
  - a light sweep
  - a logo glow
- `site/screen.css` and `site/screen.js` are shared with monitor 1. Don't change how monitor 1 looks.
- Look at the current state first: `node tools/check.cjs --shots`, and screenshot the reel.

## The goal
Ryan's words: "make it absolutely amazing… visually, go", "animations, very stylistic", sandwiches and doner. Take the motion from "nice" to "people stop and watch":
- **The food reel is the hero.** Rich, appetising, stylish motion for each category. Examples:
  - a doner spit that really turns, glistens and gets carved
  - a sandwich or burger assembling layer by layer with weight and bounce
  - sizzle, steam, sparks and heat shimmer
  - bold kinetic type for the category names, in the boards' own style
  - transitions between scenes that feel designed, not a fade
- **Ambient life across the screen**, kept subtle so the menu stays easy to read: warm light, embers or flame licks along edges, a gentle shine.
- **Match the boards:**
  - near-black `#121110`, orange `#f07c1a`, cream `#f6efe4`
  - condensed bold uppercase type (Bebas Neue is loaded)
  - Persian beside English
  - street-food energy, not corporate

## Hard limits (break one and it doesn't ship)
1. **Never cover menu text or prices.** Motion lives only in empty space:
   - board two's blank strip, 76.5%–90.6% of its height
   - the other boards' blank strips (board 1: 83.5%–90.6%, board 3: 79.4%–90.6%)
   - the board edges
   - overlays that are see-through and keep every price fully readable at a glance

   Re-measure from the PNGs if you need to.
2. **Never change, redraw or invent menu content.** No new prices, items, claims ("fresh", "halal", "best") or offers. Category names, item number ranges and the Persian names must come from the boards.
3. **Don't touch the logo artwork.** It's the shop's; glow around it is fine.
4. **TV-safe:**
   - smooth on a cheap smart-TV browser: CSS transforms and opacity, canvas if needed, no heavy filters on large areas, no video files
   - nothing over ~1 MB added
   - runs for hours without leaking memory: no growing DOM, and timers are cleaned up
5. **Self-contained:**
   - only Google Fonts may load from outside
   - everything else is inline or in `site/`
   - no libraries unless pinned and vendored into `site/`
6. **Monitor 1 stays still.** `/` and `/monitor-1/` must look exactly as they do now.
7. `node tools/check.cjs` must pass (both monitors, 1920×1080 and 1366×768, no errors, reel moving).

## How to finish
1. Work on branch **`fable/monitor-2`**. **Never push to `main`**: `main` is the live shop.
2. Commit every step with what and why, and push the branch.
3. When it's done, run `node tools/check.cjs --shots` and save 5–6 frames of the reel and one full-screen frame to `tools/` (they're gitignored; mention their paths).
4. Write a short summary at the top of `prompts/fable-monitor-2-result.md`:
   - what you built
   - what each scene does
   - anything you weren't sure about

   Commit and push it.
5. Then send one message to the session that started you, saying the branch is ready to review. It will review the work and put it live.
