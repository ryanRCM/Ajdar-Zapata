"""A wooden crate for the cycling TV's line-up slide (Ryan, Nov 2026: food standing on crates at different
heights, like the big chains' "world menu" boards). Drawn in code: a lighter top the food stands on, three
front planks with grain and gaps, corner posts, nails, shading, and "AJDAR ZAPATA" stencilled on the front.
Output: site/monitor-2/crate.webp (see-through background).
    python3 tools/draw-crate.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 720, 496          # the whole picture
TOP = 70                 # height of the top face (seen slightly from above)
rng = np.random.default_rng(7)

def wood(w, h, base, dark, seed):
    """A plank: warm base colour with long grain streaks and a soft knot or two."""
    r = np.random.default_rng(seed)
    y = np.arange(h)[:, None]; x = np.arange(w)[None, :]
    grain = np.zeros((h, w))
    for _ in range(10):
        f, ph, amp, pos = r.uniform(.001, .004), r.uniform(0, 6.3), r.uniform(1, 4), r.uniform(0, h)
        line = pos + amp * np.sin(x * f * 6.3 + ph)
        grain += np.exp(-((y - line) ** 2) / (2 * r.uniform(.8, 2.4) ** 2)) * r.uniform(.15, .45)
    for _ in range(r.integers(0, 2) + 1):
        kx, ky = r.uniform(.15, .85) * w, r.uniform(.3, .7) * h
        d = np.hypot((x - kx) / 2.2, y - ky)
        grain += np.exp(-d ** 2 / 60) * .9
    grain += r.normal(0, .05, (h, w))
    t = np.clip(grain, 0, 1)[..., None]
    col = np.array(base, float) * (1 - t) + np.array(dark, float) * t
    return col

img = np.zeros((H, W, 4), float)
def put(x0, y0, rgb, shade=None):
    h, w = rgb.shape[:2]
    if shade is not None: rgb = rgb * shade[..., None] if shade.ndim == 2 else rgb * shade
    img[y0:y0 + h, x0:x0 + w, :3] = rgb
    img[y0:y0 + h, x0:x0 + w, 3] = 255

LIGHT, MID, DARK = (226, 168, 98), (196, 132, 66), (120, 70, 28)
# top face: two boards, lighter, with a darker back edge
img[0:TOP, 14:W - 14, :3] = (110, 64, 26); img[0:TOP, 14:W - 14, 3] = 255   # the seam between the top boards
for k, (y0, h) in enumerate([(0, 34), (36, 34)]):
    put(14, y0, wood(W - 28, h, LIGHT, MID, 10 + k), np.linspace(.82, 1.0, h)[:, None] * np.ones((1, W - 28)))
# front: three planks with 6 px gaps, a little darker towards the bottom
planks = [(TOP + 6, 136), (TOP + 148, 136), (TOP + 290, 136)]   # ends exactly at H
for k, (y0, h) in enumerate(planks):
    sh = np.linspace(1.0, .86, h)[:, None] * np.ones((1, W))
    put(0, y0, wood(W, h, MID, DARK, 20 + k), sh)
gaps = np.zeros((H, W), bool)
for (y0, h) in planks: gaps[y0 - 6:y0] = True
img[gaps & (np.arange(H)[:, None] > TOP)] = [60, 30, 10, 255]
# corner posts and a darker bottom rail
for x0 in (0, W - 64):
    post = wood(64, H - TOP - 6, (176, 112, 52), (98, 54, 18), 40 + x0)
    sh = np.ones((H - TOP - 6, 64)) * np.linspace(.92, 1.06, 64)[None, :]
    put(x0, TOP + 6, post, np.clip(sh, 0, 1.1))
img[TOP:TOP + 6, :, :3] = (80, 42, 14); img[TOP:TOP + 6, :, 3] = 255     # the lip under the top face

out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), 'RGBA')
d = ImageDraw.Draw(out)
# nails on the posts
for x in (32, W - 32):
    for (y0, h) in planks:
        cy = y0 + h // 2
        d.ellipse((x - 7, cy - 7, x + 7, cy + 7), fill=(70, 62, 56)); d.ellipse((x - 4, cy - 5, x + 2, cy + 1), fill=(150, 140, 130))

# the stencil: AJDAR ZAPATA, dark, slightly worn, centred on the middle plank
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 66)
text = 'AJDAR ZAPATA'
stencil = Image.new('L', (W, H), 0)
sd = ImageDraw.Draw(stencil)
bb = sd.textbbox((0, 0), text, font=font)
tw, th = bb[2] - bb[0], bb[3] - bb[1]
cx, cy = W // 2, planks[1][0] + planks[1][1] // 2
sd.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), text, font=font, fill=255)
s = np.asarray(stencil, float) / 255
# stencil bridges: thin horizontal breaks through the letters, as a cut stencil leaves
s[int(cy - 2):int(cy + 3)] *= 0
wear = rng.uniform(.55, 1, s.shape) * np.asarray(Image.fromarray((rng.random(s.shape) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), float) / 255
s = s * np.clip(.6 + wear, 0, 1) * .85
a = np.asarray(out, float)
ink = np.array([46, 22, 8], float)
a[..., :3] = a[..., :3] * (1 - s[..., None]) + ink * s[..., None]
# overall light from the top left, and a soft dark edge at the bottom
light = np.clip(1.08 - np.arange(H)[:, None] / H * .22 - np.arange(W)[None, :] / W * .08, .7, 1.1)
a[..., :3] *= light[..., None]
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
out.save('site/monitor-2/crate.webp', quality=86, method=6)
print('crate', out.size)
