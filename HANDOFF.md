# Ajdar Zapata · handoff · 2 Nov 2026

*Start with `CLAUDE.md`. Separate from LAIFE.*

## Where it is
| What | Status |
|---|---|
| Website | `site/` on Netlify, auto-deploys from `main` ✅. Netlify connector connected 30 Oct: site `ajdar-zapata` (renamed from `domain-lock`). **Not linked to the repo yet**: still serving the 30 Oct upload, so the 2 Nov monitor pages aren't live until Ryan links it |
| Domain | **ajdarzapata.co.uk** bought 30 Oct 2026 via Netlify (Netlify DNS), renews 30 Oct 2027 ✅. **Live 30 Oct**: https and www both serve the menu, http redirects to https |
| TVs | 2 horizontal TVs: **/monitor-1** (still) and **/monitor-2** (food reel + light sweep + logo glow), both 3 boards full width. Netlify badge hidden. Built 2 Nov |
| Menu | `menu/Ajdar_Zapata_Boards.pdf` (current), rendered into `site/board-1..3.png` |
| Check | `node tools/check.cjs` → ✅ 1920×1080 and 1366×768 |
| Old | The first version was a Claude artifact (claude.ai/artifact/DQufCywpypLtHh7m5geduP). It needs a sign-in, so it's retired: the TVs use the domain |

## Next
1. Ryan puts ajdarzapata.co.uk/monitor-1 and /monitor-2 on the TVs. Ryan plans to have Fable polish the monitor 2 motion: keep the reel inside board two's empty strip and the prices untouched.
2. **Menu as data** (Ryan wants all the data on the site later). Move the menu into `site/menu.json`: number, name EN, name FA, description, price, category, board, tags (NEW, HOUSE SIGNATURE), sold out. Draw the boards from it in HTML/CSS, keeping the look of `Ajdar_Zapata_Boards.pdf` (black, orange headings, numbered orange tags, Persian beside English, address bar at the bottom). Then a price change is one line. Check every price against the PDF before it goes live.
3. **Later:** a staff page to change prices or mark sold out from a phone, plus a dated log of what's going on. Needs a real database (e.g. Netlify Blobs or a small backend), so plan it with Ryan first.

## Waiting on Ryan
- [ ] **Link the Netlify site to the repo** (Site configuration → Build & deploy → Link repository → GitHub → Ajdar-Zapata, branch main). That deploys the monitor pages and every future push.
- [ ] Put /monitor-1 and /monitor-2 on the TVs; say hit or miss on the monitor 2 animation.
- [ ] Any more specs.

**Paste-in:** "Read CLAUDE.md and HANDOFF.md in ryanRCM/Ajdar-Zapata, then do Next 1."
