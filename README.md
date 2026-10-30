# Ajdar Zapata

TV menu boards for the shop. **https://ajdarzapata.co.uk**: open it on each TV, tap once for full screen. No login, nothing to pick.

Both TVs show the three menu boards side by side (starters & drinks · sandwiches & burgers · doner, shawarma & hot dogs), from `menu/Ajdar_Zapata_Boards.pdf`.

Netlify serves `site/` from this repo, so every push to `main` goes live, and the TVs reload every 10 minutes to pick it up.

- `CLAUDE.md`: how it works and how to change the menu (for Claude).
- `HANDOFF.md`: where it stands and what's next.
- `site/`: the website. `menu/`: the menu designs (PDF). `tools/check.cjs`: the check before every push.
