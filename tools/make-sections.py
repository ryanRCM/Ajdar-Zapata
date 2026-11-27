"""The TV menu panels (site/monitor-N/sec-*.png) and both layout.css files, drawn from the same list as the printed
menu (tools/make-menu.py), in the look of the old lifted boards but sharp at 2x. Replaces the lifting in
tools/build-walls.py (the boards PDF can't be renumbered); the logo files it made are kept as they are.
    python3 tools/make-sections.py && node tools/sections.cjs && python3 tools/make-sections.py layout
The two halves the shop TVs show, still (24 Nov 2026: "the menu in two parts, one on each monitor, always fixed";
27 Nov 2026: one menu across both, sauces and drinks small in a side column, see HALVES):
site/monitor-1/halves.css, also written by `layout`, or on its own with: python3 tools/make-sections.py halves
"""
import html, json, runpy, sys, pathlib
D = runpy.run_path('tools/make-menu.py')
PAGES, SAUCES, DRINKS = D['PAGES'], D['SAUCES'], D['DRINKS']
e = html.escape
PALETTE = {1: {'heading': (120, 10, 0), 'price': (222, 22, 10), 'persian': (168, 58, 0), 'name': (14, 10, 8), 'desc': (72, 52, 36)},
           2: {'heading': (110, 6, 0), 'price': (206, 14, 30), 'persian': (150, 46, 0), 'name': (14, 10, 8), 'desc': (70, 46, 34)}}
KEY = {'STARTERS & SIDES': 'starters', 'SAUCE SELECTION': 'sauces', 'SANDWICHES': 'sandwiches', 'BURGERS': 'burgers', 'DONER BAGUETTES': 'doner',
       'DONER PLATTERS': 'platters', 'SHAWARMA': 'shawarma', 'HOT DOGS': 'hotdogs', 'DRINKS': 'drinks'}
WIDTH = {'starters': 1200, 'sauces': 600, 'drinks': 600, 'sandwiches': 1200, 'burgers': 1200, 'doner': 1200, 'platters': 1800, 'shawarma': 1800, 'hotdogs': 1800}   # TV1 columns 1200, TV2's food column 1800 (fills it), the side column (sauces, drinks) 600 (Ryan, 27 Nov 2026)
DESC = {'starters', 'sandwiches', 'burgers', 'doner', 'platters', 'shawarma', 'hotdogs'}   # ingredients on every item that has them (Ryan, 26 Nov 2026: "everything ... ingredients")
DESC_FA = False   # Persian ingredients too would halve the size of the whole board (26 Nov 2026: scale 0.50 vs 0.71); they are on the A4. True to show them
STATIC = [['starters', 'sandwiches', 'burgers'], ['drinks', 'sauces'], ['doner', 'platters', 'shawarma', 'hotdogs']]
# The halves: ONE menu split across the two TVs, read left to right (Ryan, 27 Nov 2026: "it's always going to be one
# menu split across the two monitors"; "sauces and drinks smaller, to the side"): left TV Starters, Sandwiches |
# Burgers, Doner; right TV Platters, Shawarma, Hot Dogs | a narrow side column of Sauces, Drinks and the allergy notice.
# Both TVs use the same text size (the smaller of the two that fit), so the pair reads as one board.
HALVES = {1: [['starters', 'sandwiches'], ['burgers', 'doner']], 2: [['platters', 'shawarma', 'hotdogs'], ['sauces', 'drinks']]}
SIDE = {2: 1}   # the narrow side column: drawn small (600 wide, smaller type) and given no extra width
# The food allergy notice at the end of the menu: half 2, under the side column, at least NOTE_MIN px tall at 1080
# (the menu is sized to leave that room; that column's panels don't stretch, the notice takes what is left).
NOTE = {2: 1}; NOTE_MIN = 300.0
SIZES = pathlib.Path('tools/.sections.json')

