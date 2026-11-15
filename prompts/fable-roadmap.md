# Fable brief · Ajdar Zapata, the next level · 15 Nov 2026

Paste this into a Fable session on `ryanRCM/Ajdar-Zapata`. Read `CLAUDE.md` and `HANDOFF.md` first: every rule there holds and beats anything here.

---

## 1. Why this brief exists

Ajdar Zapata is a sandwich, burger and doner shop at 864 High Road, London N12 9RH. Its menu runs on two TVs in the shop from **ajdarzapata.co.uk** (Netlify, auto-deploys from `main`). On 15 Nov 2026, `node tools/check.cjs --shots` passes on `main` (638415c):
- The full-menu TV: three columns of glass panels on a yellow marble wall, with flames behind.
- The cycling TV: one section at a time at 2.4×, real food photos, and full-screen hero slides.
- The Christmas season switches itself on from 1 Nov to 6 Jan.

It works and it looks loud and alive. This brief takes it from "a good set of screens" to **a small, complete, Apple-grade system for one shop**: one source of truth for the menu, screens that read perfectly from the door, a phone menu people actually like using, and a way for the shop to change a price or mark something sold out in ten seconds without calling anyone.

Ryan, 15 Nov 2026: *"begin to make a setup for Ajdar Zapata in the future … give me a plan for improving it."* He wants everything he makes to be **"very Apple-like … the quality and timelessness and human capability."* For a shop's screens, read that as:
- **Quality:** nothing blurry, nothing misaligned, nothing that stutters.
- **Timelessness:** a calm structure under the seasonal fun, so it still looks right in five years.
- **Human:** a customer at the door can read the price of what they want in two seconds, and a member of staff can change it in ten.

Apple-*like* means the standard of care, not copying Apple. No Apple logos, product names or look-alike UI.

## 2. What is true today (verify before you build)

| Area | State on 15 Nov | What it means |
|---|---|---|
| Menu text | Lifted from `menu/Ajdar_Zapata_Boards.pdf` as **pictures** (`tools/build-walls.py`), never retyped | Safe, but a price change means a new PDF, re-rendering and re-cutting. Text is a bitmap, so it can't be perfectly sharp at every TV size |
| The PDF | Real text: `pdftotext -layout` reads all **38 £ prices**, item numbers, English and Persian (fonts: Barlow Condensed, Barlow SemiBold, Vazirmatn) | The menu can become **data that is checked against the PDF automatically**. Nothing has to be retyped by hand |
| TVs | `/api/screen` (Netlify Function + Blobs) locks each TV to its monitor; `SWAP = true`; TVs reload on every deploy; both TVs share the show clock via Netlify's Date header | Solid. Any change to `main` reaches the shop within about a minute, so a push is a change in the shop |
| Phone page `/menu/` | The yellow board PNGs stacked, with a box covering the printed address | Works, but it's pictures: not searchable, not accessible, no tap-to-zoom by item, and it loads web fonts from Google |
| Seasons | Christmas built (1 Nov – 6 Jan). Halloween reserved for October, nothing built | Seasonal code is mixed into the TV pages (`xmas.js`, `hero.css`) |
| Checks | `tools/check.cjs` (overlaps, loading, slides, phone page), `tools/fps.cjs` (6× CPU throttle) | Good base; no check yet that **prices on screen equal the PDF** |
| Offers | `OFFERS = []` in `site/show.js`: the slide exists but stays hidden until Ryan writes offers | Keep it this way |
| `HANDOFF.md` | Was dated 2 Nov; refreshed 15 Nov | Read it |

## 3. The order of work

One phase per branch and one draft PR per phase. **Never push to `main` and never merge**: Ryan decides when each phase goes live, because `main` is the shop. Batch commits and push once per finished, checked phase (Netlify bills by deploy).

### Phase 0 · Baseline (small, do first)
1. Run `node tools/check.cjs --shots` and `node tools/fps.cjs` three times each on `main`, and write the numbers into `prompts/fable-roadmap-result.md`.
2. Make a **"from the door" check**: render each TV at 1920×1080, downscale to the size a customer sees from about 4 m away, and confirm item names and prices are still readable. Say plainly that the downscale factor is an estimate until Ryan measures the shop: ask him for the distance from the door to the TVs and the TV size in inches. Store both in `CLAUDE.md` once he answers.
3. List every slide's hold time, the loop length and the fps. This is the "before" picture for everything that follows.

