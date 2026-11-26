"""The takeaway leaflet (Ryan, 26 Nov 2026: "a leaflet with the menu in it, no ingredients, with the address and phone,
no food allergy; at the bottom the offer stand"), built from tools/make-menu.py so it can never drift from the TVs and
the A4. Double-sided A5 (148 x 210 mm), black with orange like the A4: front = logo, Starters, Sandwiches, Burgers,
Doner Baguettes; back = Platters, Shawarma, Hot Dogs, Sauces and Drinks, the address and phone, then the offer.
Writes menu/leaflet/Main.dc.html (front) and Back.dc.html (back), the two artboards of Ryan's Claude Design artifact
"Ajdar Zapata Leaflet" (https://claude.ai/artifact/89Tw2CpFz5xUPwB4HESdyz); the PDF: node tools/a4-pdf.cjs leaflet -> menu/Ajdar_Zapata_Leaflet_A5.pdf.
OFFER below is the offer box at the bottom of the back: Ryan's words from the shop's offer stand, nothing invented.
K1/K2 scale the text so each side is full.
    python3 tools/leaflet.py
"""
import html, os, re, runpy

g = runpy.run_path('tools/make-menu.py')
PAGES, SAUCES, DRINKS = g['PAGES'], g['SAUCES'], g['DRINKS']
e = html.escape
secs = {t: (fa, items) for _, _, ss in PAGES for t, fa, items in ss if isinstance(items, list)}
W, H = 559, 794   # A5 at 96 px to the inch
LOGO = '/_blob/cf0e3e5a629b743fcaa2dba8defe4817'   # the leaflet artifact's upload of menu/a4/logo.png
PHONE = '020 8259 4026'
# the offer: the shop's loyalty card, word for word (Ryan's photo, 26 Nov 2026 16:05: "offer is here")
OFFER = {'title': 'LOYALTY CARD · DAILY REWARDS', 'lines': ['£10 = 1 STAMP · £20+ = 2 STAMPS · ONE ORDER PER DAY'], 'big': '5 STAMPS · 1 FREE SHAWARMA'}

CSS = """body{margin:0}
.h{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #F07C1A;padding-bottom:3px;margin:0 0 1px}
.h b{font:800 19px/1 'Barlow Condensed';color:#F07C1A;letter-spacing:1.3px}
.h i{font:700 15px/1 Vazirmatn;color:#F5A623;font-style:normal;direction:rtl}
.r{display:flex;align-items:center;gap:8px;border-bottom:1px solid #34302c;padding:3px 0}
.n{flex:0 0 18px;height:18px;border-radius:3px;background:#F07C1A;color:#1a1310;font:800 11px/18px 'Barlow Condensed';text-align:center}
.t{flex:1;min-width:0;font:700 14.5px/1.15 'Barlow Condensed';text-transform:uppercase;color:#fff}
.f{font:700 12.5px/1.2 Vazirmatn;color:#F5B02A;direction:rtl;white-space:nowrap}
.p{flex:0 0 auto;min-width:46px;text-align:right;font:800 16px/1.05 'Barlow Condensed';color:#F07C1A;white-space:nowrap}
.s{display:flex;justify-content:space-between;align-items:baseline;gap:6px;border-bottom:1px solid #34302c;padding:3px 0}
.s span{font:600 13px 'Barlow Condensed';color:#fff;text-transform:uppercase}
.s em{font:500 11.5px Vazirmatn;color:#F5B02A;font-style:normal;direction:rtl}
.s strong{font:800 14px 'Barlow Condensed';color:#F07C1A}
.dn{display:inline-block;width:19px;color:#F07C1A;font-weight:800}
.sec{margin-bottom:10px}
.pg{}"""


def scss(k):
    return re.sub(r'(\d+(?:\.\d+)?)px', lambda m: f'{float(m.group(1)) * k:.2f}px' if float(m.group(1)) > 2 else m.group(0), CSS)


def row(x):
    pr = e(x['price']).replace(' · ', '<br>')
    return (f'<div class="r"><span class="n">{x["n"]}</span><span class="t">{e(x["en"])}</span>'
            f'<span class="f">{e(x["fa"])}</span><span class="p">{pr}</span></div>')


