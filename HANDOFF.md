# Ajdar Zapata · handoff · 27 Nov 2026 (TV layout, orange leaflet and A4, TVs locked to their halves)

*Start with `CLAUDE.md`. Separate from LAIFE.* Ryan, 26 Nov 2026: "a finalized handoff so we don't lose this", "no more mix-ups".

## The one rule
**`tools/make-menu.py` on `main` is the only true menu.** Every change goes into it first, then into all three outputs below, in the same push. Never work from an old artifact, PDF or picture: the "Ajdar Zapata Screens" artifact (board-1..3) and `menu/Ajdar_Zapata_Boards*.pdf`, `Full_Menu_A4.pdf`, `Takeaway_Flyer_A5.pdf`, `Three_TV_Boards.pdf`, `Vertical_Menu_Boards.pdf` are OLD (Cheddar, Green Sauce, Pepsi, Corn Balls, old prices): reference only.

## The outputs (all from the one list)
| Output | What | How it's made |
|---|---|---|
| **TV board** (the shop's two TVs) | One menu across both TVs: ajdarzapata.co.uk/tv1 (left: Starters over Sandwiches, Burgers over Doner) and /tv2 (right: Platters, Shawarma, Hot Dogs in a wide column; Sauces, Drinks and the allergy notice small in a side column). To check it as a PDF: `node tools/board-pdf.cjs` → `menu/Ajdar_Zapata_TV_Board.pdf` | `python3 tools/make-sections.py && node tools/sections.cjs && python3 tools/make-sections.py layout`, then `node tools/tv-stills.cjs`, `node tools/check.cjs`, push to `main` |
| **A4 to send out** (double-sided, orange with black ink: the leaflet's palette, 27 Nov) | `menu/Ajdar_Zapata_A4_Double_Sided.pdf` (27 Nov) · artifact "Ajdar Zapata A4 Menu" https://claude.ai/artifact/Lip9yS3R3pBajm6cpGiJEK | `python3 tools/a4-menu.py` → `menu/a4/Main.dc.html` (front), `Back.dc.html` (back); `node tools/a4-pdf.cjs` → the PDF; publish both artboards to that artifact |
| **Leaflet** (A5, double-sided, orange; Ryan 26 Nov: menu without ingredients, address and phone, no allergy notice, the offer at the bottom; 27 Nov: his own layout, orange) | `menu/Ajdar_Zapata_Leaflet_A5.pdf` · artifact "Ajdar Zapata Leaflet" https://claude.ai/artifact/89Tw2CpFz5xUPwB4HESdyz | `python3 tools/leaflet.py` → `menu/leaflet/Main.dc.html` (front), `Back.dc.html` (back); `node tools/a4-pdf.cjs leaflet` → the PDF; publish both artboards to that artifact. The offer box: `OFFER` in `tools/leaflet.py` (Ryan's words from the shop's offer stand; empty = a box asking for it) |
| **Chef sheet** (A3 landscape, one side, for the kitchen: Persian only, black on white, the board's numbers, Persian names, sizes and ingredients, sauces, drinks; no prices; Ryan 27 Nov) | `menu/Ajdar_Zapata_Chef_Sheet_A3.pdf` · artifact "Ajdar Zapata Chef Sheet" https://claude.ai/artifact/Q4nFQ1S6tyxzziRunRyB3a | `python3 tools/chef-sheet.py` → `menu/chef/Main.dc.html`; `node tools/a4-pdf.cjs chef` → the PDF; publish to that artifact |
| **Phone menu** (/menu/ for everyone else) | `menu/Ajdar_Zapata_Menu.pdf`, 4 orange pages | `python3 tools/make-menu.py && node tools/menu-pdf.cjs && pdftoppm -png -r 130 menu/Ajdar_Zapata_Menu.pdf site/menu/page` |

## Ryan's decisions, 26 Nov 2026 (all in the list, all three outputs)
- 32 Hot Dog **£9.50** (was £8.50).
- English "Meat" is **Lamb**: 22 Lamb Doner, 26 Lamb Doner Platter, 29 Lamb Shawarma, and "lamb doner / lamb shawarma" in 22, 24, 25, 26, 28, 29, 31, 34. Persian stays گوشت ("it's fine").
- 6 Zapata Loaded Fries: chips, cheese, olives, **mushroom** & beef salami.
- 19 is **Zapata Fillet Chicken Burger** (Persian فیله برگر مرغ زاپاتا, Claude's, for Mama to check).
- **No NEW or HOUSE SIGNATURE tags** anywhere.
- **Sauces, exactly**: Zapata Special Sauce (added back 15:38, first), Garlic, Garlic & Dill, Spicy Chilli, Ketchup, Mayo, BBQ (Ryan's photo). No Mushroom sauce. BBQ Persian سس باربیکیو is Claude's, for Mama to check.
- **41 is just Ayran (دوغ), £2.00** (15:38; was "Ayran · Sparkling or still" £1.99).
- Pickle sauce stays where it was: 14, 15, 21, 33, 34, 35.
- **TVs show English ingredients on every item that has them** (6, 8, 10, 11-36; not 1-5, 7 or drinks, which have none). Persian ingredients only on the A4 and phone menu: on the TVs they would halve the size of the whole board (text scale 0.50 instead of 0.71). To show them anyway: `DESC_FA = True` in `tools/make-sections.py`.
- **Phone: 020 8259 4026 only** on printed menus (not 07773 001111). The TVs show no phone number.
- **Allergy notice: exactly the Food Standards Agency sign in the shop** (Ryan, 15:39, with a photo of it: "exactly this"): "Food Allergy or Intolerance? If you have a food allergy, intolerance, or coeliac disease – please speak to the staff about the ingredients in your food and drink before you order. Thank you." English, then the Persian of the same words, on the A4, the TVs and the phone menu (last on the page; on the TVs under Sauces). `menu-check.py` checks all three. (Earlier that day a longer 14-allergens text was used for a few hours; Ryan replaced it with the sign.)
- A4 layout (orange with black ink since 27 Nov): front = Starters, Sandwiches, Burgers, Doner Baguettes; back = Platters, Shawarma, Hot Dogs, then Sauces and Drinks, then address and phone, then the allergy notice. Ingredients in English and Persian. Ryan rejected the TVs' yellow look for the A4.

## Ryan's decisions, 27 Nov 2026
- **TVs: always one menu split across the two monitors.** Left TV: Starters over Sandwiches | Burgers over Doner Baguettes. Right TV: Platters, Shawarma, Hot Dogs in one wide column | **Sauces and Drinks smaller, to the side** (a narrow column), the allergy notice under them. Both TVs at one text size (0.766; was 0.72), so they read as one board. `HALVES`, `SIDE`, `WIDTH` in `tools/make-sections.py`.
- **Leaflet: Ryan's own version** (his PDF of 27 Nov: logo, GRAND OPENING, the food photo, "Food images are illustrative."; back: the wraps, CHICKEN SHAWARMA £5.99 from the list, "Visit Ajdar Zapata" bar) **with an orange background**. The photo is his (`menu/leaflet/photo.jpg`, the wraps cut from it `photo-wraps.jpg`). The loyalty card stays at the bottom of the back (his version didn't have it; he asked for it on 26 Nov).
- **Chef sheet for the kitchen** (15:34): "a chef's menu version ... with the numbers as shown on the menu board ... very plain white background ... A3, one sheet ... the back of the fridge ... only Persian with the numbers, the name, the ingredients ... black on white", and "make sure it is the exact same ... all synced ... not making up anything". Built from the list by `tools/chef-sheet.py`, word for word; `tools/menu-check.py` checks it like the other outputs. No prices (kitchen), Fries' M / L from the list. Kitchen-sheet practice: number, name, what goes in, black on white, laminated; type sized for reading at 1-2 m (ingredients 13 pt, names 17 pt).
- **A4: the same palette** ("the actual menu give it same colour palette"): orange page, black ink, black heading bars and number tags. One palette file: `tools/print_palette.py`. Words unchanged.

## Mama's sheet, 26 Nov 2026 15:17 (two handwritten pages, read out by Ryan; live the same afternoon)
- 3 Fries: **M £2.99 / L £4.99** (was one size £2.99).
- 14 Royal Zapata Sandwich and 15 Giant Ajdar Zapata: **+ tomato**.
- 18 Chicken Fillet Burger **£7.50** (was £9.50); 19 Zapata Fillet Chicken Burger **£9.50** (was Claude's placeholder £11.50).
- 22-25 doner baguettes: **+ lettuce**. 24 Mixed Doner **£12.50** (was £17.50); 25 Giant Zapata Doner **£17.50** (was £12.50), **+ cheese, + red cabbage**.
- Platters 26-28: **one size, "with chips & salad"** (M/L gone): 26 **£10.50**, 27 **£9.50**, 28 **£10.50**.
- Shawarma 29 **£6.99**, 30 **£5.99**, 31 **£6.99**; "with garlic **and** chilli sauce" (was "or").
- **No placeholder prices left**: every price is Mama's.
- 16:04 (Ryan): **24 Mixed Doner £11.50** (Mama's sheet had £12.50).
- 16:05: the leaflet's offer is **the shop's loyalty card, word for word** (Ryan's photo): "LOYALTY CARD · DAILY REWARDS / £10 = 1 STAMP · £20+ = 2 STAMPS · ONE ORDER PER DAY / 5 STAMPS · 1 FREE SHAWARMA" (`OFFER` in `tools/leaflet.py`).

## The menu on 26 Nov 2026, after Mama's sheet (snapshot; if this and `tools/make-menu.py` ever differ, the list wins)
- **Starters & Sides**: 1 Chicken Wings · 5 pcs £5.49 · 2 Chicken Wings · 8 pcs £7.99 · 3 Fries M £2.99 / L £4.99 · 4 Cheesy Fries £3.99 · 5 Peri Peri Fries £3.49 · 6 Zapata Loaded Fries £7.99 · 7 Chicken Nuggets £4.99 · 8 Mexican Corn Cup £8.99 · 10 Coleslaw £3.99
- **Sandwiches**: 11 Beef Salami Sandwich £13.00 · 12 Chicken Salami Sandwich £12.00 · 13 Mixed Salami Sandwich £12.50 · 14 Royal Zapata Sandwich £21.50 · 15 Giant Ajdar Zapata £22.50
- **Burgers**: 16 Classic Burger £9.50 · 17 Double Cheeseburger £11.50 · 18 Chicken Fillet Burger £7.50 · 19 Zapata Fillet Chicken Burger £9.50 · 20 Royal Zapata Burger £13.50 · 21 Giant Zapata Burger £18.50
- **Doner Baguettes**: 22 Lamb Doner £11.50 · 23 Chicken Doner £10.50 · 24 Mixed Doner £11.50 · 25 Giant Zapata Doner £17.50
- **Doner Platters**: 26 Lamb Doner Platter £10.50 · 27 Chicken Doner Platter £9.50 · 28 Mixed Doner Platter £10.50
- **Shawarma**: 29 Lamb Shawarma £6.99 · 30 Chicken Shawarma £5.99 · 31 Mixed Shawarma £6.99
- **Hot Dogs**: 32 Hot Dog £9.50 · 33 Zapata Hot Dog £11.50 · 34 Doner Hot Dog £14.50 · 35 Ajdar Hot Dog £15.50 · 36 Sosis Bandari £9.50
- **Sauces**: Zapata Special Sauce, Garlic, Garlic & Dill, Spicy Chilli, Ketchup, Mayo, BBQ
- **Drinks**: 37 Coca-Cola £1.50 · 38 Diet Coke £1.50 · 39 Fanta £1.50 · 40 7UP £1.50 · 41 Ayran £2.00 · 42 Still Water £1.50 · 43 Sparkling Water £2.00 · 44 Istak £1.50

## Open (ask Ryan / Mama)
- [ ] Ryan: keep the loyalty card on the leaflet? (Not on his 27 Nov version; kept, as he asked on 26 Nov.)
- [ ] Ryan: TVs stay yellow? (27 Nov "same colour palette" was read as the A4.)
- [ ] Mama to check Claude's Persian: سس باربیکیو (BBQ), فیله برگر مرغ زاپاتا (19).
- [ ] Ryan: should Pickle Sauce also be in the sauce list? (His photo stopped at BBQ.)

## A big menu update, step by step (Ryan, 26 Nov 2026: "I'm going to give you sheets and everything, and once we've confirmed it, update it with everything")
1. **Read Ryan's sheets** (photos, Excel, Google Sheets, PDFs) and write every change into `tools/make-menu.py`: names, Persian, prices, ingredients (English and Persian), sauces, drinks, new or removed items and sections. Prices only from Ryan or Mama, never guessed.
2. **Confirm before building:** `python3 tools/menu-check.py --diff` lists every change against the live menu (origin/main). Send Ryan that list in plain words and wait for his yes. Anything unclear on a sheet: ask, don't guess.
3. **Build and check everything:** `bash tools/build-all.sh` (about 10 minutes): printed and phone menu, TV panels, the A4 and its PDF (`menu/Ajdar_Zapata_A4_Double_Sided.pdf`), `tools/menu-check.py` (every output word for word against the list), the TV pictures, `tools/check.cjs`. `--quick` skips the TV pictures to look at the A4 and panels first.
4. **If a section is added or renamed:** `KEY`, `WIDTH`, `HALVES` in `tools/make-sections.py` (which TV it goes on), the A4's column lists in `tools/a4-menu.py` (`cols([...], [...])`), the picture labels ("Burgers, 16 to 21") in `site/monitor-1/index.html` and `site/monitor-2/index.html`, and the phone page's `site/menu/index.html` if the printed menu's page count changes. `menu-check.py` flags all of these.
5. **Look at it:** open the A4 PDF and the TV pages (`/monitor-1/?half=1&preview`, `?half=2`) and check nothing runs off or overlaps; if the A4 front overflows, lower `K1` in `tools/a4-menu.py`.
6. **Send Ryan** the A4 PDF and a picture of each TV; publish `menu/a4/Main.dc.html` and `Back.dc.html` to the A4 artifact.
7. **Live and handoff:** commit with what and why, push to `main` (that puts it on the shop TVs), check Netlify's current deploy is that commit, then update this file: the decisions, the menu snapshot, what's open.

## Building in a Claude sandbox (26 Nov 2026)
Google Fonts is blocked there, so the panels fall back to local fonts. Install them first or the Persian comes out thin: `npm i @fontsource/bebas-neue @fontsource/barlow-semi-condensed @fontsource/vazirmatn @fontsource/barlow-condensed @fontsource/barlow` (the last two for the A4 PDF), convert the woff2 files to ttf into `~/.fonts` with fontTools (Vazirmatn: the **arabic** subset only, no latin files, or Chrome picks the wrong weight), `fc-cache -f`. Checked 26 Nov: the panels then match the 24 Nov ones.

## Which TV shows which half: how it stays locked in (27 Nov 2026)
Ryan, 27 Nov 13:43, with a photo of both TVs showing the whole menu: "fix these monitors ASAP, see which ones they are, make sure they're always going to be constantly updated to the newest version ... develop a system to make sure it's locked in." Opening: 29 Nov.
- **Now:** both TVs still run the TV page they opened on 24 Nov 16:16 (`e28571b`: no ID, can't be reloaded from here, shows show.json's "all"). `netlify/edge-functions/tv-old.js` tells them apart by **when each request arrives** (to the ms, from Netlify's request ID): each TV's timer runs ~95 ppm fast, so its arrival time slips back ~8.2 s (left) / 8.6 s (right) a day in a straight line, fitted on 23 hours of the log (within 0.16 s), and, while it holds, by **its clock reading** (exact until the TV corrects its clock). It hands each its half from the live show.json, so the newest pictures reach them within 2 minutes, and logs every answer. **Left TV = opened 16:16:19 (`o=1795536979`), right TV = 16:16:18 (`o=1795536978`)**, from Ryan's 24 Nov "right becomes left". Both on their halves since 27 Nov 13:59. (The 24 Nov version used fixed windows of the clock reading; the TVs' clock corrections moved them out, so both fell back to the whole menu.)
- **If the bridge's log says "whole menu" for a TV** (its line drifted off): refit `TV` in tv-old.js from the log: per TV, the arrival ms mod 120000 over a day of `/tv/show.json` requests without `p=`; the `/tv/ping.txt` request with the same timestamp gives its `o`. `tools/check.cjs` checks the bridge on real logged requests.
- **After any restart:** the bridge also puts each TV's side in the `az_tv` cookie (5 years). The current TV page reads it, so it comes back on its own half, pins `/tv1` or `/tv2`, keeps it in its memory too, and from then on updates itself: new pictures within 30 s, the page itself when it changes.
- **If a TV ever shows the whole menu after a restart** (its browser kept no cookie): it shows a small code at the bottom, "TV ABCD" (the start of its ID). A photo is enough: put its ID (from its `/tv/ping.txt?id=` reports) in `site/tv/show.json` `"screens": {"<id>": 1 or 2}` and push; it takes its half within 30 s and remembers. Or press **1** / **2** on that TV's remote. Or set its start page to `/tv1` / `/tv2`, which needs no memory at all (the strongest lock).
- **How they are, any time:** Netlify's request log (kept 24 h): `/tv/show.json` without `p=` → the bridge's "-> left / right" lines; `/tv/ping.txt` → each TV's `m` (its side), `o` (when it opened) and, on the current page, `pic` (the picture on the screen).
- Remove tv-old.js once no TV asks for show.json without `p=` (both on the current page).

## Keep the TVs on (Ryan, once per TV, in the TV's own settings)
- [ ] Start page of the TV's browser: **ajdarzapata.co.uk/tv1** on the left TV, **ajdarzapata.co.uk/tv2** on the right TV.
- [ ] The TV starts in that browser when it is switched on (start-up source / boot app).
- [ ] Switch **off**: screensaver, sleep timer, auto power-off, no-signal power-off, eco / energy saving, automatic source switching, USB auto-play. Take the USB sticks out.
- [ ] Power on after a power cut ("power on state": on / last state).
- [ ] Plug the TVs into the wall, not a timer strip.
- [ ] Send Claude the TV's make and model (label on the back, or Settings → About), so the exact menu names can be checked.

## Waiting on Ryan (TVs)
- [ ] The checklist above, then "they're on".
- [ ] The card change: Netlify → team ryanrcm → Usage & billing → Billing details → Payment information → Change payment method (the card owner types it in).

**Paste-in for the next session:** "Read CLAUDE.md and HANDOFF.md in ryanRCM/Ajdar-Zapata. The menu is tools/make-menu.py; for a big update follow 'A big menu update, step by step': menu-check --diff for my yes, then build-all, then push."
