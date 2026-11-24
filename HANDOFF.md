# Ajdar Zapata · handoff · 24 Nov 2026

*Start with `CLAUDE.md`. Separate from LAIFE.*

## Where it is
| What | Status |
|---|---|
| TVs | Since 24 Nov the website is the main thing again, not USB. **Left TV: ajdarzapata.co.uk/tv1** (the whole menu), **right TV: ajdarzapata.co.uk/tv2** (one section at a time, Santa's Robbery in the Christmas season). Still pictures plus a tiny silent video that keeps the TV awake (the likely reason the TV browser kept closing the page). Not yet seen on the real TVs |
| Hosting | Netlify, **just the host**: plain files, nothing runs on Netlify (functions, edge function and Blobs removed 24 Nov). Every push to `main` goes live in about a minute |
| Domain | ajdarzapata.co.uk, bought through Netlify 30 Oct 2026, renews 30 Oct 2027 |
| Netlify plan | Personal: $9 a month, 1,000 credits a month, billed at the start of each monthly cycle. Each push to `main` costs 15 credits; the TVs cost a few. Out of credits with auto-recharge off (the default) = every site on the account is paused |
| Menu | Mama's menu (18 Nov), one list: `tools/make-menu.py`. After a change: rebuild (CLAUDE.md), then `node tools/tv-stills.cjs`, then `node tools/check.cjs` |
| Check | `node tools/check.cjs` → all ✅ (24 Nov) |

## Roadmap (Ryan, 24 Nov: "boot it once and leave it forever")
1. **TVs on the website, for good.** Ryan does the TV checklist below, tells Claude, and Claude reads the TVs' reports (Netlify request log, `/tv/ping.txt`, kept 24 hours) to confirm they stay up.
2. **Netlify paid from the business owner's card.** Netlify → team ryanrcm → Usage & billing → Billing details → Payment information → Change payment method. The card owner types the card in themselves. Never put card details in a chat.
3. **Later: Mama changes the menu from her phone.** Plan it with Ryan: the simplest safe way for a price change to reach `tools/make-menu.py`, be checked, and go live.

## Keep the TVs on (Ryan, once per TV, in the TV's own settings)
- [ ] Start page of the TV's browser: **ajdarzapata.co.uk/tv1** on the left TV, **ajdarzapata.co.uk/tv2** on the right TV.
- [ ] The TV starts in that browser when it is switched on (start-up source / boot app).
- [ ] Switch **off**: screensaver, sleep timer, auto power-off, no-signal power-off, eco / energy saving, automatic source switching, USB auto-play. Take the USB sticks out.
- [ ] Power on after a power cut ("power on state": on / last state).
- [ ] Plug the TVs into the wall, not a timer strip.
- [ ] Send Claude the TV's make and model (label on the back, or Settings → About), so the exact menu names can be checked.

## Waiting on Ryan
- [ ] The checklist above, then "they're on".
- [ ] The card change (roadmap 2).
- [ ] Mama's own prices for the placeholders (19 Zapata Chicken Burger, the platter sizes): see CLAUDE.md.

**Paste-in:** "Read CLAUDE.md and HANDOFF.md in ryanRCM/Ajdar-Zapata. The TVs are on: read their reports and tell me if they stay up."
