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
# Left TV: the whole menu at once, three columns (the last one is next to the middle of the pair, above
# half the logo). Right TV: one section at a time, as big as the screen allows (Ryan, 2 Nov 2026: "one of
# them static with everything, the other one cycling big").
STATIC = [['starters', 'sauces'], ['sandwiches', 'burgers', 'drinks'], ['doner', 'platters', 'shawarma', 'hotdogs']]
# Colours on each wall (Ryan, 2 Nov 2026: "different colours ... very nice", like the big chains' boards:
# strong red prices, dark headings, black item names, high contrast on bright glass).
#   heading: section titles · price: prices and number tags · persian: Persian names · name: English item
#   names · desc: the small descriptions
PALETTE = {1: {'heading': (120, 10, 0), 'price': (222, 22, 10), 'persian': (168, 58, 0), 'name': (14, 10, 8), 'desc': (72, 52, 36)},
           2: {'heading': (110, 6, 0), 'price': (206, 14, 30), 'persian': (150, 46, 0), 'name': (14, 10, 8), 'desc': (70, 46, 34)}}
CAP = 16  # longest blank gap kept inside a section, in board pixels (down)
HCAP = 34  # longest blank gap kept across a row (between a name and its price)

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
    # the same across: cap the empty space between names and prices (full-width lines are ignored when
    # looking for it, and simply come out shorter)
    ink2 = np.abs(out - B).max(axis=2) > 30
    lines = ink2.mean(axis=1) > 0.5
    cols = ink2[~lines].any(axis=0)
    keepc = np.ones(len(cols), bool)
    x = 0
    while x < len(cols):
        if not cols[x]:
            e = x
            while e < len(cols) and not cols[e]: e += 1
            if x > 0 and e < len(cols) and e - x > HCAP: keepc[x + HCAP:e] = False
            x = e
        else:
            x += 1
    out = out[:, keepc]
    # heading rule: the first thick full-width orange band
    o = (np.abs(out - np.array([240, 124, 26])).max(axis=2) < 60).mean(axis=1) > 0.8
    rule = int(np.argmax(o)) if o.any() else 60
    return out, rule

def lift(a, pal, rule):
    """Black-background lettering -> see-through ink in the wall's colours, each part its own colour:
    orange ink above the heading rule is the heading, the rest of the orange ink is prices and number tags;
    yellow ink is Persian; cream ink is item names, the dimmer grey lines are descriptions. Everything but
    nothing is thickened (Ryan: thickening closed up the 6s and 9s)."""
    from PIL import ImageFilter
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
    heading = ink & orange & (np.arange(a.shape[0])[:, None] <= rule + 6)
    parts = {'heading': heading, 'price': ink & orange & ~heading, 'persian': ink & yellow,
             'name': ink & neutral & ~desc, 'desc': ink & desc}
    # each part on its own layer, thickened on its own (except descriptions), so colours never bleed
    layers = {}
    for name, m in parts.items():
        la = np.where(m, alpha, 0)
        layers[name] = la
    names = list(layers)
    stack = np.stack([layers[n] for n in names])
    alpha = stack.max(axis=0)
    pick = stack.argmax(axis=0)
    rgb = np.zeros(a.shape[:2] + (3,), float)
    for k, n in enumerate(names): rgb[pick == k] = pal[n]
    out = np.dstack([rgb, alpha * 255])
    return Image.fromarray(np.clip(out, 0, 255).round().astype(np.uint8), 'RGBA')

def logo(src=None, k=1):
    """The logo cut out of the original board: everything outside the oval becomes see-through.
    With src (the board rendered at k times), a sharp big copy."""
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

def logo_big():
    """A sharp big copy of the logo for the right TV's Christmas slide: the logo cut from the PDF rendered at 3x."""
    import os, subprocess, tempfile
    tmp = tempfile.mkdtemp()
    subprocess.run(['pdftoppm', '-png', '-r', '324', '-f', '2', '-l', '2', 'menu/Ajdar_Zapata_Boards.pdf', os.path.join(tmp, 'b')], check=True)
    logo(Image.open(os.path.join(tmp, 'b-2.png')), 3).save('site/monitor-2/logo-big.webp', quality=88, method=6)

# ---- measure every section once (sizes are the same on both walls)
boards = {n: np.asarray(Image.open(f'site/board-{n}.png').convert('RGB'), float) for n in (1, 2, 3)}
tight = {}
for name, (b, y0, y1) in SECTIONS.items():
    tight[name] = tighten(boards[b][y0:y1 + 1, X0:X1])

