"""Lay the menu out across the two TVs: glass panels on a bright reddish-orange wall, text as big as fits.
(Ryan, 2 Nov 2026: split the menu across the walls; "bright, screamy, reddish-orange", "glassy yellow,
glassy orange", polished high-contrast text, "even bigger", only the address at the bottom, one logo
in the middle.)

Every section is lifted straight off the original boards (site/board-N.png): nothing is retyped.
  1. The empty gaps between items are tightened and the thin divider lines dropped, so the text can be
     bigger. Every printed row is kept.
  2. The lettering is lifted off the black background as see-through ink and recoloured by which ink it
     was (orange headings/prices/tags, yellow Persian names, cream/grey English), per wall palette.
The sections sit on glass panels, two columns per TV. The bottom has only the address, read across the
pair, with the one logo in the middle of it, straddling the gap between the two TVs.
Output per monitor: sec-*.png, logo.png (left or right half is shown by CSS), layout.css.
    python3 tools/build-walls.py        (re-measure SECTIONS below if a new PDF moves things)
"""
import numpy as np
from PIL import Image

B = np.array([18, 17, 16], float)
X0, X1 = 60, 1154
# name: (board, first row, last row)  rows on the 1215x2160 boards
SECTIONS = {
    'starters': (1, 303, 1082), 'sauces': (1, 1121, 1433), 'drinks': (1, 1475, 1794),
    'sandwiches': (2, 305, 989), 'burgers': (2, 1034, 1639),
    'doner': (3, 301, 645), 'platters': (3, 683, 957), 'shawarma': (3, 996, 1270), 'hotdogs': (3, 1307, 1721),
}
# monitor: (outer column, inner column). Inner = next to the middle of the pair, above half the logo.
WALLS = {1: (['sandwiches', 'burgers'], ['starters', 'sauces']),
         2: (['shawarma', 'hotdogs'], ['doner', 'platters', 'drinks'])}
# ink colours on each wall: orange ink (headings, prices, number tags), yellow ink (Persian names, pills),
# neutral ink (English names and descriptions)
PALETTE = {1: {'orange': (176, 18, 8), 'yellow': (92, 26, 0), 'neutral': (18, 12, 8)},
           2: {'orange': (110, 8, 0), 'yellow': (70, 14, 0), 'neutral': (18, 12, 8)}}
CAP = 16  # longest blank gap kept inside a section, in board pixels

def tighten(a):
    """Drop thin divider lines and cap blank gaps. Returns the new image and the heading-rule row."""
    d = np.abs(a - B).max(axis=2)
    ink = d > 30
    rows = ink.any(axis=1)
    keep = np.ones(len(rows), bool)
    y = 0
    while y < len(rows):  # thin full-width faint lines between items
        if rows[y]:
            e = y
            while e < len(rows) and rows[e]: e += 1
            band = slice(y, e)
            wide = ink[band].mean(axis=0).mean() > 0.6 if e - y <= 3 else False
            faint = d[band][ink[band]].max() < 110
            if wide and faint: keep[band] = False
            y = e
        else:
            y += 1
    rows = rows & keep
    y = 0
    while y < len(rows):  # cap blank runs
        if not rows[y]:
            e = y
            while e < len(rows) and not rows[e]: e += 1
            if e - y > CAP: keep[y + CAP:e] = False
            y = e
        else:
            y += 1
    out = a[keep]
    # heading rule: the first thick full-width orange band
    o = (np.abs(out - np.array([240, 124, 26])).max(axis=2) < 60).mean(axis=1) > 0.8
    rule = int(np.argmax(o)) if o.any() else 60
    return out, rule

def lift(a, pal):
    """Black-background lettering -> see-through ink in the wall's colours."""
    v = a - B
    r = np.maximum(v[..., 0], 1)
    ratio = v[..., 1] / r
    alpha = np.clip(np.abs(v).max(axis=2) / 228, 0, 1)
    rgba = np.zeros(a.shape[:2] + (4,), float)
    cls = np.where(ratio < 0.6, 0, np.where(ratio < 0.86, 1, 2))
    for k, name in enumerate(['orange', 'yellow', 'neutral']):
        m = cls == k
        rgba[m, :3] = pal[name]
        if name == 'orange':
            alpha = np.where(m, np.clip(v[..., 0] / 222, 0, 1), alpha)
        if name == 'yellow':
            alpha = np.where(m, np.clip(v[..., 0] / 227, 0, 1), alpha)
    rgba[..., 3] = alpha * 255
    rgba[alpha < 0.04] = 0
    return Image.fromarray(np.clip(rgba, 0, 255).round().astype(np.uint8), 'RGBA')