def row(x, key):
    name = x['en'].upper(); tag = ''
    if ' · ' in name: name, t = name.split(' · '); tag = f'<span class="pill">{e(t)}</span>'
    if x['badge']: tag += f'<span class="pill">{e(x["badge"])}</span>'
    desc = f'<div class="d">{e(x["den"])}</div>' if key in DESC and x['den'] else ''
    if desc and DESC_FA and x['dfa']: desc += f'<div class="dfa" dir="rtl">{e(x["dfa"])}</div>'
    pr = x['price']
    if pr.startswith('M '):
        m, l = [v.split(' ')[1] for v in pr.split(' · ')]
        price = f'<span class="ml"><i>M</i>{e(m)}</span><span class="ml"><i>L</i>{e(l)}</span>'
    else: price = f'<span class="p">{e(pr)}</span>'
    return f'<div class="r"><span class="n">{x["n"]}</span><div class="b"><div class="t">{e(name)}{tag}</div>{desc}</div><span class="f" dir="rtl">{e(x["fa"])}</span>{price}</div>'

def sec(title, fa, items):
    key = KEY[title]
    h = f'<div class="sec" id="{key}" style="width:{WIDTH[key]}px"><div class="h"><span>{e(title)}</span><span class="hf" dir="rtl">{e(fa)}</span></div>'
    if items == 'SAUCES':
        h += ''.join(f'<div class="s"><span class="t">{e(a.upper())}</span><span class="f" dir="rtl">{e(b)}</span></div>' for a, b in SAUCES)
    elif items == 'DRINKS':   # every drink on its own row with its own number and price (Mama, 24 Nov 2026), 37-43 as printed
        def dname(a):
            a = a.upper()
            return e(a.split(' · ')[0]) + (f'<span class="pill">{e(a.split(" · ")[1])}</span>' if ' · ' in a else '')
        h += ''.join(f'<div class="r"><span class="n">{n}</span><div class="b"><div class="t">{dname(a)}</div></div><span class="f" dir="rtl">{e(b)}</span><span class="p">{p}</span></div>' for n, a, b, p in DRINKS)
    else:
        h += ''.join(row(x, key) for x in items)
    return h + '</div>'

def page(mon):
    c = {k: 'rgb(%d,%d,%d)' % v for k, v in PALETTE[mon].items()}
    css = f'''
*{{box-sizing:border-box;margin:0;padding:0}} html,body{{background:transparent}}
body{{font-family:'Barlow Semi Condensed',sans-serif;color:{c['name']};padding:40px;display:flex;flex-direction:column;gap:60px;align-items:flex-start;-webkit-font-smoothing:antialiased}}
.sec{{padding:2px 4px 6px}}
.h{{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:4px solid {c['heading']};padding-bottom:12px;margin-bottom:2px;color:{c['heading']};font:400 52px/1 'Bebas Neue',sans-serif;letter-spacing:3px;-webkit-text-stroke:1.2px {c['heading']}}}
.hf{{font:800 38px/1.2 'Vazirmatn',sans-serif;letter-spacing:0;color:{c['persian']};-webkit-text-stroke:0}}
.r{{display:flex;align-items:center;gap:18px;padding:9px 0 10px;border-bottom:2px solid rgba(90,30,0,.14)}} .r:last-child,.s:last-child{{border-bottom:0}}
.n{{flex:0 0 50px;height:50px;border-radius:11px;background:{c['price']};color:#fff;font:400 30px/50px 'Bebas Neue',sans-serif;text-align:center;letter-spacing:.5px;box-shadow:0 2px 0 rgba(0,0,0,.18)}}
.b{{flex:1;min-width:0}}
.t{{font:400 38px/1 'Bebas Neue',sans-serif;letter-spacing:.6px;-webkit-text-stroke:.7px {c['name']};white-space:nowrap}} .t.sm{{font-size:31px}}
.pill{{display:inline-block;vertical-align:middle;margin:-6px 0 0 14px;border:2.5px solid {c['price']};color:{c['price']};border-radius:99px;font:700 16px/1 'Barlow Semi Condensed',sans-serif;letter-spacing:2px;padding:4px 12px 5px;-webkit-text-stroke:0}}
.d{{font:500 20px/1.25 'Barlow Semi Condensed',sans-serif;color:{c['desc']};margin-top:5px;letter-spacing:.2px}}
.dfa{{font:600 19px/1.5 'Vazirmatn',sans-serif;color:{c['desc']};margin-top:2px;text-align:right}}
.f{{font:800 28px/1.3 'Vazirmatn',sans-serif;color:{c['persian']};white-space:nowrap}}
.p,.ml{{font:400 48px/1 'Bebas Neue',sans-serif;color:{c['price']};letter-spacing:1px;-webkit-text-stroke:1px {c['price']};min-width:132px;text-align:right;white-space:nowrap}}
.ml{{min-width:150px;font-size:44px}} .ml i{{font:800 19px/1 'Barlow Semi Condensed',sans-serif;font-style:normal;-webkit-text-stroke:0;background:{c['price']};color:#fff;border-radius:6px;padding:3px 7px 4px;margin-right:7px;vertical-align:9px;letter-spacing:0}}
.soft .b .f{{margin-top:6px;font-size:25px}} .soft{{padding-left:68px}}
.s{{display:flex;align-items:center;gap:26px;padding:8px 0 9px;border-bottom:2px solid rgba(90,30,0,.14)}} .s .t{{flex:0 0 52%;text-align:right;font-size:40px}} .s .f{{font-size:31px}}
#sauces .h,#drinks .h{{font-size:42px;padding-bottom:9px}} #sauces .hf,#drinks .hf{{font-size:30px}}
#sauces .s{{gap:16px;padding:5px 0 6px}} #sauces .s .t{{font-size:30px;flex:0 0 50%}} #sauces .s .f{{font-size:24px}}
#drinks .r{{gap:12px;padding:5px 0 6px}} #drinks .n{{flex:0 0 38px;height:38px;border-radius:9px;font-size:23px;line-height:38px}} #drinks .t{{font-size:29px}} #drinks .f{{font-size:21px}} #drinks .p{{font-size:36px;min-width:96px}}
#starters .r{{padding:6px 0 7px}} #doner .r,#platters .r,#shawarma .r,#hotdogs .r{{padding:8px 0 9px}}
'''
    secs = ''.join(sec(*s) for _, _, ss in PAGES for s in ss)
    return ('<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Semi+Condensed:wght@500;700;800&family=Vazirmatn:wght@700;800&display=swap" rel="stylesheet">'
            f'<style>{css}</style></head><body>{secs}</body></html>')