def sec(t):
    fa, items = secs[t]
    return f'<div class="sec"><div class="h"><b>{e(t)}</b><i>{e(fa)}</i></div>' + ''.join(row(x) for x in items) + '</div>'


BAR = '<div style="position: absolute; left: 0; right: 0; {pos}: 0; height: 7px; background: #F07C1A"></div>'


def page(title, inner, k):
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
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&amp;family=Barlow:wght@400;500&amp;family=Vazirmatn:wght@400;500;700&amp;display=swap" rel="stylesheet">
<style>
{scss(k)}
</style>
</helmet>
<div style="width: {W}px; height: {H}px; box-sizing: border-box; background: #121110; position: relative; overflow: hidden; padding: 18px 26px 18px; display: flex; flex-direction: column; color: #fff" class="pg">
{BAR.format(pos="top")}
{BAR.format(pos="bottom")}
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


logo = f'<div style="display: flex; justify-content: center; margin: 4px 0 8px"><img src="{LOGO}" alt="Ajdar Zapata Sandwich" style="width: 140px; height: 68px; object-fit: contain"></div>'
front = logo + ''.join(sec(t) for t in ['STARTERS & SIDES', 'SANDWICHES', 'BURGERS', 'DONER BAGUETTES'])

sauces = ''.join(f'<div class="s"><span>{e(a)}</span><em>{e(b)}</em></div>' for a, b in SAUCES)
drinks = ''.join(f'<div class="s"><span><b class="dn">{n}</b>{e(a)} <em>{e(b)}</em></span><strong>{p}</strong></div>' for n, a, b, p in DRINKS)
if OFFER:
    offer = ('<div style="margin-top: 10px; background: #F07C1A; color: #121110; border-radius: 8px; padding: 8px 12px 9px; text-align: center">'
             f'<div style="font: 800 20px/1.1 \'Barlow Condensed\', sans-serif; letter-spacing: 1px">{e(OFFER["title"])}</div>'
             + ''.join(f'<div style="font: 700 15px/1.25 \'Barlow Condensed\', sans-serif; margin-top: 3px">{e(l)}</div>' for l in OFFER['lines'])
             + f'<div style="font: 800 22px/1.1 \'Barlow Condensed\', sans-serif; margin-top: 4px; color: #fff; background: #121110; border-radius: 6px; padding: 4px 8px; display: inline-block">{e(OFFER["big"])}</div></div>')
else:
    offer = ('<div style="margin-top: 10px; border: 2px dashed #F07C1A; border-radius: 8px; padding: 12px; text-align: center; '
             'font: 700 15px/1.3 \'Barlow Condensed\', sans-serif; color: #F07C1A">OFFER GOES HERE: send Claude the offer stand</div>')
back = (''.join(sec(t) for t in ['DONER PLATTERS', 'SHAWARMA', 'HOT DOGS'])
        + f'''<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr); column-gap: 18px">
<div><div class="h"><b>SAUCE SELECTION</b><i>انتخاب سس</i></div>{sauces}</div>
<div><div class="h"><b>DRINKS</b><i>نوشیدنی‌ها</i></div>{drinks}</div>
</div>
<div style="margin-top: auto; padding-top: 10px; text-align: center; font: 800 17px/1.25 'Barlow Condensed', sans-serif; color: #F07C1A; letter-spacing: .4px">864 High Road, London N12 9RH<br><span style="font-size: 26px; color: #fff">{PHONE}</span></div>
{offer}''')

os.makedirs('menu/leaflet', exist_ok=True)
open('menu/leaflet/Main.dc.html', 'w').write(page('Ajdar Zapata Leaflet – front', front, float(os.environ.get('K1', '0.9'))))
open('menu/leaflet/Back.dc.html', 'w').write(page('Ajdar Zapata Leaflet – back', back, float(os.environ.get('K2', '0.92'))))
print('wrote menu/leaflet/Main.dc.html, Back.dc.html')