def logo():
    """The logo cut out of the original board: everything outside the oval becomes see-through."""
    a = np.asarray(Image.open('site/board-2.png').convert('RGB').crop((372, 40, 843, 262)), float)
    dist = np.abs(a - B).max(axis=2)
    near = dist < 40
    out = np.zeros_like(near); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= near
    while True:
        g = out.copy(); g[1:] |= out[:-1]; g[:-1] |= out[1:]; g[:, 1:] |= out[:, :-1]; g[:, :-1] |= out[:, 1:]; g &= near
        if (g == out).all(): break
        out = g
    alpha = 1 - np.clip(1 - dist / 40, 0, 1) * out
    return Image.fromarray(np.dstack([a, alpha * 255]).round().astype(np.uint8), 'RGBA')

# ---- measure every section once (sizes are the same on both walls)
boards = {n: np.asarray(Image.open(f'site/board-{n}.png').convert('RGB'), float) for n in (1, 2, 3)}
tight = {}
for name, (b, y0, y1) in SECTIONS.items():
    tight[name] = tighten(boards[b][y0:y1 + 1, X0:X1])

# ---- layout, in pixels of a 1920x1080 screen
W, H = 1920.0, 1080.0
M = 22.0                          # outer margin
GAP = 18.0                        # between panels
PAD = 16.0                        # inside a panel
TOP, BOTTOM = 16.0, 1080 - 84.0   # the address bar sits below BOTTOM
LOGO_W = 330.0                    # the whole logo, across both TVs (half on each), at the bottom middle
LOGO_H = LOGO_W * 222 / 471
LOGO_TOP = H - LOGO_H - 6
col_w = (W - 2 * M - GAP) / 2

def col_need(names, s, top):
    return top + sum(tight[n][0].shape[0] * s + 2 * PAD for n in names) + GAP * (len(names) - 1)

s = (col_w - 2 * PAD) / (X1 - X0)           # as wide as a column allows
for mon, (outer, inner) in WALLS.items():  # ...unless a column runs out of height
    for names, bottom in ((outer, BOTTOM), (inner, LOGO_TOP - GAP)):
        while col_need(names, s, TOP) > bottom:
            s -= 0.002
print(f'scale {s:.3f} screen px per board px: text {s / 0.5:.2f}x the original whole boards, {s / 0.7019:.2f}x the last version')

pct = lambda v, ref: f'{v / ref * 100:.3f}%'
for mon, (outer, inner) in WALLS.items():
    css = [f'/* Made by tools/build-walls.py: do not edit by hand. Text scale {s:.3f}. */']
    outer_x = M if mon == 1 else W - M - col_w
    inner_x = W - M - col_w if mon == 1 else M
    for names, x, bottom, side in ((outer, outer_x, BOTTOM, 'outer'), (inner, inner_x, LOGO_TOP - GAP, 'inner')):
        y = TOP
        for name in names:
            img, rule = tight[name]
            lift(img, PALETTE[mon]).save(f'site/monitor-{mon}/sec-{name}.png', optimize=True)
            h = img.shape[0] * s + 2 * PAD
            css.append(f'.sec-{name} {{ left: {pct(x, W)}; top: {pct(y, H)}; width: {pct(col_w, W)}; height: {pct(h, H)}; }}')
            css.append(f'.hl[data-for="{name}"] {{ left: {pct(x + PAD, W)}; width: {pct(col_w - 2 * PAD, W)}; top: {pct(y + PAD + rule * s, H)}; }}')
            y += h + GAP
        css.append(f'.{side}-free {{ left: {pct(x, W)}; width: {pct(col_w, W)}; top: {pct(y, H)}; height: {pct(bottom - y, H)}; }}')
        print(mon, side, 'ends at', round(y - GAP), 'free below:', round(bottom - y))
    logo().save(f'site/monitor-{mon}/logo.png', optimize=True)
    lx = W - LOGO_W / 2 if mon == 1 else -LOGO_W / 2
    css.append(f'.logo {{ left: {pct(lx, W)}; top: {pct(LOGO_TOP, H)}; width: {pct(LOGO_W, W)}; height: {pct(LOGO_H, H)}; }}')
    css.append(f'.halo {{ left: {pct(lx - LOGO_W * .1, W)}; top: {pct(LOGO_TOP - LOGO_H * .12, H)}; width: {pct(LOGO_W * 1.2, W)}; height: {pct(LOGO_H * 1.24, H)}; }}')
    # the address bar: from the outer margin to just short of the logo half
    side = 'left' if mon == 1 else 'right'
    css.append(f'.address {{ top: {pct(BOTTOM + 12, H)}; height: {pct(H - BOTTOM - 24, H)}; }}')
    css.append(f'.address .frame {{ {side}: {pct(M, W)}; {"right" if mon == 1 else "left"}: {pct(LOGO_W / 2 + 18, W)}; }}')
    open(f'site/monitor-{mon}/layout.css', 'w').write('\n'.join(css) + '\n')
