"""Marbled backgrounds like the shop's chair covers (Ryan, 2 Nov 2026): swirling liquid streaks with bubble
cells, in an orange version (right TV) and a yellow version (left TV). Made once, saved as JPEGs, so the TVs
only show a picture (no work for their processors).

How: smooth random noise (several sizes added together), sampled at positions that are themselves pushed
around by more noise (domain warping) gives flowing marble streaks. The value is mapped through a colour
ramp, and bubble cells (pale centre, darker rim) are scattered along the light streaks.
    python3 tools/make-marble.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1920, 1080
rng = np.random.default_rng(7)

def smooth_noise(w, h, cells):
    small = rng.random((cells, int(cells * h / w) + 2)).astype(np.float32)
    return np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255

def fbm(w, h, base=5, octaves=4):
    out = np.zeros((h, w), np.float32); amp = 1.0; total = 0
    for o in range(octaves):
        out += amp * smooth_noise(w, h, base * 2 ** o); total += amp; amp *= 0.5
    return out / total

def sample(field, x, y):
    h, w = field.shape
    x = np.clip(x, 0, w - 1.001); y = np.clip(y, 0, h - 1.001)
    x0 = x.astype(int); y0 = y.astype(int); fx = x - x0; fy = y - y0
    a = field[y0, x0]; b = field[y0, x0 + 1]; c = field[y0 + 1, x0]; d = field[y0 + 1, x0 + 1]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy

def marble(seed):
    global rng
    rng = np.random.default_rng(seed)
    w, h = W // 2, H // 2
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n1, n2, n3 = fbm(w, h, 3), fbm(w, h, 4), fbm(w, h, 2, 5)
    # warp twice: q pushes the sample point, r pushes it again (flowing, folded streaks)
    qx = sample(n1, xx, yy) * 380; qy = sample(n2, xx, yy) * 260
    rx = sample(n2, xx + qx, yy + qy) * 340; ry = sample(n1, xx + qx * .7, yy + qy * .7) * 260
    f = sample(n3, xx + rx, yy + ry)
    # a gentle diagonal flow, like the fabric, folded by the noise
    f = 0.9 * f + 0.1 * (np.sin((xx * 0.003 + yy * 0.006) * 6.283 + f * 9) * 0.5 + 0.5)
    f = (f - f.min()) / (f.max() - f.min())
    # sharpen into marbled bands: steeper steps between colours
    f = 0.5 + 0.5 * np.tanh((f - 0.5) * 2.8)   # smooth, never flat at the ends
    return f

def ramp(f, stops):
    xs = np.array([s[0] for s in stops]); cs = np.array([s[1] for s in stops], np.float32)
    out = np.zeros(f.shape + (3,), np.float32)
    for k in range(3): out[..., k] = np.interp(f, xs, cs[:, k])
    return out

def cells(img, f, ring, fill, glint, count, seed):
    """Bubble cells in clusters along the light streaks: soft-edged, a darker rim, mixed fills
    (pale cream, peach, a few grey-lilac), small ones crowding round the big ones, like the chair fabric."""
    r = np.random.default_rng(seed)
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, 'RGBA')
    h, w = f.shape
    fills = [fill, glint, (186, 166, 170, 235), (255, 200, 160, 235)]
    centres = []
    tries = 0
    while len(centres) < count // 9 and tries < 5000:   # cluster centres in the lightest streaks
        tries += 1
        x, y = int(r.integers(0, W)), int(r.integers(0, H))
        if f[min(h - 1, y // 2), min(w - 1, x // 2)] > 0.72: centres.append((x, y))
    for cx, cy in centres:
        for _ in range(int(r.integers(4, 14))):
            x = int(cx + r.normal(0, 46)); y = int(cy + r.normal(0, 26))
            if not (0 <= x < W and 0 <= y < H) or f[min(h - 1, y // 2), min(w - 1, x // 2)] < 0.55: continue
            rad = int(r.choice([3, 5, 7, 9, 12, 16, 21], p=[.24, .22, .17, .14, .11, .08, .04]))
            col = fills[int(r.choice(4, p=[.5, .2, .15, .15]))]
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=ring)
            inner = max(2, int(rad * r.uniform(0.62, 0.8)))
            d.ellipse([x - inner, y - inner, x + inner, y + inner], fill=col)
    layer = layer.filter(ImageFilter.GaussianBlur(1.1))
    img.alpha_composite(layer) if img.mode == 'RGBA' else img.paste(layer, (0, 0), layer)

def make(name, stops, ring, fill, glint, seed):
    f = marble(seed)
    rgb = ramp(f, stops)
    d = np.abs(((f * 6 + 0.5) % 1) - 0.5)                  # distance to the nearest band edge
    vein = np.exp(-(d ** 2) / 0.0006) * (f > 0.08) * (f < 0.92)   # thin bright lines along band edges
    rgb = rgb + (np.array(stops[-1][1], np.float32) - rgb) * (vein[..., None] * 0.35)
    img = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    cells(img, f, ring, fill, glint, 260, seed + 1)
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    img.save(f'site/{name}', quality=84, optimize=True, progressive=True)
    print(name, 'done')

# right TV: orange marble (deep red, red-orange, orange, light orange, cream)
make('marble-orange.jpg',
     [(0, (196, 66, 0)), (.22, (232, 98, 0)), (.42, (250, 128, 8)), (.6, (255, 160, 30)), (.78, (255, 192, 90)), (1, (255, 232, 180))],  # warm orange: TVs push red
     ring=(206, 96, 10, 235), fill=(255, 226, 180, 240), glint=(255, 248, 230, 230), seed=11)
# left TV: yellow marble (amber, golden, yellow, pale yellow, cream)
make('marble-yellow.jpg',
     [(0, (214, 104, 0)), (.22, (240, 150, 0)), (.42, (255, 190, 10)), (.6, (255, 214, 40)), (.78, (255, 232, 120)), (1, (255, 246, 210))],
     ring=(214, 130, 10, 235), fill=(255, 246, 214, 240), glint=(255, 255, 248, 230), seed=23)