def sizes():
    # the panels' sizes, from tools/sections.cjs; without that file, from the panel pictures (drawn at 2x)
    if SIZES.exists(): return {k: tuple(v) for k, v in json.loads(SIZES.read_text()).items()}
    from PIL import Image
    return {k: tuple(round(v / 2) for v in Image.open(f'site/monitor-1/sec-{k}.png').size) for k in WIDTH}

def halves():
    """site/monitor-1/halves.css: /monitor-1/?half=1 and ?half=2, the two halves of one menu, one per shop TV, both at the
    same text scale. Both halves in the same yellow, so the two TVs read as one board (Ryan, 24 Nov 2026: "one big one")."""
    size = sizes()
    W, H, M, GAP, PAD, TOP = 1920.0, 1080.0, 14.0, 12.0, 10.0, 12.0
    BOT = H - 12.0
    pct = lambda v, ref: f'{v / ref * 100:.3f}%'
    css = ['/* Made by tools/make-sections.py: do not edit by hand. The two halves of the menu, one per shop TV, still. */',
]
    fits = {}
    for half, cols in HALVES.items():
        fixed_w = 2 * M + GAP * (len(cols) - 1) + 2 * PAD * len(cols)
        s = (W - fixed_w) / sum(max(size[n][0] for n in c) for c in cols)
        for k, c in enumerate(cols):
            room = (NOTE_MIN + GAP) if NOTE.get(half) == k else 0
            s = min(s, (BOT - TOP - room - GAP * (len(c) - 1) - 2 * PAD * len(c)) / sum(size[n][1] for n in c))
        fits[half] = s
    s = min(fits.values())   # one menu: the same text size on both TVs
    out = []
    for half, cols in HALVES.items():
        fixed_w = 2 * M + GAP * (len(cols) - 1) + 2 * PAD * len(cols)
        side = SIDE.get(half)
        food = [k for k in range(len(cols)) if k != side]
        extra = (W - fixed_w - s * sum(max(size[n][0] for n in c) for c in cols)) / len(food)
        css.append(f'/* half {half}: text scale {s:.3f} (this half alone would fit {fits[half]:.3f}) */')
        css += [f'html.half-{half} .sec-{n} {{ display: none; }}' for n in WIDTH if n not in [n for c in cols for n in c]]
        x = M
        for k, c in enumerate(cols):
            cw = max(size[n][0] for n in c) * s + 2 * PAD + (0 if k == side else extra)
            used = sum(size[n][1] * s + 2 * PAD for n in c) + GAP * (len(c) - 1)
            note = NOTE.get(half) == k
            grow = 0 if note else (BOT - TOP - used) / len(c); y = TOP
            for n in c:
                h = size[n][1] * s + 2 * PAD + grow
                css.append(f'html.half-{half} .sec-{n} {{ left: {pct(x, W)}; top: {pct(y, H)}; width: {pct(cw, W)}; height: {pct(h, H)}; }}')
                y += h + GAP
            if note:   # the allergy notice in what is left at the bottom of this column
                css.append(f'html.half-{half} .note {{ display: flex; left: {pct(x, W)}; top: {pct(y, H)}; width: {pct(cw, W)}; height: {pct(BOT - y, H)}; }}')
            x += cw + GAP
        out.append(f'half {half} text scale {s:.3f}')
    open('site/monitor-1/halves.css', 'w').write('\n'.join(css) + '\n')
    print('halves written; ' + ', '.join(out))

