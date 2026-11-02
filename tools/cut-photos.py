"""Cut Ryan's clean studio food photos (menu/photos/, white backgrounds, no watermarks) off their
backgrounds for the right TV (Ryan, 2 Nov 2026: real pictures instead of drawn food). The stack of three
subs is split into its three subs. Output: site/monitor-2/photo-*.webp (see-through background).
Only photos without other companies' watermarks are used (several of the sent photos carry
"Snapp! Food" or other sites' marks).
    python3 tools/cut-photos.py
"""
import numpy as np
from PIL import Image, ImageFilter

def cutout(img):
    a = np.asarray(img.convert('RGB'), float)
    light = a.min(axis=2) > 222                    # white-ish
    flat = (a.max(axis=2) - a.min(axis=2)) < 22    # and not coloured
    near = light & flat
    out = np.zeros_like(near); out[0, :] = out[-1, :] = out[:, 0] = out[:, -1] = True; out &= near
    while True:                                     # background = white reachable from the edges
        g = out.copy(); g[1:] |= out[:-1]; g[:-1] |= out[1:]; g[:, 1:] |= out[:, :-1]; g[:, :-1] |= out[:, 1:]; g &= near
        if (g == out).all(): break
        out = g
    alpha = Image.fromarray(((~out) * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = img.convert('RGB').copy(); rgba.putalpha(alpha)
    return rgba.crop(rgba.getbbox())

def save(im, name, width=900):
    if im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(f'site/monitor-2/photo-{name}.webp', quality=86, method=6)
    print(name, im.size)

save(cutout(Image.open('menu/photos/salami-sausage-sub.jpg')), 'salami-sub')
save(cutout(Image.open('menu/photos/minced-meat-sub.jpg')), 'minced-sub')
stack = Image.open('menu/photos/three-subs.jpg').convert('RGB')
a = np.asarray(stack, float)
rows = ~((a.min(axis=2) > 222).mean(axis=1) > 0.985)     # rows with food on them
bands, y = [], 0
while y < len(rows):
    if rows[y]:
        e = y
        while e < len(rows) and rows[e]: e += 1
        if e - y > 60: bands.append((max(0, y - 6), min(len(rows), e + 6)))
        y = e
    else:
        y += 1
print('subs found in the stack:', len(bands))
for (y0, y1), name in zip(bands, ['chicken-fillet-sub', 'beef-patty-sub', 'salami-steak-sub']):
    save(cutout(stack.crop((0, y0, stack.width, y1))), name)

# Ryan's second batch (2 Nov): the doner platter on white (cut out), and the wraps on a blue table
# (busy background: kept whole, shown with rounded corners).
save(Image.open('menu/photos/doner-fries-platter.jpg').convert('RGB'), 'doner-platter', width=700)  # grey background: framed, not cut out
wraps = Image.open('menu/photos/doner-wraps-tray.jpg').convert('RGB')
w, h = wraps.size
save(wraps.crop((0, int(h * 0.45), w, h)), 'shawarma-wraps', width=700)

# Ryan's sauce pots (2 Nov): spicy chilli, cheddar, garlic & dill, on white -> cut out.
for n in ('spicy-chilli', 'cheddar', 'garlic-dill'):
    save(cutout(Image.open(f'menu/photos/sauce-{n}.jpg')), f'sauce-{n}', width=400)
