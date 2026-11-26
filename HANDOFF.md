# Ajdar Zapata · handoff · 26 Nov 2026 (final, after Mama's sheet)

*Start with `CLAUDE.md`. Separate from LAIFE.* Ryan, 26 Nov 2026: "a finalized handoff so we don't lose this", "no more mix-ups".

## The one rule
**`tools/make-menu.py` on `main` is the only true menu.** Every change goes into it first, then into all three outputs below, in the same push. Never work from an old artifact, PDF or picture: the "Ajdar Zapata Screens" artifact (board-1..3) and `menu/Ajdar_Zapata_Boards*.pdf`, `Full_Menu_A4.pdf`, `Takeaway_Flyer_A5.pdf`, `Three_TV_Boards.pdf`, `Vertical_Menu_Boards.pdf` are OLD (Cheddar, Green Sauce, Pepsi, Corn Balls, old prices): reference only.

## The three outputs
| Output | What | How it's made |
|---|---|---|
| **TV board** (the shop's two TVs) | ajdarzapata.co.uk/tv1 (left: Starters, Sandwiches, Burgers, Drinks) and /tv2 (right: Doner, Platters, Shawarma, Hot Dogs, Sauces, allergy notice) | `python3 tools/make-sections.py && node tools/sections.cjs && python3 tools/make-sections.py layout`, then `node tools/tv-stills.cjs`, `node tools/check.cjs`, push to `main` |
| **A4 to send out** (double-sided, black and orange) | `menu/Ajdar_Zapata_A4_Double_Sided.pdf` (final, 26 Nov) · artifact "Ajdar Zapata A4 Menu" https://claude.ai/artifact/Lip9yS3R3pBajm6cpGiJEK | `python3 tools/a4-menu.py` → `menu/a4/Main.dc.html` (front), `Back.dc.html` (back); `node tools/a4-pdf.cjs` → the PDF; publish both artboards to that artifact |
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
- A4 layout: front = Starters, Sandwiches, Burgers, Doner Baguettes; back = Platters, Shawarma, Hot Dogs, then Sauces and Drinks, then address and phone, then the allergy notice. Ingredients in English and Persian. Ryan rejected the TVs' yellow look for the A4.

## Mama's sheet, 26 Nov 2026 15:17 (two handwritten pages, read out by Ryan; live the same afternoon)
- 3 Fries: **M £2.99 / L £4.99** (was one size £2.99).
- 14 Royal Zapata Sandwich and 15 Giant Ajdar Zapata: **+ tomato**.
- 18 Chicken Fillet Burger **£7.50** (was £9.50); 19 Zapata Fillet Chicken Burger **£9.50** (was Claude's placeholder £11.50).
- 22-25 doner baguettes: **+ lettuce**. 24 Mixed Doner **£12.50** (was £17.50); 25 Giant Zapata Doner **£17.50** (was £12.50), **+ cheese, + red cabbage**.
- Platters 26-28: **one size, "with chips & salad"** (M/L gone): 26 **£10.50**, 27 **£9.50**, 28 **£10.50**.
- Shawarma 29 **£6.99**, 30 **£5.99**, 31 **£6.99**; "with garlic **and** chilli sauce" (was "or").
- **No placeholder prices left**: every price is Mama's.

## The menu on 26 Nov 2026, after Mama's sheet (snapshot; if this and `tools/make-menu.py` ever differ, the list wins)
- **Starters & Sides**: 1 Chicken Wings · 5 pcs £5.49 · 2 Chicken Wings · 8 pcs £7.99 · 3 Fries M £2.99 / L £4.99 · 4 Cheesy Fries £3.99 · 5 Peri Peri Fries £3.49 · 6 Zapata Loaded Fries £7.99 · 7 Chicken Nuggets £4.99 · 8 Mexican Corn Cup £8.99 · 10 Coleslaw £3.99
- **Sandwiches**: 11 Beef Salami Sandwich £13.00 · 12 Chicken Salami Sandwich £12.00 · 13 Mixed Salami Sandwich £12.50 · 14 Royal Zapata Sandwich £21.50 · 15 Giant Ajdar Zapata £22.50
- **Burgers**: 16 Classic Burger £9.50 · 17 Double Cheeseburger £11.50 · 18 Chicken Fillet Burger £7.50 · 19 Zapata Fillet Chicken Burger £9.50 · 20 Royal Zapata Burger £13.50 · 21 Giant Zapata Burger £18.50
- **Doner Baguettes**: 22 Lamb Doner £11.50 · 23 Chicken Doner £10.50 · 24 Mixed Doner £12.50 · 25 Giant Zapata Doner £17.50
- **Doner Platters**: 26 Lamb Doner Platter £10.50 · 27 Chicken Doner Platter £9.50 · 28 Mixed Doner Platter £10.50
- **Shawarma**: 29 Lamb Shawarma £6.99 · 30 Chicken Shawarma £5.99 · 31 Mixed Shawarma £6.99
- **Hot Dogs**: 32 Hot Dog £9.50 · 33 Zapata Hot Dog £11.50 · 34 Doner Hot Dog £14.50 · 35 Ajdar Hot Dog £15.50 · 36 Sosis Bandari £9.50
- **Sauces**: Zapata Special Sauce, Garlic, Garlic & Dill, Spicy Chilli, Ketchup, Mayo, BBQ
- **Drinks**: 37 Coca-Cola £1.50 · 38 Diet Coke £1.50 · 39 Fanta £1.50 · 40 7UP £1.50 · 41 Ayran £2.00 · 42 Still Water £1.50 · 43 Sparkling Water £2.00 · 44 Istak £1.50

## Open (ask Ryan / Mama)
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

## Telling each TV which it is (24 Nov 2026)
The two TVs are identical to the site, so each is told once. Either press **1** on the left TV's remote and **2** on the right TV's remote while the menu is showing, or set the start pages to `ajdarzapata.co.uk/tv1` (left) and `/tv2` (right). Until told, a TV shows the whole menu. If a TV shows the whole menu again after being switched off and on, it forgets (its browser keeps no memory): then set the start pages, which never need memory.

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
