"""The takeaway leaflet, built from tools/make-menu.py so it can never drift from the TVs and the A4.
Ryan, 26 Nov 2026: "a leaflet with the menu in it, no ingredients, with the address and phone, no food allergy; at the
bottom the offer"; 27 Nov 2026: his version (Grand Opening, the food photo, Chicken Shawarma featured, "Visit Ajdar
Zapata") with "the background orange" and the A4 in the same palette (tools/print_palette.py).
Double-sided A5 (148 x 210 mm). Front: logo, GRAND OPENING, the photo, Starters, Sandwiches, Burgers, Doner Baguettes,
address and phone. Back: the photo, the featured item (name and price from the list), Platters, Shawarma, Hot Dogs,
Sauces and Drinks, the loyalty card word for word, then Visit Ajdar Zapata with the address and phone.
Writes menu/leaflet/Main.dc.html (front) and Back.dc.html (back), the two artboards of Ryan's Claude Design artifact
"Ajdar Zapata Leaflet" (https://claude.ai/artifact/89Tw2CpFz5xUPwB4HESdyz), and menu/leaflet/assets.json (which upload
is which local file, for the PDF); the PDF: node tools/a4-pdf.cjs leaflet -> menu/Ajdar_Zapata_Leaflet_A5.pdf.
The photo (menu/leaflet/photo.jpg, and the wraps cut from it) is from Ryan's own leaflet ("Food images are illustrative.").
The pictures bleed off the top corners and the black bar along the bottom (.foot) carries the address, as on his version.
K1/K2 scale the menu text so each side is full (0.81 and 0.8 on 27 Nov; lower one if a side runs into the black bar).
    python3 tools/leaflet.py
"""
import html, json, os, re, runpy
from print_palette import ORANGE, INK, BROWN, SOFT, RULE, BAR_CSS

g = runpy.run_path('tools/make-menu.py')
PAGES, SAUCES, DRINKS = g['PAGES'], g['SAUCES'], g['DRINKS']
e = html.escape
secs = {t: (fa, items) for _, _, ss in PAGES for t, fa, items in ss if isinstance(items, list)}
items = {x['n']: x for fa, its in secs.values() for x in its}
W, H = 559, 794   # A5 at 96 px to the inch
LOGO = '/_blob/cf0e3e5a629b743fcaa2dba8defe4817'    # the leaflet artifact's upload of menu/a4/logo.png
PHOTO = '/_blob/3ccd67438563e5f29caed24f6d30de72'   # the leaflet artifact's upload of menu/leaflet/photo.jpg (front)
WRAPS = '/_blob/d9e71a39c89b647ba3c36eb8436cbfe3'   # ... of menu/leaflet/photo-wraps.jpg (back: the wraps cut from the same photo)
ASSETS = {LOGO.split('/')[-1]: 'menu/a4/logo.png', PHOTO.split('/')[-1]: 'menu/leaflet/photo.jpg', WRAPS.split('/')[-1]: 'menu/leaflet/photo-wraps.jpg'}
PHONE = '020 8259 4026'
ADDRESS = '864 High Road, London N12 9RH'
FEATURE = 30   # Chicken Shawarma, as on Ryan's version: its name and price come from the list
# the offer: the shop's loyalty card, word for word (Ryan's photo, 26 Nov 2026 16:05)
OFFER = {'title': 'LOYALTY CARD · DAILY REWARDS', 'lines': ['£10 = 1 STAMP · £20+ = 2 STAMPS · ONE ORDER PER DAY'], 'big': '5 STAMPS · 1 FREE SHAWARMA'}

