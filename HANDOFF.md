# Ajdar Zapata screens · handoff · 30 Oct 2026

*Work for Ajdar Zapata (the restaurant). Separate from LAIFE: none of LAIFE's data, rules or councils belong here. Moves to its own Claude account later.*

## Where it is now
| What | Where |
|---|---|
| Live TV site (v1) | https://claude.ai/artifact/DQufCywpypLtHh7m5geduP (on Ryan's account, private until shared) |
| Screens (2 TVs, locked in 30 Oct) | TV 1: sandwiches/burgers/hot dogs, fixed · TV 2: doner/shawarma ↔ starters/sides/drinks, 20s each. Each TV remembers its pick, so the plain link works |
| Source | `site/`: `index.html` + `board-1..3.png` (the Three TV Boards PDF rendered at 3840×2160) |
| Original designs | `menu/`: Three TV Boards, Vertical Menu Boards, Full Menu A4, Takeaway Flyer A5 |

Built: full screen, wake lock, cursor hides, retries a failed image, updates reach open screens on their own.

## Next: move it to its own account, with a database
1. **New account.** Make the new Claude account and give it this repo. Artifacts can't move between accounts, so the new account republishes from `site/`.
2. **Everything goes through the database.** Give the new artifact the `db` capability. Collections:
   - `products`: number, name EN, name FA, price, category, board, tags (NEW, HOUSE SIGNATURE), sold-out flag.
   - `boards`: which TV shows which categories, rotation on/off, seconds per board.
   - `log`: what's going on, dated (price changes, sold-outs, new items, tasks, issues).
3. **Draw the boards from the data**, not from PNGs, keeping the PDF look (black, orange headers, red rule, Persian on the right). A price changed in the database shows on every TV.
4. **Staff page** (same artifact, `#admin`): change a price, mark sold out, add a log line. Phone-first.
5. **Seed** `products` from `menu/Three_TV_Boards.pdf` (43 items, all prices are in it) with `ArtifactData`, then check every price against the PDF.
6. Hand over: share the link to the TVs, write a short guide for staff.

## Waiting on Ryan
- [ ] Share the live link (Share → anyone with the link) so the TVs open it.
- [ ] Short links (e.g. is.gd/ajdartv1): the cloud session was blocked from making them; Ryan can make them or allow it.
- [ ] The rest of the specs.
- [ ] The new account.

**Paste-in (new account):** "Read HANDOFF.md in ryanRCM/Ajdar-Zapata. Rebuild the TV screens in this account with a `db` database (products, boards, log), seeded from the menu, and push it here."
