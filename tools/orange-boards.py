"""Make Monitor 2's orange boards from the black ones: site/board-N.png -> site/monitor-2/board-N.png.

Ryan, 2 Nov 2026: "Background ORANGE not black". Painting only the background orange would hide
the orange prices and headings, so the two colours swap. Every pixel p becomes black + orange - p:
black background -> orange, orange type -> black, cream type -> near-black.
Antialiased edges stay smooth because the swap is linear. The logo (above row 265) keeps its own
colours: only the plain background around it, reached from the edges, turns orange. Text and prices are not redrawn, only recoloured.
Run: python3 tools/orange-boards.py
"""
import numpy as np
from PIL import Image

B = np.array([18, 17, 16], float)    # board black  #121110
O = np.array([240, 124, 26], float)  # board orange #f07c1a
LOGO_END = 265                        # first blank row under the logo (12.3% of 2160)

for n in (1, 2, 3):
    a = np.asarray(Image.open(f'site/board-{n}.png').convert('RGB'), float)
    out = np.clip(B + O - a, 0, 255)
    # Logo band: keep the artwork, turn only the plain background orange (soft edge), keep the top bar swapped.
    top = a[:LOGO_END]
    dist = np.abs(top - B).max(axis=2, keepdims=True)
    w = np.clip(1 - dist / 40, 0, 1)
    # Only background reachable from the band's edges counts: the logo's own dark inside stays as drawn.
    near = (dist[..., 0] < 40)
    outside = np.zeros_like(near)
    outside[:, 0] = outside[:, -1] = outside[-1, :] = True
    outside &= near
    while True:
        grown = outside.copy()
        grown[1:] |= outside[:-1]; grown[:-1] |= outside[1:]
        grown[:, 1:] |= outside[:, :-1]; grown[:, :-1] |= outside[:, 1:]
        grown &= near
        if (grown == outside).all(): break
        outside = grown
    w = w * outside[..., None]
    logo = top + (O - B) * w
    bar = np.zeros(top.shape[:2], bool); bar[:20] = True  # the board's top orange bar (rows 0-19)
    logo[bar] = out[:LOGO_END][bar]
    out[:LOGO_END] = logo
    img = Image.fromarray(out.round().astype(np.uint8))
    # 256 colours with dithering: looks the same, and about 150 KB a board instead of 350 KB.
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(f'site/monitor-2/board-{n}.png', optimize=True)
    print(n, 'done')
