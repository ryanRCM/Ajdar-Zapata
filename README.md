# Ajdar Zapata

TV menu boards for the shop. Open a link on each TV and it plays full screen, nonstop. No login.

Both TVs show the same thing: the three menu boards side by side (starters & drinks · sandwiches & burgers · doner, shawarma & hot dogs), from `menu/Ajdar_Zapata_Boards.pdf`.

Live: https://claude.ai/artifact/DQufCywpypLtHh7m5geduP

Open that link on each TV and tap the screen once for full screen. Nothing to pick.

## Put it on a real website (free, short address, no sign-in)
`site/` is a complete website and `netlify.toml` tells Netlify to serve it. One time, from a phone or laptop:
1. Go to **app.netlify.com**, sign up with GitHub (free).
2. **Add new site → Import an existing project → GitHub → `Ajdar-Zapata`** → Deploy. No settings to change.
3. **Site configuration → Change site name** → `ajdarzapata`.
4. On each TV, type **ajdarzapata.netlify.app** once and bookmark it.

Every push to this repo updates the site, and the TVs reload every 10 minutes, so new menus appear on their own.

- `site/`: the page and the three boards.
- `menu/`: the menu designs (PDF). `Ajdar_Zapata_Boards.pdf` is the one on the TVs; the others are older versions.
- `HANDOFF.md`: where it stands and what's next (own account, a database for products and what's going on).