# ---- sauces: the board prints them small in a 3-across grid. Rebuild them as a list like the other
# sections (Ryan, 2 Nov 2026: the sauces must be big): one sauce per row, English left, Persian right,
# each name cut straight from the board (never retyped) and enlarged to match the other sections' names.
def sauce_list():
    b, y0, y1 = SECTIONS['sauces']
    src = boards[b][y0:y1 + 1, X0:X1]
    head = src[:76]                                   # title, Persian title and the rule
    cells_x = [(0, 365), (370, 735), (740, 1094)]     # the grid's three columns
    rows_y = [((88, 111), (119, 144)), ((170, 193), (200, 226)), ((252, 275), (283, 308))]  # (English, Persian)
    def cut(y, x):
        part = src[y[0]:y[1], x[0]:x[1]]
        ink = np.abs(part - B).max(axis=2) > 30
        xs = np.where(ink.any(axis=0))[0]
        return part[:, xs.min() - 1:xs.max() + 2]
    def up(img, k=1.45):
        im = Image.fromarray(img.astype(np.uint8)).resize((round(img.shape[1] * k), round(img.shape[0] * k)), Image.LANCZOS)
        return np.asarray(im, float)
    width = head.shape[1]
    lines = [head, np.tile(B, (18, width, 1))]
    for (ey, fy) in rows_y:
        for x in cells_x:
            en, fa = up(cut(ey, x)), up(cut(fy, x))
            h = max(en.shape[0], fa.shape[0])
            row = np.tile(B, (h, width, 1))
            row[(h - en.shape[0]) // 2:(h - en.shape[0]) // 2 + en.shape[0], 8:8 + en.shape[1]] = en
            row[(h - fa.shape[0]) // 2:(h - fa.shape[0]) // 2 + fa.shape[0], width - 8 - fa.shape[1]:width - 8] = fa
            lines += [row, np.tile(B, (22, width, 1))]
    out = np.vstack(lines + [np.tile(B, (10, width, 1))])
    return out, tight['sauces'][1]

tight['sauces'] = sauce_list()

# ---- layout, in pixels of a 1920x1080 screen
W, H = 1920.0, 1080.0
M, GAP, PAD = 14.0, 12.0, 10.0          # outer margin, between panels, inside a panel
TOP = 12.0
BOTTOM1 = H - 12.0                      # left TV: no bottom bar (allergy notice only on the right TV)
BOTTOM2 = H - 96.0                      # right TV: the allergy bar sits below this
pct = lambda v, ref: f'{v / ref * 100:.3f}%'
size = {n: (t[0].shape[1], t[0].shape[0]) for n, t in tight.items()}   # (width, height) in board pixels

def common(mon, css):
    if mon == 2:  # the allergy notice, on the right TV only (Ryan, 2 Nov 2026: "only in one section")
        css.append(f'.allergy-bar {{ left: {pct(M, W)}; right: {pct(M, W)}; top: {pct(BOTTOM2 + 10, H)}; height: {pct(H - BOTTOM2 - 20, H)}; }}')
    logo().save(f'site/monitor-{mon}/logo.png', optimize=True)
    if mon == 2: logo_big()

for mon in (1, 2):
    for name, (img, rule) in tight.items():
        lift(img, PALETTE[mon], rule).save(f'site/monitor-{mon}/sec-{name}.png', optimize=True)

# Left TV: everything at once. Each column is as wide as its widest section needs, all at one text scale,
# as big as both the screen's width and each column's height allow.
def col_w_board(names): return max(size[n][0] for n in names)
def col_h_board(names): return sum(size[n][1] for n in names)
fixed_w = 2 * M + GAP * (len(STATIC) - 1) + 2 * PAD * len(STATIC)
s1 = (W - fixed_w) / sum(col_w_board(c) for c in STATIC)
for names in STATIC:
    s1 = min(s1, (BOTTOM1 - TOP - GAP * (len(names) - 1) - 2 * PAD * len(names)) / col_h_board(names))
css = [f'/* Made by tools/build-walls.py: do not edit by hand. Left TV, everything at once, text scale {s1:.3f}. */']
extra_w = (W - fixed_w - s1 * sum(col_w_board(c) for c in STATIC)) / len(STATIC)   # share any spare width
x = M
for names in STATIC:
    cw = col_w_board(names) * s1 + 2 * PAD + extra_w
    used = sum(size[n][1] * s1 + 2 * PAD for n in names) + GAP * (len(names) - 1)
    grow = (BOTTOM1 - TOP - used) / len(names)          # panels share the leftover height: fill to the bottom
    y = TOP
    for n in names:
        h = size[n][1] * s1 + 2 * PAD + grow
        css.append(f'.sec-{n} {{ left: {pct(x, W)}; top: {pct(y, H)}; width: {pct(cw, W)}; height: {pct(h, H)}; }}')
        y += h + GAP
    x += cw + GAP
common(1, css)
open('site/monitor-1/layout.css', 'w').write('\n'.join(css) + '\n')

# Right TV: one section at a time, each scaled to fill the space beside the food column.
SIDE_W = 520.0
area_x, area_w = M, W - 2 * M - SIDE_W - GAP
area_top, area_bottom = TOP, BOTTOM2
css = ['/* Made by tools/build-walls.py: do not edit by hand. Right TV, one section at a time, each as big as fits. */']
scales = []
for n, (w0, h0) in size.items():
    s2 = min((area_w - 2 * PAD) / w0, (area_bottom - area_top - 2 * PAD) / h0)
    scales.append(s2)
    w, h = w0 * s2 + 2 * PAD, h0 * s2 + 2 * PAD
    css.append(f'.tvslide.sec-{n} {{ left: {pct(area_x + (area_w - w) / 2, W)}; top: {pct(area_top + (area_bottom - area_top - h) / 2, H)}; width: {pct(w, W)}; height: {pct(h, H)}; }}')
css.append(f'.side {{ left: {pct(W - M - SIDE_W, W)}; top: {pct(TOP, H)}; width: {pct(SIDE_W, W)}; height: {pct(BOTTOM2 - TOP, H)}; }}')
common(2, css)
open('site/monitor-2/layout.css', 'w').write('\n'.join(css) + '\n')
print(f'left TV (everything): text {s1 / 0.5:.2f}x the original boards (was 1.08x) | right TV: {min(scales) / 0.5:.2f}x to {max(scales) / 0.5:.2f}x (was 2.42x for all)')
