"""The double-sided A4 menu for sending out (Ryan, 26 Nov 2026), built from tools/make-menu.py.
Writes menu/a4/Main.dc.html (front) and menu/a4/Back.dc.html (back): the two artboards of Ryan's Claude Design
artifact "Ajdar Zapata A4 Menu" (https://claude.ai/artifact/Lip9yS3R3pBajm6cpGiJEK): publish them there. The PDF:
node tools/a4-pdf.cjs (or the artifact's Export > PDF). The logo is that artifact's upload (/_blob/...), also menu/a4/logo.png. K1/K2 scale the text so each
page is full (front 1.11, back 1.06 fit as of 26 Nov, after Mama's sheet; lower K1 if the front ever overflows).
The final PDF of 26 Nov is menu/Ajdar_Zapata_A4_Double_Sided.pdf.
    python3 tools/a4-menu.py
"""
import html, runpy, json
g = runpy.run_path('tools/make-menu.py')
PAGES, SAUCES, DRINKS = g['PAGES'], g['SAUCES'], g['DRINKS']
e = html.escape
secs = {}
for _, _, ss in PAGES:
    for t, fa, items in ss:
        if isinstance(items, list): secs[t] = (fa, items)
for x in secs['HOT DOGS'][1]:
    pass   # Ryan 26 Nov 2026
import re as _re
for t in secs:
    for x in secs[t][1]:
        for k in ('en','den'):
            x[k]=_re.sub(r'\bMeat\b','Lamb',_re.sub(r'\bmeat\b','lamb',x[k]))   # Ryan 26 Nov 2026: meat = lamb

LOGO = '/_blob/753d812f4c6a4a73e2c896594f40b699'
CSS = """body{margin:0}
.card{}
.h{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #F07C1A;padding-bottom:4px;margin:0 0 2px}
.h b{font:800 21px/1 'Barlow Condensed';color:#F07C1A;letter-spacing:1.5px}
.h i{font:700 16px/1 Vazirmatn;color:#F5A623;font-style:normal;direction:rtl}
.r{display:flex;gap:7px;border-bottom:1px solid #34302c;padding:4px 0 4px}
.n{flex:0 0 18px;height:18px;border-radius:3px;background:#F07C1A;color:#1a1310;font:800 11px/18px 'Barlow Condensed';text-align:center;margin-top:1px}
.b{flex:1;min-width:0}
.l1{display:flex;align-items:baseline;gap:8px}
.t{flex:1;min-width:0;font:700 14px/1.2 'Barlow Condensed';text-transform:uppercase;color:#fff}
.f{font:700 12px/1.2 Vazirmatn;color:#F5B02A;direction:rtl;white-space:nowrap}
.p{flex:0 0 auto;text-align:right;font:800 16px/1 'Barlow Condensed';color:#F07C1A;white-space:nowrap}
.c{white-space:nowrap;display:inline-block;font:500 7.5px/1 Barlow;letter-spacing:1px;color:#F5C04A;border:1px solid #F5C04A;border-radius:9px;padding:1px 5px;margin-left:5px;vertical-align:2px}
.d{font:400 9.5px/1.3 Barlow;color:#d0c9bf;margin-top:2px}
.dfa{font:400 9.5px/1.5 Vazirmatn;color:#e2b86a;direction:rtl;text-align:right;margin-top:1px}
.s{display:flex;justify-content:space-between;align-items:baseline;gap:6px;border-bottom:1px solid #34302c;padding:4px 0}
.s span{font:600 13.5px 'Barlow Condensed';color:#fff;text-transform:uppercase}
.s em{font:500 12px Vazirmatn;color:#F5B02A;font-style:normal;direction:rtl}
.s strong{font:800 14px 'Barlow Condensed';color:#F07C1A}
.dn{display:inline-block;width:20px;color:#F07C1A;font-weight:800}
.pg{}"""

def row(x):
    badge = f'<span class="c">{e(x["badge"])}</span>' if x['badge'] else ''
    pr = e(x['price']).replace(' · ', '<br>')
    d = f'<div class="d">{e(x["den"])}</div>' if x['den'] else ''
    dfa = f'<div class="dfa">{e(x["dfa"])}</div>' if x['dfa'] else ''
    return (f'<div class="r"><span class="n">{x["n"]}</span><div class="b"><div class="l1"><span class="t">{e(x["en"])}{badge}</span>'
            f'<span class="f">{e(x["fa"])}</span><span class="p">{pr}</span></div>{d}{dfa}</div></div>')

def sec(t):
    fa, items = secs[t]
    return f'<div class="card"><div class="h"><b>{e(t)}</b><i>{e(fa)}</i></div>' + ''.join(row(x) for x in items) + '</div>'