### Phase 1 · The menu becomes data (the biggest lever)
Goal: **one file is the truth**, `site/menu.json`, and a price change is one line.
1. Write `tools/extract-menu.py`: read the PDF text (`pdftotext -layout`, or `pdfplumber` for positions) into `site/menu.json`. One entry per item: `{n, en, fa, desc, price, section, board, tags: ["NEW" | "HOUSE SIGNATURE"], soldOut: false}`; sections `{id, en, fa, order}`; the sauces list; drinks; the allergy notice in English and Persian. Persian is copied from the PDF text exactly. Check its character order: RTL extraction can reverse runs, so compare the shaped rendering against the PDF image before trusting it.
2. Write `tools/menu-parity.cjs`: **fails the build** if any price, number, name or Persian string in `menu.json` differs from the PDF's own text. This test is what makes the data trustworthy. Never weaken it to get green.
3. Don't switch the TVs to the data yet. Phase 1 ships the data plus the parity test only, on its own PR, so Ryan can see the menu as a table and confirm it.
4. Hard rule, unchanged: **prices come only from Ryan or his PDFs. Never guess, round or "fix" one.** If the PDF and the boards disagree, stop and ask Ryan.

### Phase 2 · An Apple-grade design system for the shop
Goal: the same brand, built properly. Text that is real type, razor sharp at any TV size.
1. `site/brand.css`: tokens for colour (the boards' own near-black `#121110`, orange `#f07c1a`, cream `#f6efe4`, the yellow and orange walls, dark-red headings, bright-red prices), type (Barlow Condensed ExtraBold for names and prices, Barlow SemiBold for descriptions, Vazirmatn for Persian), a modular type scale, an 8 px spacing grid and radii.
2. **Self-host the fonts** (woff2 in `site/fonts/`, check their licences: Barlow and Vazirmatn are under the SIL Open Font License, and you must check the files you ship). This removes the Google Fonts dependency from the TVs and the phone page, so a slow network can never leave the TV in a fallback font.
3. Tabular figures for every price (`font-variant-numeric: tabular-nums`), so the £ signs line up in a clean column. That is the single most "Apple" detail on a menu.
4. Persian set right-to-left with `dir="rtl"` on its own span, baseline-aligned with the English. No mirrored punctuation.
5. Write `DESIGN.md`: the tokens, the type scale, the motion rules, plus three before/after screenshots.

### Phase 3 · TVs v3: the boards drawn from the data
Goal: the same layout Ryan approved, now drawn from `menu.json` in HTML/CSS, so it is sharp, editable and checkable.
1. Rebuild each panel (the left TV's three columns, the right TV's one-section slides) from the data, matching the current look closely enough that Ryan can't tell at a glance, but sharper. Compare against the current screenshots side by side.
2. Extend `check.cjs`: **every price drawn on screen equals `menu.json`** (read the DOM text), no text overflows or is clipped at 1920×1080 and 1366×768, and nothing covers a price.
3. **Sold out:** an item with `soldOut: true` shows a calm "Sold out today" ribbon (English and Persian, taken from Ryan) and greys its price. It never just disappears, so a customer isn't confused. The words come from Ryan; until he writes them, the ribbon has no text.
4. Motion stays within the existing rules: `transform` and `opacity` only, 30+ fps at 6× throttle, and everything pre-decoded before it moves. Keep the Christmas heroes working on top.
5. Then the photos: only Ryan's clean ones, never watermarked ones. Give Ryan a **shot list** of what's missing (e.g. a real burger photo, since the burger slide reuses sandwich shots) as a short note, not a demand.

### Phase 4 · The phone menu, done properly (`/menu/`)
Goal: the menu people open from a QR code at the counter. Fast, clear, beautiful on a phone.
1. Draw it from `menu.json`: sections as a sticky segmented bar, item cards with the number, English, Persian, description and price in tabular figures. An "English / فارسی" toggle that reorders but never retranslates anything.
2. It works offline after the first visit (a small service worker caching the page, the data and the fonts), loads in under 1 s on 4G, and passes a contrast check (WCAG AA). Real text means screen readers work.
3. A printable QR code for the counter (generated locally, SVG), pointing to `ajdarzapata.co.uk/menu`. Ryan prints it.
4. Allergens: show **only** the shop's own allergy notice, word for word. Per-item allergen data only if the shop supplies it in writing. Never infer allergens from ingredients.

### Phase 5 · The staff page (needs Ryan's yes before you start)
Goal: from a phone, staff change a price, mark sold out or switch the offers slide on, see a preview, and publish. Every change is logged with a date.
1. **Plan it with Ryan first** (`CLAUDE.md`: "Needs a real database … plan it with Ryan first"). Propose: Netlify Blobs for the live menu overrides, a Netlify Function to read and write them, and sign-in through Netlify Identity or a single staff passcode stored as a Netlify environment variable (never in the repo). Rate-limit the function. Every write records who, what, when, the old value and the new value.
2. The TVs read the overrides on top of `menu.json` (overrides win, the parity test still guards the base file), so a sold-out mark shows within a minute without a deploy.
3. Security review before it ships: auth on every write, no secrets in code, input validated (price format `£d.dd` only), and an undo of the last change.
4. Cost: stay on the free Netlify tier's limits. Say in the PR what it costs per month at the shop's traffic.

### Phase 6 · Seasons as a system
1. Move season code into `site/seasons/<name>/` with one switch in `season.js` (dates in one table), so a season is a folder, not edits across the TV pages.
2. Halloween (October) gets built only when Ryan asks.
3. **Ask Ryan** whether the shop wants any other seasons, e.g. Nowruz (Persian New Year, around 20–21 March) or Ramadan opening times. Never assume the shop's culture or customs; he decides.

### Phase 7 · Run it like a product
1. A status page (`/api/screen?status` already exists): show "both TVs checked in within the last 5 minutes" plainly, and offer Ryan an alert (e.g. a daily scheduled check) only if he wants one.
2. A one-line rollback in `CLAUDE.md` (revert the last commit, then push) and a tested branch-preview routine, so every PR is looked at on a Netlify preview link before it touches the shop.
3. Keep `HANDOFF.md` current at the end of every session.

## 4. Hard rules (break one and it doesn't ship)
1. **Never change, retype or invent menu content.** Prices, names, numbers, Persian and the allergy notice come only from Ryan's PDFs or his written words. The parity test enforces it.
2. **Never cover a price.** Motion lives beside, behind or between panels.
3. **Never push to `main` and never merge.** Draft PRs only; Ryan says when it goes live.
4. **Smooth:** `transform` and `opacity` only; 30+ fps at 6× throttle on both TVs; nothing moves before everything has loaded.
5. **No watermarked photos, no invented claims** ("fresh", "halal", "best"), **no offers** Ryan didn't write.
6. **No secrets in the repo**, no paid Netlify add-ons or plan changes without Ryan's yes.
7. **Cost:** Fable uses limits fastest. Do one phase per session, read only what the phase needs, and stop at the end of each phase with the PR and a short result note.

## 5. Questions for Ryan (ask one at a time, only when that phase needs it)
1. Distance from the door to the TVs, and the TV sizes in inches (Phase 0).
2. Does the menu table from Phase 1 match the shop's real prices today? (Phase 1)
3. The exact "Sold out today" wording in English and Persian (Phase 3).
4. Should the phone menu have a QR at the counter, and where? (Phase 4)
5. Who on staff should be able to change prices, and how do they sign in? (Phase 5)
6. Which seasons does the shop want? (Phase 6)

## 6. Done looks like
- One file, `menu.json`, is the truth, proven against the PDF by a test.
- The TVs and the phone menu draw from it, sharp at any size, and check that every price on screen matches.
- Staff can mark sold out or change a price from a phone, logged and undoable (once Ryan approves Phase 5).
- Every phase ends in a draft PR with before/after screenshots, the check output (✅/❌), the fps numbers and a short note of what Ryan needs to decide.
