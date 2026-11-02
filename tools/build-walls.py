"""Lay the menu out across the two TVs: glass panels on a bright reddish-orange wall, text as big as fits.
(Ryan, 2 Nov 2026: split the menu across the walls; "bright, screamy, reddish-orange", "glassy yellow,
glassy orange", polished high-contrast text, "even bigger", only the address at the bottom, one logo
in the middle.)

Every section is lifted straight off the original boards (site/board-N.png): nothing is retyped.
  1. The empty gaps between items are tightened and the thin divider lines dropped, so the text can be
     bigger. Every printed row is kept.
  2. The lettering is lifted off the black background as see-through ink and recoloured by which ink it
     was (orange headings/prices/tags, yellow Persian names, cream/grey English), per wall palette.
The left TV shows every section at once on glass panels in three columns; the right TV cycles through the
sections one at a time, each as big as fits, beside its food animation. The bottom bar has only the allergy notice;
the one logo sits at the top of the right TV's food column.
Output per monitor: sec-*.png, logo.png (left or right half is shown by CSS), layout.css.
    python3 tools/build-walls.py        (re-measure SECTIONS below if a new PDF moves things)
"""
import os, subprocess, tempfile
import numpy as np
from PIL import Image, ImageFilter

B = np.array([18, 17, 16], float)
X0, X1 = 60, 1154
# name: (board, first row, last row)  rows on the 1215x2160 boards
SECTIONS = {
    'starters': (1, 303, 1082), 'sauces': (1, 1121, 1433), 'drinks': (1, 1475, 1794),
    'sandwiches': (2, 305, 989), 'burgers': (2, 1034, 1639),
    'doner': (3, 301, 645), 'platters': (3, 683, 957), 'shawarma': (3, 996, 1270), 'hotdogs': (3, 1307, 1721),
}
# Left TV: the whole menu at once, three columns (the last one is next to the middle of the pair, above
# half the logo). Right TV: one section at a time, as big as the screen allows (Ryan, 2 Nov 2026: "one of
# them static with everything, the other one cycling big").
STATIC = [['starters', 'sauces', 'drinks'], ['sandwiches', 'burgers'], ['doner', 'platters', 'shawarma', 'hotdogs']]
# Colours on each wall (Ryan, 2 Nov 2026: "different colours ... very nice", like the big chains' boards:
# strong red prices, dark headings, black item names, high contrast on bright glass).
#   heading: section titles · price: prices and number tags · persian: Persian names · name: English item
#   names · desc: the small descriptions
PALETTE = {1: {'heading': (120, 10, 0), 'price': (222, 22, 10), 'persian': (168, 58, 0), 'name': (14, 10, 8), 'desc': (72, 52, 36)},
           2: {'heading': (110, 6, 0), 'price': (206, 14, 30), 'persian': (150, 46, 0), 'name': (14, 10, 8), 'desc': (70, 46, 34)}}
CAP = 16  # longest blank gap kept inside a section, in board pixels
# Clean text (Christmas update, 2 Nov 2026): the lettering is lifted from the PDF rendered at K times the
# board size, then shrunk to exactly the pixels each TV shows it at, so edges stay crisp (no stretching).
K = 3
PDF = 'menu/Ajdar_Zapata_Boards.pdf'
# Thickening (in output pixels of each TV) so the lettering reads bolder from across the shop: a little,
# never so much that letters run together.
GROW = {1: 0.55, 2: 0.45}

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
            wide = ink[band].mean(axis=0).mean() > 0.6 if e - y <= 3 * K else False
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
            if e - y > CAP * K: keep[y + CAP * K:e] = False
            y = e
        else:
            y += 1
    out = a[keep]
    # heading rule: the first thick full-width orange band
    o = (np.abs(out - np.array([240, 124, 26])).max(axis=2) < 60).mean(axis=1) > 0.8
    rule = int(np.argmax(o)) if o.any() else 60
    return out, rule

