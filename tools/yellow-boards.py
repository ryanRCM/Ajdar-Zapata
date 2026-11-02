"""Make Monitor 1's yellow boards (left wall) from the black ones: site/board-N.png -> site/monitor-1/board-N.png.

Ryan, 2 Nov 2026: "yellow and orange theme. The left wall is yellow, the right wall is orange. Mainly yellow."
Every pixel is recoloured by how much "ink" it carries over the black background: plain background
becomes yellow, full-strength type (orange headings and prices, cream names) becomes black, and lighter
grey small print becomes a dark brown, so the hierarchy stays. Number tags turn black with yellow numbers.
Text and prices are not redrawn, only recoloured. The logo (above row 265) keeps its own colours: only
the plain background around it, reached from the edges, turns yellow.
Run: python3 tools/yellow-boards.py   (re-run after making new boards from a new PDF)
"""
import numpy as np
from PIL import Image

B = np.array([18, 17, 16], float)    # board black  #121110
Y = np.array([255, 198, 26], float)  # wall yellow  #ffc61a
K = np.array([18, 17, 16], float)    # ink on yellow
LOGO_END = 265                        # first blank row under the logo (12.3% of 2160)

def outside_mask(near):
    """Background pixels connected to the band's left, right or bottom edge."""
    out = np.zeros_like(near)
    out[:, 0] = out[:, -1] = out[-1, :] = True
    out &= near
    while True:
        g = out.copy()
        g[1:] |= out[:-1]; g[:-1] |= out[1:]; g[:, 1:] |= out[:, :-1]; g[:, :-1] |= out[:, 1:]
        g &= near
        if (g == out).all():
            return out
        out = g

for n in (1, 2, 3):
    a = np.asarray(Image.open(f'site/board-{n}.png').convert('RGB'), float)
    ink = np.clip(np.abs(a - B).max(axis=2, keepdims=True) / 200, 0, 1)
    out = Y + (K - Y) * ink
    top = a[:LOGO_END]
    dist = np.abs(top - B).max(axis=2, keepdims=True)
    w = np.clip(1 - dist / 40, 0, 1) * outside_mask(dist[..., 0] < 40)[..., None]
    logo = top + (Y - B) * w
    logo[:20] = out[:20]  # the top bar, like the rest of the board
    out[:LOGO_END] = logo
    img = Image.fromarray(np.clip(out, 0, 255).round().astype(np.uint8))
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(f'site/monitor-1/board-{n}.png', optimize=True)
    print(n, 'done')