def cols(L, R):
    c = lambda ts: '<div style="display: flex; flex-direction: column; gap: 14px">' + ''.join(sec(t) for t in ts) + '</div>'
    return f'<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 26px; align-items: start">{c(L)}{c(R)}</div>'

BAR = '<div style="position: absolute; left: 0; right: 0; {pos}: 0; height: 8px; background: #F07C1A"></div>'
import os, re as _re2
def scss(k):
    return _re2.sub(r'(\d+(?:\.\d+)?)px', lambda m: f'{float(m.group(1))*k:.2f}px' if float(m.group(1))>2 else m.group(0), CSS)
def page(title, inner, k=1.0):
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
<div style="width: 794px; height: 1123px; box-sizing: border-box; background: #121110; position: relative; overflow: hidden; padding: 24px 36px 22px; display: flex; flex-direction: column; color: #fff" class="pg">
{BAR.format(pos="top")}
{BAR.format(pos="bottom")}
{inner}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":794,"height":1123}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''

front = (f'<div style="display: flex; justify-content: center; margin-bottom: 8px"><img src="{LOGO}" alt="Ajdar Zapata Sandwich" style="width: 170px; height: 83px; object-fit: contain"></div>'
         + cols(['STARTERS & SIDES', 'SANDWICHES'], ['BURGERS', 'DONER BAGUETTES'])
         + '<div style="margin-top: auto; padding-top: 8px; display: flex; justify-content: space-between; font: 600 12px Barlow, sans-serif; color: #a39d95"><span>Continued overleaf →</span><span style="font-family: Vazirmatn, sans-serif; direction: rtl">ادامه در پشت صفحه</span></div>')

sauces = ''.join(f'<div class="s"><span>{e(a)}</span><em>{e(b)}</em></div>' for a, b in SAUCES)
drinks = ''.join(f'<div class="s"><span><b class="dn">{n}</b>{e(a)} <em>{e(b)}</em></span><strong>{p}</strong></div>' for n, a, b, p in DRINKS)
back = (f'<div style="display: flex; justify-content: center; margin-bottom: 8px"><img src="{LOGO}" alt="Ajdar Zapata Sandwich" style="width: 170px; height: 83px; object-fit: contain"></div>'
        + cols(['DONER PLATTERS', 'SHAWARMA'], ['HOT DOGS'])
        + f'''<div style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 26px; margin-top: auto; padding-top: 10px">
<div class="card"><div class="h"><b>SAUCE SELECTION</b><i>انتخاب سس</i></div>
<div>{sauces}</div></div>
<div class="card"><div class="h"><b>DRINKS</b><i>نوشیدنی‌ها</i></div>
<div>{drinks}</div></div>
</div>
<div style="margin-top: 10px; border: 2px solid #F07C1A; border-radius: 8px; padding: 7px 12px; text-align: center; font: 800 19px/1.2 'Barlow Condensed', sans-serif; color: #F07C1A; letter-spacing: 0.5px">864 High Road, London N12 9RH · Tel 020 8259 4026 · ajdarzapata.co.uk</div>
<div style="margin-top: 10px; border: 1.5px solid #5a524a; border-radius: 8px; padding: 9px 12px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 22px; color: #e4ddd3; font: 400 10.5px/1.4 Barlow, sans-serif">
<p style="margin: 0; font-size: 12px; line-height: 1.45"><b style="color: #F5A623; font-size: 14px">FOOD ALLERGY OR INTOLERANCE?</b><br>If you have a food allergy, intolerance, or coeliac disease – please speak to the staff about the ingredients in your food and drink before you order. Thank you.</p>
<p style="margin: 0; font-family: Vazirmatn, sans-serif; direction: rtl; font-size: 11.5px; line-height: 1.7"><b style="color: #F5A623; font-size: 13px">حساسیت یا عدم تحمل غذایی؟</b><br>اگر حساسیت یا عدم تحمل غذایی یا بیماری سلیاک دارید، لطفاً پیش از سفارش دربارهٔ مواد غذا و نوشیدنی با کارکنان ما صحبت کنید. سپاسگزاریم.</p>
</div>''')

P = 'menu/a4/'
open(P + 'Main.dc.html', 'w').write(page('Ajdar Zapata Menu – front', front, float(os.environ.get('K1','1.11'))))
open(P + 'Back.dc.html', 'w').write(page('Ajdar Zapata Menu – back', back, float(os.environ.get('K2','1.06'))))
# self-check: every item, description and price from the repo list appears
allx = [x for t in secs for x in secs[t][1]]
txt = open(P + 'Main.dc.html').read() + open(P + 'Back.dc.html').read()
miss = [x['n'] for x in allx if not all(e(v).split(' · ')[0] in txt for v in (x['en'], x['fa'], x['den'], x['dfa'], x['price']) if v)]
print('items', len(allx), 'missing', miss, 'drinks', len(DRINKS), 'sauces', len(SAUCES))
