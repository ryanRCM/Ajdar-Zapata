# Ajdar Zapata · handoff · 2 Nov 2026

*Start with `CLAUDE.md`. Separate from LAIFE.*

## Where it is
| What | Status |
|---|---|
| Website | `site/` on Netlify, auto-deploys from `main` ✅. Netlify connector connected 30 Oct: site `ajdar-zapata` (renamed from `domain-lock`). Linked to the repo 2 Nov, Netlify's deploy key added to GitHub (read-only) by Ryan. If ajdarzapata.co.uk still shows the old single-page menu, the latest build is blocked or hasn't run: see Waiting on Ryan |
| Domain | **ajdarzapata.co.uk** bought 30 Oct 2026 via Netlify (Netlify DNS), renews 30 Oct 2027 ✅. **Live 30 Oct**: https and www both serve the menu, http redirects to https |
| TVs | 2 horizontal TVs: **/monitor-1** (still) and **/monitor-2** (Fable's motion, merged 2 Nov: 7-scene food reel with slab wipes and kinetic type, embers, flame licks, heading-rule light runs, logo rings). Monitor 2 runs **on orange** (Ryan, 2 Nov: "Background ORANGE not black"): own recoloured boards in `site/monitor-2/`, made by `tools/orange-boards.py`; re-run it after any new board PNGs. Both 3 boards full width. Netlify badge hidden. What each scene does: `prompts/fable-monitor-2-result.md` |
| Menu | `menu/Ajdar_Zapata_Boards.pdf` (current), rendered into `site/board-1..3.png` |
| Check | `node tools/check.cjs` → ✅ 1920×1080 and 1366×768 |
| Old | The first version was a Claude artifact (claude.ai/artifact/DQufCywpypLtHh7m5geduP). It needs a sign-in, so it's retired: the TVs use the domain |

## Next
1. Ryan puts ajdarzapata.co.uk/monitor-1 and /monitor-2 on the TVs. Watch monitor 2 on the real TV: if it stutters, thin the flame licks in `site/monitor-2/motion.js`.
2. **Menu as data** (Ryan wants all the data on the site later). Move the menu into `site/menu.json`: number, name EN, name FA, description, price, category, board, tags (NEW, HOUSE SIGNATURE), sold out. Draw the boards from it in HTML/CSS, keeping the look of `Ajdar_Zapata_Boards.pdf` (black, orange headings, numbered orange tags, Persian beside English, address bar at the bottom). Then a price change is one line. Check every price against the PDF before it goes live.
3. **Later:** a staff page to change prices or mark sold out from a phone, plus a dated log of what's going on. Needs a real database (e.g. Netlify Blobs or a small backend), so plan it with Ryan first.

## Waiting on Ryan
- [x] **Unblock Netlify builds.** Ryan upgraded the Netlify plan (2 Nov), which lifts the free plan's block on commits from an "unrecognized Git contributor" (Claude's commits).
- [ ] Put /monitor-1 and /monitor-2 on the TVs; say hit or miss on the monitor 2 animation.
- [ ] Persian allergy line (Fable's translation, reviewed 2 Nov, reads correctly): Ryan to confirm with the shop.
- [ ] Hang **monitor 1 on the left**, monitor 2 on the right: the address reads across the pair.
- [ ] Any more specs.

**Paste-in:** "Read CLAUDE.md and HANDOFF.md in ryanRCM/Ajdar-Zapata, then do Next 1."
