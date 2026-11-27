"""The chef's sheet for the kitchen (Ryan, 27 Nov 2026: "a chef's menu version ... with the numbers as shown on the menu
board ... very plain white background ... A3, just one sheet to be put on the back of the fridge ... only Persian with
the numbers, the name, the ingredients ... black on white"; "make sure it is the exact same ... all synced ... not making
up anything").
Built from tools/make-menu.py, like everything else: the board's numbers, the Persian names and the Persian ingredients
word for word, sizes where the list has them (Fries: M / L), the sauces and the drinks. No prices, no English, no
pictures: a kitchen build sheet on white, to print and laminate; three colours (below), heavy type.
Writes menu/chef/Main.dc.html, the artboard of Ryan's Claude Design artifact "Ajdar Zapata Chef Sheet"
(https://claude.ai/artifact/Q4nFQ1S6tyxzziRunRyB3a; its index is menu/chef/canvas.json); the PDF:
node tools/a4-pdf.cjs chef -> menu/Ajdar_Zapata_Chef_Sheet_A3.pdf. A3 landscape, 4 columns right to left in number order; K scales the type so the sheet is full (0.98 on 27 Nov:
ingredients 13 pt, names 17 pt, for reading at 1-2 m).
    python3 tools/chef-sheet.py
"""
import datetime, html, os, re, runpy

g = runpy.run_path('tools/make-menu.py')
PAGES, SAUCES, DRINKS = g['PAGES'], g['SAUCES'], g['DRINKS']
e = html.escape
secs = [(t, fa, items) for _, _, ss in PAGES for t, fa, items in ss if isinstance(items, list)]
W, H = 1587, 1123          # A3 landscape at 96 px to the inch (420 x 297 mm)
COLS = int(os.environ.get("COLS", "4"))
FA_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
MONTHS = ['ژانویه', 'فوریه', 'مارس', 'آوریل', 'مه', 'ژوئن', 'ژوئیه', 'اوت', 'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر']
today = datetime.date.today()
DATE = f'{today.day} {MONTHS[today.month - 1]} {today.year}'.translate(FA_DIGITS)

# Three colours so the kitchen tells things apart at a glance (Ryan, 27 Nov 2026 17:00: "add colours ... around 3 colours
# so they can differentiate things easier", "font make thick"): red = numbers and sections, black = the item's name,
# blue = what goes in it. All on white, all heavy. Contrast on white: red 6.5:1, blue 8.7:1.
RED, BLUE, INK = '#B91C1C', '#1E3A8A', '#000'
CSS = """body{margin:0}
.cols{column-count:%d;column-gap:28px;column-rule:2px solid #000;direction:rtl}
.sec{}
h2{margin:0 0 4px;padding:3px 12px 4px;border-radius:6px;background:""" + RED + """;font:900 26px/1.2 Vazirmatn;color:#fff;break-after:avoid}
.sec+.sec{margin-top:12px}
.r{display:flex;gap:10px;align-items:flex-start;padding:5px 0 6px;border-bottom:1.5px solid #8a8a8a;break-inside:avoid}
.n{flex:0 0 40px;height:36px;border-radius:5px;background:""" + RED + """;color:#fff;font:900 25px/36px 'Barlow Condensed';text-align:center;direction:ltr}
.b{flex:1;min-width:0}
.l1{display:flex;align-items:baseline;gap:10px}
.t{font:900 23px/1.25 Vazirmatn;color:""" + INK + """}
.sz{font:900 19px/1 'Barlow Condensed';color:""" + RED + """;border:2.5px solid """ + RED + """;border-radius:4px;padding:2px 7px 1px;direction:ltr;white-space:nowrap}
.d{font:700 18px/1.45 Vazirmatn;color:""" + BLUE + """;margin-top:1px}
.ss{display:grid;grid-template-columns:1fr 1fr;column-gap:16px}
.s{font:900 19px/1.3 Vazirmatn;color:""" + INK + """;padding:6px 0;border-bottom:1.5px solid #8a8a8a}
.dk{display:grid;grid-template-columns:1fr 1fr;column-gap:16px}
.dk .r{padding:5px 0 6px}
.pg{}"""


def scss(k):
    return re.sub(r'(\d+(?:\.\d+)?)px', lambda m: f'{float(m.group(1)) * k:.2f}px' if float(m.group(1)) > 2 else m.group(0), CSS % COLS)


def sizes(price):
    """Sizes as the list gives them in the price ("M £2.99 · L £4.99" -> M / L); none for one size."""
    parts = [p.split()[0] for p in price.split(' · ') if len(p.split()) == 2]
    return ' / '.join(parts) if len(parts) > 1 else ''


def row(n, name, size='', desc=''):
    sz = f'<span class="sz">{e(size)}</span>' if size else ''
    d = f'<div class="d">{e(desc)}</div>' if desc else ''
    return f'<div class="r"><span class="n">{n}</span><div class="b"><div class="l1"><span class="t">{e(name)}</span>{sz}</div>{d}</div></div>'


body = ''.join(f'<div class="sec"><h2>{e(fa)}</h2>' + ''.join(row(x['n'], x['fa'], sizes(x['price']), x['dfa']) for x in items) + '</div>'
               for t, fa, items in secs)
body += ('<div class="sec"><h2>انتخاب سس</h2><div class="ss">' + ''.join(f'<div class="s">{e(fa)}</div>' for _, fa in SAUCES) + '</div></div>'
         '<div class="sec"><h2>نوشیدنی‌ها</h2><div class="dk">' + ''.join(row(n, fa) for n, _, fa, _ in DRINKS) + '</div></div>')


def page(k):
    return f'''<!doctype html>
<html lang="fa">
<head>
<meta charset="utf-8">
<title>Ajdar Zapata – chef sheet A3</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@800;900&amp;family=Vazirmatn:wght@700;800;900&amp;display=swap" rel="stylesheet">
<style>
{scss(k)}
</style>
</helmet>
<div style="width: {W}px; height: {H}px; box-sizing: border-box; background: #fff; position: relative; overflow: hidden; padding: 24px 32px 20px; display: flex; flex-direction: column; color: #000" class="pg">
<div style="display: flex; justify-content: space-between; align-items: baseline; direction: rtl; border-bottom: 5px solid {RED}; padding-bottom: 6px; margin-bottom: 10px">
<span style="font: 900 {34 * k:.1f}px/1.1 Vazirmatn, sans-serif; color: #000">اژدر زاپاتا · منوی آشپزخانه</span>
<span style="font: 800 {18 * k:.1f}px/1.1 Vazirmatn, sans-serif; color: #000">به‌روز: {DATE}</span>
</div>
<div class="cols">{body}</div>
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


os.makedirs('menu/chef', exist_ok=True)
open('menu/chef/Main.dc.html', 'w').write(page(float(os.environ.get("K", "0.98"))))
print('wrote menu/chef/Main.dc.html')