def layout():
    size = sizes()
    W, H, M, GAP, PAD, TOP = 1920.0, 1080.0, 14.0, 12.0, 10.0, 12.0
    BOT = H - 12.0
    pct = lambda v, ref: f'{v / ref * 100:.3f}%'
    cw_b = lambda names: max(size[n][0] for n in names)
    fixed_w = 2 * M + GAP * (len(STATIC) - 1) + 2 * PAD * len(STATIC)
    s1 = (W - fixed_w) / sum(cw_b(c) for c in STATIC)
    for names in STATIC:
        s1 = min(s1, (BOT - TOP - GAP * (len(names) - 1) - 2 * PAD * len(names)) / sum(size[n][1] for n in names))
    css = [f'/* Made by tools/make-sections.py: do not edit by hand. Full-menu TV, everything at once, text scale {s1:.3f}. */']
    extra_w = (W - fixed_w - s1 * sum(cw_b(c) for c in STATIC)) / len(STATIC)
    x = M
    for names in STATIC:
        cw = cw_b(names) * s1 + 2 * PAD + extra_w
        used = sum(size[n][1] * s1 + 2 * PAD for n in names) + GAP * (len(names) - 1)
        grow = (BOT - TOP - used) / len(names); y = TOP
        for n in names:
            h = size[n][1] * s1 + 2 * PAD + grow
            css.append(f'.sec-{n} {{ left: {pct(x, W)}; top: {pct(y, H)}; width: {pct(cw, W)}; height: {pct(h, H)}; }}')
            y += h + GAP
        x += cw + GAP
    open('site/monitor-1/layout.css', 'w').write('\n'.join(css) + '\n')
    SIDE_W = 520.0; area_w = W - 2 * M - SIDE_W - GAP
    css = ['/* Made by tools/make-sections.py: do not edit by hand. Cycling TV, one section at a time, each as big as fits. */']
    for n, (w0, h0) in size.items():
        s2 = min((area_w - 2 * PAD) / w0, (BOT - TOP - 2 * PAD) / h0)
        w, h = w0 * s2 + 2 * PAD, h0 * s2 + 2 * PAD
        css.append(f'.tvslide.sec-{n} {{ left: {pct(M + (area_w - w) / 2, W)}; top: {pct(TOP + (BOT - TOP - h) / 2, H)}; width: {pct(w, W)}; height: {pct(h, H)}; }}')
    css.append(f'.side {{ left: {pct(W - M - SIDE_W, W)}; top: {pct(TOP, H)}; width: {pct(SIDE_W, W)}; height: {pct(BOT - TOP, H)}; }}')
    open('site/monitor-2/layout.css', 'w').write('\n'.join(css) + '\n')
    print(f'layout written; full-menu TV text scale {s1:.3f}')
    halves()

if sys.argv[1:] == ['layout']: layout()
elif sys.argv[1:] == ['halves']: halves()
else:
    for mon in (1, 2): pathlib.Path(f'tools/.sections-{mon}.html').write_text(page(mon))
    print('wrote tools/.sections-1.html, -2.html')