def lift(a, pal, rule, width, grow):
    """Black-background lettering -> see-through ink in the wall's colours, each part its own colour:
    orange ink above the heading rule is the heading, the rest of the orange ink is prices and number tags;
    yellow ink is Persian; cream ink is item names, the dimmer grey lines are descriptions. Everything but
    the descriptions is thickened a little so it reads bolder from across the shop. The work is done at the
    high-resolution render; each part is then shrunk on its own to the TV's width (so colours never bleed
    into each other) and thickened by `grow` output pixels."""
    v = a - B
    r = np.maximum(v[..., 0], 1)
    ratio = v[..., 1] / r
    peak = np.abs(v).max(axis=2)
    alpha = np.clip(peak / 228, 0, 1)
    orange, yellow, neutral = ratio < 0.6, (ratio >= 0.6) & (ratio < 0.86), ratio >= 0.86
    alpha = np.where(orange, np.clip(v[..., 0] / 222, 0, 1), alpha)
    alpha = np.where(yellow, np.clip(v[..., 0] / 227, 0, 1), alpha)
    # description rows: neutral ink there never gets as bright as the cream item names
    rowmax = np.where(neutral & (alpha > 0.05), peak, 0).max(axis=1)
    desc_rows = (rowmax > 0) & (rowmax < 205)
    desc = neutral & desc_rows[:, None]
    alpha = np.where(desc, np.clip(alpha / 0.71, 0, 1), alpha)   # full strength, not grey
    ink = alpha >= 0.04
    heading = ink & orange & (np.arange(a.shape[0])[:, None] <= rule + 6 * K)
    parts = {'heading': heading, 'price': ink & orange & ~heading, 'persian': ink & yellow,
             'name': ink & neutral & ~desc, 'desc': ink & desc}
    # each part on its own layer, shrunk and thickened on its own (except descriptions), so colours never bleed
    height = round(a.shape[0] * width / a.shape[1])
    layers = {}
    for name, m in parts.items():
        la = Image.fromarray((np.where(m, alpha, 0) * 255).round().astype(np.uint8))
        la = np.asarray(la.resize((width, height), Image.LANCZOS, reducing_gap=3.0), float) / 255
        if name != 'desc' and grow > 0:
            # grow by a fraction of a pixel: blend in the 1-pixel dilation at that strength
            grown = np.asarray(Image.fromarray((la * 255).round().astype(np.uint8)).filter(ImageFilter.MaxFilter(3)), float) / 255
            la = np.maximum(la, grown * grow)
        layers[name] = np.clip(la, 0, 1)
    names = list(layers)
    stack = np.stack([layers[n] for n in names])
    alpha = stack.max(axis=0)
    pick = stack.argmax(axis=0)
    rgb = np.zeros(alpha.shape + (3,), float)
    for k, n in enumerate(names): rgb[pick == k] = pal[n]
    out = np.dstack([rgb, alpha * 255])
    return Image.fromarray(np.clip(out, 0, 255).round().astype(np.uint8), 'RGBA')

def logo(src=None, k=1):
    """The logo cut out of the original board: everything outside the oval becomes see-through.
    With src (the board rendered at k times), a sharp big copy for the right TV's full-screen slide."""
    src = src or Image.open('site/board-2.png')
    a = np.asarray(src.convert('RGB').crop((372 * k, 40 * k, 843 * k, 262 * k)), float)
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
tmp = tempfile.mkdtemp()
subprocess.run(['pdftoppm', '-png', '-r', str(108 * K), '-f', '1', '-l', '3', PDF, os.path.join(tmp, 'b')], check=True)
boards = {n: Image.open(os.path.join(tmp, f'b-{n}.png')).convert('RGB') for n in (1, 2, 3)}
hi, tight = {}, {}
for name, (b, y0, y1) in SECTIONS.items():
    img, rule = tighten(np.asarray(boards[b].crop((X0 * K, y0 * K, X1 * K, (y1 + 1) * K)), float))
    hi[name] = (img, rule)
    tight[name] = (img[::K], rule)   # board-pixel sizes, for the layout below

# ---- layout, in pixels of a 1920x1080 screen
W, H = 1920.0, 1080.0
M, GAP, PAD = 20.0, 14.0, 12.0          # outer margin, between panels, inside a panel
TOP, BOTTOM = 14.0, 1080 - 96.0         # the allergy bar sits below BOTTOM
pct = lambda v, ref: f'{v / ref * 100:.3f}%'
CW = X1 - X0

