"""The sauce names for the right TV's sauce slide (Christmas update, 2 Nov 2026: "big lean in on the sauces").
Each name is lifted straight off the board (menu/Ajdar_Zapata_Boards.pdf, page 1, Sauce selection), English and
Persian separately, never retyped: the PDF is rendered at 3x the board size so the names stay crisp when big.
Output: site/monitor-2/sauces/sauce-<n>-en.png and -fa.png, n = 1..9 in board order (left to right, top
to bottom): Zapata Special Sauce, Garlic, Garlic & Dill, Spicy Chilli, Mushroom, Ketchup, Mayo, Cheddar
Sauce, Green Sauce.
    python3 tools/build-sauces.py
"""
import os, subprocess, tempfile
import numpy as np
from PIL import Image

K = 3
B = np.array([18, 17, 16], float)
EN, FA = (20, 12, 8), (150, 40, 0)   # dark ink for the English, brown-red for the Persian, on bright glass
tmp = tempfile.mkdtemp()
subprocess.run(['pdftoppm', '-png', '-r', str(108 * K), '-f', '1', '-l', '1', 'menu/Ajdar_Zapata_Boards.pdf', os.path.join(tmp, 'b')], check=True)
board = Image.open(os.path.join(tmp, 'b-1.png')).convert('RGB')
# below the section's heading rule, down to the end of the section (board rows 1195..1433, x 60..1154)
a = np.asarray(board.crop((60 * K, 1195 * K, 1154 * K, 1434 * K)), float)
v = a - B
peak = np.abs(v).max(axis=2)
ratio = v[..., 1] / np.maximum(v[..., 0], 1)
ink = peak > 60
yellow = ink & (ratio >= .6) & (ratio < .86)
neutral = ink & (ratio >= .86) & (peak > 150)        # the bright cream names (the grey dividers are dimmer)

def runs(mask, gap):
    """[start, end) spans of True, merging spans separated by fewer than `gap` False entries."""
    out, i = [], 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j < len(mask) and mask[j]: j += 1
            if out and i - out[-1][1] < gap: out[-1][1] = j
            else: out.append([i, j])
            i = j
        else:
            i += 1
    return out

text = yellow | neutral
# three equal columns on the board (each name's English sits left, its Persian right, so split by position)
cols = [[0, 360 * K], [362 * K, 732 * K], [734 * K, a.shape[1]]]
rows = runs(text.any(axis=1), 14 * K)
assert len(rows) == 3, rows
n = 0
for r0, r1 in rows:
    for c0, c1 in cols:
        n += 1
        for part, m, col in (('en', neutral, EN), ('fa', yellow, FA)):
            cell = m[r0:r1, c0:c1]
            ys, xs = np.nonzero(cell)
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            box = (slice(r0 + y0 - K, r0 + y1 + K), slice(c0 + x0 - K, c0 + x1 + K))
            alpha = np.clip((peak[box] - 20) / 200, 0, 1)
            # keep only this part's ink (and its soft anti-aliased edge, which is too dim to tell apart by colour)
            fam = (ratio[box] >= .86) if part == 'en' else ((ratio[box] >= .6) & (ratio[box] < .86))
            alpha = np.where(fam | (peak[box] < 120), alpha, 0)
            img = np.dstack([np.full(alpha.shape, c, float) for c in col] + [alpha * 255])
            Image.fromarray(img.round().astype(np.uint8), 'RGBA').save(f'site/monitor-2/sauces/sauce-{n}-{part}.png', optimize=True)
        print(n, 'cell', (r1 - r0) // K, 'x', (c1 - c0) // K)
