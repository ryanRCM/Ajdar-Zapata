# Monitor 2 motion · result · 2 Nov 2026

**Branch `fable/monitor-2`, ready to review. Not on `main`.** Netlify's deploy preview is blocked by its free-plan "unrecognized Git contributor" rule, not by the code. Ryan can approve it in Netlify (see the comment on PR #1). `node tools/check.cjs` passes ✅ on both monitors at 1920×1080 and 1366×768.

## Orange background (Ryan, 2 Nov: "Background ORANGE not black")
- **Monitor 2 now runs on orange.** It uses its own copies of the boards in `site/monitor-2/board-1..3.png`, made by `python3 tools/orange-boards.py` from `site/board-*.png`.
- **The two colours swap, not just the background.** Painting only the background orange would have hidden the orange prices and headings. So the background turns orange and the orange and cream type turns black, by a pure per-pixel recolour.
  - Every word, price and number is still the same pixels in the same place.
  - The logo artwork is unchanged and its black oval now sits on the orange.
  - The orange bars at the top and bottom become black.
- **The motion is re-coloured to suit.**
  - The reel words are black, with the accent word in cream.
  - Each food sits on a black oval badge like the logo's.
  - The wipe is a black slab.
  - The embers are cream, the flame licks deep red, and the logo glow cream.
- **Size:** the three orange boards add about 430 KB in total, saved at 256 colours with dithering. They look the same as the full-colour version.
- **Monitor 1 is still black and untouched.** If Ryan wants it orange too, it would be one line per board in `monitor-1/index.html`.
- **When the menu changes:** re-run `python3 tools/orange-boards.py` after making new boards from a new PDF.

## Allergy notice, full wording (Ryan, 2 Nov: "Allergy notes / Full legal phrase")
- **Both monitors, all three boards** now show the FSA's standard allergen sign wording in the band under the address box, in place of the short "Allergies? Please tell our staff before ordering" line:
  - English: **Food Allergies and Intolerances:** Before ordering please speak to our staff about your requirements.
  - Persian: **حساسیت و عدم تحمل غذایی:** لطفاً پیش از سفارش، نیازهای خود را با کارکنان ما در میان بگذارید.
- **It's live text, not part of the board images.** It is written once in `site/screen.js` and styled in `site/screen.css`, so changing the wording is one edit. It covers only the blank band between the address box and the bottom bar, and fits at both TV sizes.
- **This touches Monitor 1** (screen.css, screen.js and a font link) because the notice belongs on both TVs. Monitor 1 looks the same apart from the notice.
- **Ryan to check the Persian.** I translated it. "حساسیت" matches the boards' own word for allergy.
- The PDF in `menu/` still has the short line, so the next PDF should carry the full wording too.

## What I built
Monitor 2 keeps the three boards' content exactly as it is (now on orange, see above). All motion sits in the blank space around them. A pixel check against the PNGs found zero menu pixels under any motion box, at both screen sizes.

- **The reel** sits in board two's blank strip, 76.8–90.0% of its height. It plays seven scenes, about 46 seconds per loop.
- **The hand-over** between scenes is a slanted orange slab that sweeps across. The old food is shoved out tilted and its letters fly up while the next scene is revealed behind the slab. There is no fade.
- **The type** rises letter by letter in Bebas Neue, with the accent word in orange, then glints. An orange rule draws under it, then the number range and Persian name rise. Long names shrink to fit any screen.
- **The board heading lights up.** While a scene plays, a light runs along that category's orange heading rule on its own board.
- **Ambient life**, all subtle:
  - embers drift up the side gutters of all three boards
  - flame licks and warm light glow in the blank strips of boards one and three
  - a light runs up the two seams between boards
  - a soft orange ring breathes around each logo, with the artwork itself untouched
  - the slow warm sweep across the screen stays, now every 18 seconds

## The scenes
| # | Scene | What happens | Words shown (from the boards) |
|---|---|---|---|
| 1 | Sandwiches | A baguette builds: bread slides in, then lettuce drops, tomato pops, salami flips on, pickles land, sauce draws itself and the top lands with a squash. Steam. | SANDWICHES · NO. 11 – 15 · ساندویچ |
| 2 | Burgers | The bun slides in and the patty slams down with sparks. Cheese lands and drips, then lettuce, tomato and the sesame lid with a squash and bounce. | BURGERS · NO. 16 – 20 · برگر |
| 3 | Doner baguettes | The spit turns beside a flickering burner, with heat glow, gloss and dripping juice. A knife carves down it and shavings fall into a baguette, which fills up. | DONER BAGUETTES · NO. 21 – 24 · دونر باگت |
| 4 | Doner platters | A plate skids in and carved meat rains down and heaps up. Lettuce and tomato pop on, and a shine runs over the meat. | DONER PLATTERS · NO. 25 – 27 · خوراک دونر |
| 5 | Shawarma | A wrap rolls in and a cleaver chops it. The halves split to show the filling, and steam rises. | SHAWARMA · NO. 28 – 30 · شاورما |
| 6 | Hot dogs | The sausage drops in with sparks, mustard and ketchup draw themselves on, and the bun closes. | HOT DOGS · NO. 31 – 35 · هات‌داگ |
| 7 | Starters & sides | A carton slides in, fries shoot up into it one by one, and salt glints. | STARTERS & SIDES · NO. 1 – 10 · پیش‌غذا |

## Checks
- The boards, prices and logo artwork are unchanged. Monitor 1, `screen.css` and `screen.js` are untouched.
- Animation uses only transforms, opacity and clip paths, with no filters, video or libraries. The motion files are 56 KB, and the orange boards about 430 KB.
- Everything is built once at load. Over two full loops the page kept the same element count (515) and the same memory.
- Only Google Fonts loads from outside, as before.
- `tools/check.cjs` changed in one way. It now waits each scene's own hold time before checking that the reel moved, because scenes are longer than the old 3.6 seconds.

## Screenshots (gitignored, in `tools/`)
- `tools/shot-m2-full.png` shows the full screen at 1920×1080.
- `tools/shot-reel-1.png` to `shot-reel-7.png` show each scene once built.
- `tools/shot-reel-3b.png` shows the doner mid-carve.
- `tools/shot-reel-wipe.png` is frozen mid-wipe.
- `tools/shot-m2-1920.png` and `shot-m2-1366.png` come from the check.

## Not sure about
- **The old reel's "DONER · 21–27" is split** into Doner Baguettes (21–24) and Doner Platters (25–27), to match the boards' own headings. It is also on board three, not board two.
- **Starters & sides was added as a seventh scene.** The brief named five categories. Fries are on board one, so it seemed fair, but it can be dropped by deleting one block.
- **The burger, sandwich and platter art is illustrative.** It shows lettuce, tomato, salami, cheese and pickles, which the board descriptions mention. It doesn't claim anything new, but the reviewer should be happy with it.
- **It has not run on a real TV browser.** Everything stays light, but the flame licks are SVG paths. If a cheap TV stutters, reduce them in `motion.js`.
- The blank strip on board three measured 80.0–90.6%, not 79.4% as the brief said, so I used the measured value.