CSS = BAR_CSS + f"""
body{{margin:0}}
.h{{padding:3px 9px 2px;margin:0 0 1px}}
.r{{display:flex;align-items:center;gap:8px;border-bottom:1px solid {RULE};padding:1.5px 0}}
.t{{flex:1;min-width:0;font:700 14.5px/1.1 'Barlow Condensed';text-transform:uppercase;color:{INK}}}
.f{{font:700 12.5px/1.15 Vazirmatn;color:{BROWN};direction:rtl;white-space:nowrap}}
.p{{flex:0 0 auto;min-width:46px;text-align:right;font:800 16px/1 'Barlow Condensed';color:{INK};white-space:nowrap}}
.s{{display:flex;justify-content:space-between;align-items:baseline;gap:6px;border-bottom:1px solid {RULE};padding:2px 0}}
.s span{{font:700 13px 'Barlow Condensed';color:{INK};text-transform:uppercase}}
.s em{{font:600 11.5px Vazirmatn;color:{BROWN};font-style:normal;direction:rtl}}
.s strong{{font:800 14px 'Barlow Condensed';color:{INK}}}
.dn{{display:inline-block;width:19px;color:{INK};font-weight:800}}
.sec{{margin-bottom:5px}}
.pg{{}}"""


def scss(k):
    return re.sub(r'(\d+(?:\.\d+)?)px', lambda m: f'{float(m.group(1)) * k:.2f}px' if float(m.group(1)) > 2 else m.group(0), CSS)


def row(x):
    pr = e(x['price']).replace(' · ', '<br>')
    return (f'<div class="r"><span class="n">{x["n"]}</span><span class="t">{e(x["en"])}</span>'
            f'<span class="f">{e(x["fa"])}</span><span class="p">{pr}</span></div>')


def sec(t):
    fa, its = secs[t]
    return f'<div class="sec"><div class="h"><b>{e(t)}</b><i>{e(fa)}</i></div>' + ''.join(row(x) for x in its) + '</div>'


NOTE = f'<div style="font: 400 8px/1 Barlow, sans-serif; color: {BROWN}; margin: 2px 0 5px">Food images are illustrative.</div>'


def photo(src, side, w, h, pos):
    # bleeds off the top corner on `side`, with a black edge and a rounded inner corner
    other = 'left' if side == 'right' else 'right'
    return (f'<div style="position: absolute; top: 0; {side}: 0; width: {w}px; height: {h}px; box-sizing: border-box; overflow: hidden; '
            f'border-{other}: 4px solid {INK}; border-bottom: 4px solid {INK}; border-bottom-{other}-radius: 26px">'
            f'<img src="{src}" alt="Ajdar Zapata food" style="width: 100%; height: 100%; object-fit: cover; object-position: {pos}; display: block"></div>')


def foot(inner, h):
    return f'<div class="foot" style="position: absolute; left: 0; right: 0; bottom: 0; height: {h}px; background: {INK}; box-sizing: border-box; padding: 0 22px; display: flex; align-items: center">{inner}</div>'


def page(title, inner, k, fh):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&amp;family=Barlow:wght@400;500;600&amp;family=Vazirmatn:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>
{scss(k)}
</style>
</helmet>
<div style="width: {W}px; height: {H}px; box-sizing: border-box; background: {ORANGE}; position: relative; overflow: hidden; padding: 14px 22px {fh}px; display: flex; flex-direction: column; color: {INK}" class="pg">
{inner}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''


FH1, FH2 = 40, 56   # the black bar along the bottom, front and back
front = (photo(PHOTO, 'right', 294, 178, '50% 64%')
         + f'''<div style="width: 210px; height: 166px; display: flex; flex-direction: column; justify-content: space-between">
<img src="{LOGO}" alt="Ajdar Zapata Sandwich" style="width: 150px; height: 73px; object-fit: contain; object-position: left center">
<div style="font: 800 52px/0.9 'Barlow Condensed', sans-serif; color: {INK}; letter-spacing: 1px">GRAND<br>OPENING</div>
</div>
{NOTE}'''
         + ''.join(sec(t) for t in ['STARTERS & SIDES', 'SANDWICHES', 'BURGERS', 'DONER BAGUETTES'])
         + foot(f'''<div style="flex: 1; display: flex; justify-content: space-between; align-items: center">
<span style="font: 600 13px Barlow, sans-serif; color: #fff">{ADDRESS}</span>
<span style="font: 800 23px/1 'Barlow Condensed', sans-serif; color: {ORANGE}; letter-spacing: .5px">{PHONE}</span></div>''', FH1))

