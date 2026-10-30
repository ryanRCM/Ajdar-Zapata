# Ajdar Zapata screens · handoff · 30 Oct 2026

*Work for Ajdar Zapata (the restaurant). Separate from LAIFE: none of LAIFE's data, rules or councils belong here. Moves to its own Claude account later.*

## Where it is now
| What | Where |
|---|---|
| Live TV site (v3) | https://claude.ai/artifact/DQufCywpypLtHh7m5geduP (on Ryan's account, private until shared) |
| Screens (2 horizontal TVs) | Both show the same: the 3 portrait boards side by side at full height. Plain link, nothing to pick |
| Source | `site/`: `index.html` + `board-1..3.png` (`menu/Ajdar_Zapata_Boards.pdf`, 3 portrait pages rendered at 1215×2160) |
| Designs | `menu/Ajdar_Zapata_Boards.pdf` is current (30 Oct). Older: Three TV Boards, Vertical Menu Boards, Full Menu A4, Takeaway Flyer A5 |

Built: full screen, wake lock, cursor hides, retries a failed image, updates reach open screens on their own.

## Next: move it to its own account, with a database
1. **New account.** Make the new Claude account and give it this repo. Artifacts can't move between accounts, so the new account republishes from `site/`.
2. **Everything goes through the database.** Give the new artifact the `db` capability. Collections:
   - `products`: number, name EN, name FA, price, category, board, tags (NEW, HOUSE SIGNATURE), sold-out flag.
   - `boards`: which TV shows which categories, rotation on/off, seconds per board.
   - `log`: what's going on, dated (price changes, sold-outs, new items, tasks, issues).
3. **Draw the boards from the data**, not from PNGs, keeping the look of `Ajdar_Zapata_Boards.pdf` (black, orange headings, numbered orange tags, Persian beside English, address bar at the bottom). A price changed in the database shows on every TV.
4. **Staff page** (same artifact, `#admin`): change a price, mark sold out, add a log line. Phone-first.
5. **Seed** `products` from `menu/Ajdar_Zapata_Boards.pdf` (all items and prices are in it, with descriptions) with `ArtifactData`, then check every price against the PDF.
6. Hand over: share the link to the TVs, write a short guide for staff.

## Waiting on Ryan
- [ ] Put it on Netlify (free, ~5 min, steps in README) → **ajdarzapata.netlify.app** on both TVs. Replaces the artifact link and the short-link idea.
- [ ] Domain: **ajdarzapata.co.uk** was free on 30 Oct (ajdarzapata.com and ajdar-zapata.com are taken; maybe the shop already owns the .com?). Buy it in Netlify (Domain management → Add a domain), or at Namecheap and point it at Netlify DNS.
- [ ] The rest of the specs.
- [ ] The new account.

**Paste-in (new account):** "Read HANDOFF.md in ryanRCM/Ajdar-Zapata. Rebuild the TV screens in this account with a `db` database (products, boards, log), seeded from the menu, and push it here."