def common(mon, css):
    # the bottom bar: only the allergy notice (Ryan, 2 Nov 2026), on both TVs
    css.append(f'.allergy-bar {{ left: {pct(M, W)}; right: {pct(M, W)}; top: {pct(BOTTOM + 10, H)}; height: {pct(H - BOTTOM - 20, H)}; }}')
    logo().save(f'site/monitor-{mon}/logo.png', optimize=True)
    if mon == 2: logo(boards[2], K).save('site/monitor-2/logo-big.webp', quality=88, method=6)

# Inside a panel, the picture fits the box left by the CSS padding (1.48vh) and rim (.36vh) on a 1080 screen.
INSET = 2 * (16 + 3.9)
def save_section(mon, name, box_w, box_h):
    img, rule = hi[name]
    w = min(box_w - INSET, (box_h - INSET) * img.shape[1] / img.shape[0])
    lift(img, PALETTE[mon], rule, int(round(w)), GROW[mon]).save(f'site/monitor-{mon}/sec-{name}.png', optimize=True)

# Left TV: everything, three columns, one scale.
col_w = (W - 2 * M - 2 * GAP) / 3
s1 = (col_w - 2 * PAD) / CW
for i, names in enumerate(STATIC):
    bottom = BOTTOM
    while TOP + sum(tight[n][0].shape[0] * s1 + 2 * PAD for n in names) + GAP * (len(names) - 1) > bottom:
        s1 -= 0.002
css = [f'/* Made by tools/build-walls.py: do not edit by hand. Left TV, everything at once, text scale {s1:.3f}. */']
for i, names in enumerate(STATIC):
    x = M + i * (col_w + GAP)
    y = TOP
    bottom = BOTTOM
    used = sum(tight[n][0].shape[0] * s1 + 2 * PAD for n in names) + GAP * (len(names) - 1)
    grow = (bottom - TOP - used) / sum(tight[n][0].shape[0] for n in names)  # fill the column to the bottom:
    for n in names:                                                         # taller glass, lettering centred
        h = tight[n][0].shape[0] * (s1 + grow) + 2 * PAD
        css.append(f'.sec-{n} {{ left: {pct(x, W)}; top: {pct(y, H)}; width: {pct(col_w, W)}; height: {pct(h, H)}; }}')
        save_section(1, n, col_w, h)
        y += h + GAP
common(1, css)
open('site/monitor-1/layout.css', 'w').write('\n'.join(css) + '\n')

# Right TV: one section at a time on the left, its food animation in a column on the right.
SIDE_W = 520.0
area_x, area_w = M, W - 2 * M - SIDE_W - GAP
area_top, area_bottom = TOP, BOTTOM
s2 = (area_w - 2 * PAD) / CW
tallest = max(t[0].shape[0] for t in tight.values())
s2 = min(s2, (area_bottom - area_top - 2 * PAD) / tallest)
css = [f'/* Made by tools/build-walls.py: do not edit by hand. Right TV, one section at a time, text scale {s2:.3f}. */']
for n, (img, rule) in tight.items():
    h = img.shape[0] * s2 + 2 * PAD
    w = CW * s2 + 2 * PAD
    y = area_top + (area_bottom - area_top - h) / 2
    css.append(f'.tvslide.sec-{n} {{ left: {pct(area_x + (area_w - w) / 2, W)}; top: {pct(y, H)}; width: {pct(w, W)}; height: {pct(h, H)}; }}')
    save_section(2, n, w, h)
css.append(f'.tvslide.soon {{ left: {pct(area_x, W)}; top: {pct(area_top + 60, H)}; width: {pct(area_w, W)}; height: {pct(area_bottom - area_top - 120, H)}; }}')
css.append(f'.side {{ left: {pct(W - M - SIDE_W, W)}; top: {pct(TOP, H)}; width: {pct(SIDE_W, W)}; height: {pct(BOTTOM - TOP, H)}; }}')
common(2, css)
open('site/monitor-2/layout.css', 'w').write('\n'.join(css) + '\n')
print(f'left TV (everything): text {s1 / 0.5:.2f}x the original boards | right TV (one at a time): text {s2 / 0.5:.2f}x')
