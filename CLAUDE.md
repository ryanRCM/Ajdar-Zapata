# Ajdar Zapata · CLAUDE.md

Read this first, then `HANDOFF.md`. This repo is the TV menu website for **Ajdar Zapata**, a sandwich shop at 864 High Road, London N12 9RH. It is separate from Ryan's LAIFE project: none of LAIFE's rules, data or files belong here.

## What it is
- Two horizontal TVs in the shop open **https://ajdarzapata.co.uk** and show the menu full screen, nonstop. No login, nothing to click.
- Both TVs show the same page: the three portrait menu boards side by side at full height.
- **Hosting:** Netlify, linked to this repo (`netlify.toml` → serves `site/`). **Every push to `main` goes live** within about a minute, and the TVs reload every 10 minutes. So a push is a change in the shop: check before you push.
- **Domain:** `ajdarzapata.co.uk`, bought 30 Oct 2026 through Netlify (Netlify DNS), renews 30 Oct 2027. Ryan owns the Netlify account and pays for the domain.

## Files
| Path | What |
|---|---|
| `site/index.html` | The page: three boards in a row, wake lock, hidden cursor, tap for full screen, 10-min reload, retries a failed image |
| `site/board-1..3.png` | The boards: `menu/Ajdar_Zapata_Boards.pdf` pages 1–3 at 1215×2160. 1 = starters, sauces, drinks · 2 = sandwiches, burgers · 3 = doner, platters, shawarma, hot dogs |
| `menu/Ajdar_Zapata_Boards.pdf` | **The current menu design** (Ryan, 30 Oct 2026). The other PDFs in `menu/` are older versions, kept for reference |
| `tools/check.cjs` | The check before every push |
| `HANDOFF.md` | Where it stopped and what's next |

## How to change the menu
1. **New PDF from Ryan:** render each page at TV height and replace the boards:
   `pdftoppm -png -r 108 menu/<new>.pdf site/board` (810×1440pt pages → 1215×2160). Other page sizes: pick `-r` so the height comes out at 2160.
2. Run `node tools/check.cjs` and show ✅/❌.
3. Commit with what and why, push to `main`, then open https://ajdarzapata.co.uk to confirm it's live.

## Rules
- **Never put the shop's menu wrong on the TVs.** Prices come only from Ryan or his PDFs. Don't guess, round or "fix" a price.
- One change per push, checked first. If live breaks, revert the last commit and push (that's the rollback), then fix.
- No secrets in this repo, ever. If Netlify settings need changing from code, Ryan adds a `NETLIFY_AUTH_TOKEN` to the Claude environment settings; never ask him to paste it in chat.
- Money (domain, paid plans) is Ryan's call.
- Talk to Ryan short and plain, the main thing first, one step at a time.
