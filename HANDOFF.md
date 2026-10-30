# Ajdar Zapata · handoff · 30 Oct 2026

*Start with `CLAUDE.md`. Separate from LAIFE.*

## Where it is
| What | Status |
|---|---|
| Website | `site/` on Netlify, auto-deploys from `main` ✅ |
| Domain | **ajdarzapata.co.uk** bought 30 Oct 2026 via Netlify (Netlify DNS), renews 30 Oct 2027 ✅. DNS works, but at handoff Netlify answered **404 Not Found** for it: the domain isn't on a site with a published deploy yet (check Deploys + Domain management) |
| TVs | 2 horizontal TVs, both the same page: 3 portrait boards side by side |
| Menu | `menu/Ajdar_Zapata_Boards.pdf` (current), rendered into `site/board-1..3.png` |
| Check | `node tools/check.cjs` → ✅ 1920×1080 and 1366×768 |
| Old | The first version was a Claude artifact (claude.ai/artifact/DQufCywpypLtHh7m5geduP). It needs a sign-in, so it's retired: the TVs use the domain |

## Next
1. Fix the 404: in Netlify, the Ajdar-Zapata site needs a green **Published** deploy and `ajdarzapata.co.uk` listed under its Domain management. Then confirm https://ajdarzapata.co.uk loads the boards (and `www.`), then that both TVs have it bookmarked full screen.
2. **Menu as data** (Ryan wants all the data on the site later). Move the menu into `site/menu.json`: number, name EN, name FA, description, price, category, board, tags (NEW, HOUSE SIGNATURE), sold out. Draw the boards from it in HTML/CSS, keeping the look of `Ajdar_Zapata_Boards.pdf` (black, orange headings, numbered orange tags, Persian beside English, address bar at the bottom). Then a price change is one line. Check every price against the PDF before it goes live.
3. **Later:** a staff page to change prices or mark sold out from a phone, plus a dated log of what's going on. Needs a real database (e.g. Netlify Blobs or a small backend), so plan it with Ryan first.

## Waiting on Ryan
- [ ] Bookmark ajdarzapata.co.uk on both TVs once it loads.
- [ ] Any more specs.

**Paste-in:** "Read CLAUDE.md and HANDOFF.md in ryanRCM/Ajdar-Zapata, then do Next 1."