fx = items[FEATURE]
sauces = ''.join(f'<div class="s"><span>{e(a)}</span><em>{e(b)}</em></div>' for a, b in SAUCES)
drinks = ''.join(f'<div class="s"><span><b class="dn">{n}</b>{e(a)} <em>{e(b)}</em></span><strong>{p}</strong></div>' for n, a, b, p in DRINKS)
offer = (f'<div style="margin-top: 6px; background: {INK}; color: {ORANGE}; border-radius: 8px; padding: 5px 12px 6px; text-align: center">'
         f'<div style="font: 800 18px/1.1 \'Barlow Condensed\', sans-serif; letter-spacing: 1px">{e(OFFER["title"])}</div>'
         + ''.join(f'<div style="font: 700 13.5px/1.25 \'Barlow Condensed\', sans-serif; margin-top: 2px; color: #fff">{e(l)}</div>' for l in OFFER['lines'])
         + f'<div style="font: 800 19px/1.1 \'Barlow Condensed\', sans-serif; margin-top: 3px; color: {INK}; background: {ORANGE}; border-radius: 6px; padding: 2px 10px; display: inline-block">{e(OFFER["big"])}</div></div>')
back = (photo(WRAPS, 'left', 262, 172, '50% 50%')
        + f'''<div style="margin-left: 250px; height: 162px; display: flex; flex-direction: column; justify-content: center; align-items: flex-end; text-align: right">
<img src="{LOGO}" alt="Ajdar Zapata Sandwich" style="width: 132px; height: 64px; object-fit: contain; object-position: right center">
<div style="font: 800 26px/1 'Barlow Condensed', sans-serif; color: {INK}; margin-top: 8px; text-transform: uppercase">{e(fx["en"])}</div>
<div style="font: 800 42px/1 'Barlow Condensed', sans-serif; color: #fff; background: {INK}; border-radius: 6px; padding: 3px 12px 2px; margin-top: 5px">{e(fx["price"])}</div>
</div>
{NOTE}'''
        + ''.join(sec(t) for t in ['DONER PLATTERS', 'SHAWARMA', 'HOT DOGS'])
        + f'''<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr); column-gap: 16px">
<div><div class="h"><b>SAUCE SELECTION</b><i>انتخاب سس</i></div>{sauces}</div>
<div><div class="h"><b>DRINKS</b><i>نوشیدنی‌ها</i></div>{drinks}</div>
</div>
{offer}'''
        + foot(f'''<div style="flex: 1; text-align: center">
<div style="font: 800 17px/1.1 'Barlow Condensed', sans-serif; color: {ORANGE}; letter-spacing: 1.5px">VISIT AJDAR ZAPATA</div>
<div style="font: 600 11.5px/1.35 Barlow, sans-serif; color: #fff">{ADDRESS}</div>
<div style="font: 800 21px/1.05 'Barlow Condensed', sans-serif; color: {ORANGE}">{PHONE}</div></div>''', FH2))

os.makedirs('menu/leaflet', exist_ok=True)
open('menu/leaflet/Main.dc.html', 'w').write(page('Ajdar Zapata Leaflet – front', front, float(os.environ.get('K1', '0.81')), FH1 + 6))
open('menu/leaflet/Back.dc.html', 'w').write(page('Ajdar Zapata Leaflet – back', back, float(os.environ.get('K2', '0.8')), FH2 + 6))
json.dump(ASSETS, open('menu/leaflet/assets.json', 'w'), indent=1)
print('wrote menu/leaflet/Main.dc.html, Back.dc.html')
