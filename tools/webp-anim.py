"""Joins frames (PNG files, in name order) into one looping animated WebP picture, for the shop TVs (they show it
in a plain <img>, so it moves without any code on the TV). Only what changes between frames is stored.
    python3 tools/webp-anim.py <frames-dir> <out.webp> <fps>"""
import sys, glob
from PIL import Image
src, out, fps = sys.argv[1], sys.argv[2], float(sys.argv[3])
frames = [Image.open(f).convert('RGB') for f in sorted(glob.glob(src + '/*.png'))]
frames[0].save(out, 'WEBP', save_all=True, append_images=frames[1:], duration=round(1000 / fps), loop=0,
               quality=82, method=4, kmin=0, kmax=0, allow_mixed=False)
print(out, len(frames), 'frames')
