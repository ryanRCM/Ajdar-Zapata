"""Quick drawn food pictures for the sections that have no photo yet (Ryan, 2 Nov 2026: "for anything that
isn't [a photo], just generate a picture for it, real quick for now"). Shaded, see-through PNGs drawn at
3x and scaled down so the edges are smooth. Real photos replace them later.
    python3 tools/draw-food.py      -> site/monitor-2/art-*.png
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = 3                        # supersampling
W, H = 900, 600
random.seed(4)

def canvas(): return Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))

def shade(img, mask, top, bottom, light=0.0, angle=90):
    """Fill mask with a vertical gradient top->bottom plus an optional soft highlight band."""
    w, h = img.size
    y = np.linspace(0, 1, h)[:, None]
    t, b = np.array(top, float), np.array(bottom, float)
    col = t + (b - t) * y[..., None]
    col = np.broadcast_to(col, (h, w, 3)).copy()
    if light:
        band = np.exp(-((y - 0.25) ** 2) / 0.01) * light
        col = col + (255 - col) * band[..., None]
    layer = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).convert('RGBA')
    layer.putalpha(mask)
    img.alpha_composite(layer)

def shape(fn):
    m = Image.new('L', (W * S, H * S), 0); fn(ImageDraw.Draw(m)); return m

def shadow(img, box, blur=40, a=110):
    m = shape(lambda d: d.ellipse([v * S for v in box], fill=a)).filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new('RGBA', img.size, (60, 20, 0, 0)); sh.putalpha(m); img.alpha_composite(sh)

def gloss(img, box, a=120, blur=12):
    m = shape(lambda d: d.ellipse([v * S for v in box], fill=a)).filter(ImageFilter.GaussianBlur(blur))
    g = Image.new('RGBA', img.size, (255, 255, 255, 0)); g.putalpha(m); img.alpha_composite(g)

def save(img, name):
    img = img.resize((W, H), Image.LANCZOS)
    img = img.crop(img.getbbox())
    img.save(f'site/monitor-2/art-{name}.png', optimize=True); print(name, img.size)

def poly(points): return shape(lambda d: d.polygon([(x * S, y * S) for x, y in points], fill=255))
def ell(box): return shape(lambda d: d.ellipse([v * S for v in box], fill=255))
def rrect(box, r): return shape(lambda d: d.rounded_rectangle([v * S for v in box], r * S, fill=255))

# ---- fries in a red carton
img = canvas(); shadow(img, (250, 540, 650, 590))
for i in range(22):
    x = 300 + i * 14 + random.uniform(-6, 6); top = random.uniform(80, 200); ang = random.uniform(-12, 12)
    dx = math.tan(math.radians(ang)) * (420 - top)
    m = poly([(x, top), (x + 26, top + 4), (x + 26 + dx, 430), (x + dx, 430)])
    shade(img, m, (255, 214, 92), (214, 140, 30), light=0.3)
carton = poly([(260, 300), (640, 300), (600, 570), (300, 570)])
shade(img, carton, (236, 40, 26), (160, 14, 8), light=0.15)
shade(img, poly([(275, 360), (625, 360), (618, 400), (282, 400)]), (255, 236, 200), (240, 210, 170))
gloss(img, (300, 310, 420, 560), a=60, blur=20)
save(img, 'fries')

# ---- hot dog
img = canvas(); shadow(img, (90, 470, 810, 560))
shade(img, rrect((80, 300, 820, 470), 85), (236, 172, 90), (186, 112, 40), light=0.25)        # bottom bun
shade(img, rrect((60, 250, 840, 360), 55), (176, 58, 34), (120, 30, 16), light=0.45)          # sausage
gloss(img, (120, 262, 780, 290), a=140, blur=8)
z = shape(lambda d: d.line([((100 + k * 40) * S, (290 + (18 if k % 2 else -6)) * S) for k in range(18)], fill=255, width=16 * S, joint='curve'))
shade(img, z, (255, 222, 40), (240, 190, 0))                                                   # mustard
shade(img, rrect((100, 200, 800, 290), 70), (244, 186, 100), (204, 128, 50), light=0.35)      # top bun, behind look
save(img, 'hotdog')

# ---- doner baguette
img = canvas(); shadow(img, (60, 470, 840, 560))
shade(img, rrect((50, 330, 850, 480), 70), (236, 180, 100), (190, 120, 50), light=0.2)
for k in range(46):
    x = 80 + k * 16 + random.uniform(-5, 5); y = 300 + random.uniform(-12, 12)
    shade(img, ell((x, y, x + 46, y + 40)), random.choice([(176, 86, 40), (150, 66, 26), (196, 110, 52)]), (110, 46, 18), light=0.2)
for k in range(14):
    x = 90 + k * 52 + random.uniform(-8, 8)
    shade(img, ell((x, 318, x + 36, 344)), (226, 40, 30), (170, 20, 14), light=0.3)
    shade(img, ell((x + 20, 330, x + 64, 352)), (110, 190, 60), (70, 140, 30))
shade(img, rrect((40, 180, 860, 320), 75), (246, 196, 116), (206, 134, 56), light=0.4)
for k in range(30):
    x = 120 + random.uniform(0, 660); y = 205 + random.uniform(0, 40)
    shade(img, ell((x, y, x + 10, y + 6)), (255, 244, 214), (230, 210, 170))
save(img, 'doner')

# ---- shawarma wrap
img = canvas(); shadow(img, (300, 520, 620, 580))
shade(img, poly([(300, 120), (620, 120), (500, 560), (420, 560)]), (240, 214, 160), (200, 160, 100), light=0.25)
for k in range(5):
    y = 170 + k * 70
    shade(img, poly([(320 + k * 24, y), (600 - k * 24, y - 18), (596 - k * 24, y - 6), (322 + k * 24, y + 12)]), (170, 110, 50), (140, 80, 30))
for k in range(18):
    x = 310 + random.uniform(0, 290); y = 80 + random.uniform(0, 50)
    shade(img, ell((x, y, x + 50, y + 40)), random.choice([(176, 86, 40), (150, 66, 26)]), (110, 46, 18), light=0.2)
for k in range(6):
    x = 320 + k * 48
    shade(img, ell((x, 70, x + 40, 100)), (110, 190, 60), (70, 140, 30))
shade(img, poly([(390, 400), (530, 400), (500, 560), (420, 560)]), (226, 230, 236), (150, 156, 164), light=0.5)   # foil
save(img, 'shawarma')

# ---- doner platter
img = canvas(); shadow(img, (80, 470, 820, 580), blur=50)
shade(img, ell((70, 250, 830, 540)), (250, 250, 248), (214, 214, 210), light=0.2)
shade(img, ell((140, 290, 760, 500)), (236, 236, 232), (224, 224, 220))
for k in range(60):
    x = 220 + random.uniform(0, 280); y = 230 + random.uniform(0, 160)
    shade(img, ell((x, y, x + 60, y + 44)), random.choice([(176, 86, 40), (150, 66, 26), (196, 110, 52)]), (110, 46, 18), light=0.25)
for k in range(26):
    x = 520 + random.uniform(0, 170); y = 300 + random.uniform(0, 110)
    shade(img, ell((x, y, x + 46, y + 26)), (110, 190, 60), (70, 140, 30), light=0.2)
for k in range(5):
    x = 560 + k * 30; shade(img, ell((x, 340 + (k % 2) * 30, x + 40, 380 + (k % 2) * 30)), (226, 40, 30), (170, 20, 14), light=0.35)
save(img, 'platter')

# ---- sauces: three glossy pots
img = canvas()
for i, (c1, c2) in enumerate([((230, 40, 26), (160, 14, 8)), ((250, 246, 236), (214, 208, 196)), ((96, 170, 60), (56, 120, 30))]):
    x = 70 + i * 270
    shadow(img, (x - 10, 470, x + 250, 560))
    shade(img, poly([(x, 300), (x + 240, 300), (x + 220, 520), (x + 20, 520)]), (250, 250, 248), (200, 200, 196), light=0.2)
    shade(img, ell((x, 260, x + 240, 340)), (240, 240, 236), (210, 210, 206))
    shade(img, ell((x + 14, 268, x + 226, 332)), c1, c2, light=0.25)
    gloss(img, (x + 50, 278, x + 130, 300), a=170, blur=6)
save(img, 'sauces')

# ---- drinks: a cold cup with a straw and a can
img = canvas(); shadow(img, (150, 500, 760, 580))
shade(img, rrect((480, 230, 690, 560), 26), (226, 228, 232), (150, 154, 160), light=0.45)                 # can
shade(img, rrect((490, 300, 680, 470), 6), (230, 30, 30), (170, 14, 14))
shade(img, poly([(200, 170), (450, 170), (420, 560), (230, 560)]), (236, 40, 26), (160, 14, 8), light=0.2)  # cup
shade(img, poly([(212, 300), (440, 300), (432, 360), (219, 360)]), (255, 255, 255), (240, 240, 240))
shade(img, rrect((180, 150, 470, 190), 18), (252, 252, 250), (220, 220, 216))
shade(img, poly([(340, 20), (360, 20), (350, 160), (330, 160)]), (255, 255, 255), (230, 230, 230))
for k in range(40):
    x = 220 + random.uniform(0, 200); y = 200 + random.uniform(0, 340)
    gloss(img, (x, y, x + 9, y + 12), a=200, blur=1)
save(img, 'drinks')
