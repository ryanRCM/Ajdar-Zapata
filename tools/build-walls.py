"""Lay the menu out across the two TVs, bigger (Ryan, 2 Nov 2026: "make the words even bigger ... someone
in the store must be able to see these things"; he chose to split the menu between the two walls).

Each menu section is cut straight from the themed boards (site/monitor-1/board-N.png yellow,
site/monitor-2/board-N.png orange), so every price, name and Persian word is exactly as printed:
nothing is retyped. The sections go into two columns per TV, all at one scale, with the logo
centred between them. Output per monitor: sec-*.png, logo.png, and layout.css (positions in % of
a 16:9 screen). Run after tools/yellow-boards.py and tools/orange-boards.py:
    python3 tools/build-walls.py
If the boards change, re-measure the section rows below (blank bands between sections).
"""
from PIL import Image

X0, X1 = 60, 1154  # crop width: the boards' content runs from x 67 to 1146
# name: (board, first row, last row, heading-rule row)   rows measured on the 1215x2160 boards
SECTIONS = {
    'starters':   (1, 303, 1082, 370.5),
    'sauces':     (1, 1121, 1433, 1188.5),
    'drinks':     (1, 1475, 1794, 1543),
    'sandwiches': (2, 305, 989, 377.5),
    'burgers':    (2, 1034, 1639, 1106.5),
    'doner':      (3, 301, 645, 367.5),
    'platters':   (3, 683, 957, 748.5),
    'shawarma':   (3, 996, 1270, 1061.5),
    'hotdogs':    (3, 1307, 1721, 1373),
}
WALLS = {  # monitor: (left column, right column)
    1: (['starters', 'sauces'], ['sandwiches', 'burgers']),
    2: (['doner', 'platters', 'drinks'], ['shawarma', 'hotdogs']),
}
W, H = 1920.0, 1080.0
TOP, BOTTOM = 0.025 * H, 0.89 * H      # content area; the address strip and allergy notice sit below
GAP = 40                                # board pixels between sections in a column
CENTRE = 300.0                          # screen pixels for the middle column with the logo
LOGO = (372, 40, 843, 262)              # logo crop on the boards (x0, y0, x1, y1)

BG = {1: (255, 198, 26), 2: (240, 124, 26)}  # wall colours, as in yellow-boards.py / orange-boards.py

def logo_img(bg):
    """The logo from the original full-colour board (256-colour boards band its gradient), with only
    the plain black background around it, reached from the crop's edges, turned to the wall colour."""
    import numpy as np
    a = np.asarray(Image.open('site/board-2.png').convert('RGB').crop(LOGO), float)
    dist = np.abs(a - np.array([18, 17, 16])).max(axis=2)
    near = dist < 40
    out = np.zeros_like(near); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= near
    while True:
        g = out.copy(); g[1:] |= out[:-1]; g[:-1] |= out[1:]; g[:, 1:] |= out[:, :-1]; g[:, :-1] |= out[:, 1:]; g &= near
        if (g == out).all(): break
        out = g
    w = (np.clip(1 - dist / 40, 0, 1) * out)[..., None]
    a = a + (np.array(bg, float) - np.array([18, 17, 16])) * w
    return Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8))

def col_h(names):
    return sum(SECTIONS[n][2] - SECTIONS[n][1] + 1 for n in names) + GAP * (len(names) - 1)

s = min((BOTTOM - TOP) / col_h(c) for cols in WALLS.values() for c in cols)
col_w = (X1 - X0) * s
margin = (W - 2 * col_w - CENTRE) / 2
assert margin >= 16, margin
pct = lambda v, ref: f'{v / ref * 100:.3f}%'
print(f'scale {s:.4f} screen px per board px (whole boards were {H / 2160:.4f}): text {s / (H / 2160):.2f}x bigger')

for mon, cols in WALLS.items():
    boards = {n: Image.open(f'site/monitor-{mon}/board-{n}.png') for n in (1, 2, 3)}  # keep the 256-colour palette: small files
    css = [f'/* Made by tools/build-walls.py: do not edit by hand. Scale {s:.4f}, columns {col_w:.0f}px of 1920. */']
    for ci, names in enumerate(cols):
        x = margin if ci == 0 else W - margin - col_w
        y = TOP
        for name in names:
            b, y0, y1, rule = SECTIONS[name]
            boards[b].crop((X0, y0, X1, y1 + 1)).save(f'site/monitor-{mon}/sec-{name}.png', optimize=True)
            h = (y1 - y0 + 1) * s
            css.append(f'.sec-{name} {{ left: {pct(x, W)}; top: {pct(y, H)}; width: {pct(col_w, W)}; height: {pct(h, H)}; }}')
            r = y + (rule - y0) * s
            css.append(f'.hl[data-for="{name}"] {{ left: {pct(x + (67 - X0) * s, W)}; width: {pct((1147 - 67) * s, W)}; top: {pct(r, H)}; }}')
            y += h + GAP * s
        css.append(f'/* column {ci + 1} ends at {y - GAP * s:.0f}px of 1080 */')
        css.append(f'.col{ci + 1}-free {{ left: {pct(x, W)}; width: {pct(col_w, W)}; top: {pct(y - GAP * s + 0.02 * H, H)}; height: {pct(BOTTOM - (y - GAP * s + 0.02 * H), H)}; }}')
    lw = CENTRE - 30
    lh = lw * (LOGO[3] - LOGO[1]) / (LOGO[2] - LOGO[0])
    logo_img(BG[mon]).save(f'site/monitor-{mon}/logo.png', optimize=True)
    lx = margin + col_w + (CENTRE - lw) / 2
    css.append(f'.logo {{ left: {pct(lx, W)}; top: {pct(TOP, H)}; width: {pct(lw, W)}; height: {pct(lh, H)}; }}')
    css.append(f'.halo {{ left: {pct(lx - lw * 0.12, W)}; top: {pct(TOP - lh * 0.12, H)}; width: {pct(lw * 1.24, W)}; height: {pct(lh * 1.24, H)}; }}')
    css.append(f'.centre-free {{ left: {pct(margin + col_w + 20, W)}; width: {pct(CENTRE - 40, W)}; top: {pct(TOP + lh + 0.02 * H, H)}; height: {pct(BOTTOM - TOP - lh - 0.02 * H, H)}; }}')
    open(f'site/monitor-{mon}/layout.css', 'w').write('\n'.join(css) + '\n')
    print(mon, 'written')
