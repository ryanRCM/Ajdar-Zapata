# Ajdar Zapata

TV menu boards for the shop. No login. Open one address per TV and tap once for full screen:

| TV | Address | Shows |
|---|---|---|
| Monitor 1 | **ajdarzapata.co.uk/monitor-1** (or just ajdarzapata.co.uk) | The three boards, still |
| Monitor 2 | **ajdarzapata.co.uk/monitor-2** | The same boards plus motion: a food reel (sandwiches, burgers, doner, shawarma, hot dogs) in board two's empty strip, a light sweep and a glowing logo |

Both show the three menu boards side by side (starters & drinks · sandwiches & burgers · doner, shawarma & hot dogs), from `menu/Ajdar_Zapata_Boards.pdf`.

Netlify serves `site/` from this repo, so every push to `main` goes live, and the TVs reload every 10 minutes to pick it up.

- `CLAUDE.md`: how it works and how to change the menu (for Claude).
- `HANDOFF.md`: where it stands and what's next.
- `site/`: the website. `menu/`: the menu designs (PDF). `tools/check.cjs`: the check before every push.
