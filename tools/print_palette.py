"""One colour palette for everything printed: the A4 menu (tools/a4-menu.py) and the A5 leaflet (tools/leaflet.py).
Ryan, 27 Nov 2026: the leaflet "background to be orange", and "the actual menu give it same colour palette, lock in
everything". Orange page, black ink; black bars and boxes carry orange and white.
"""
ORANGE = '#F07C1A'      # the page (the logo's and the TVs' orange)
INK = '#121110'         # names, prices, rules, bars, number tags
BROWN = '#3b1200'       # Persian and ingredients (dark brown on orange reads well)
SOFT = '#F9B46B'        # Persian on the black bars
RULE = 'rgba(18,17,16,.24)'

# section heading: a black bar with orange English and soft-orange Persian; number tags black with orange figures
BAR_CSS = f""".h{{display:flex;justify-content:space-between;align-items:center;background:{INK};border-radius:5px;padding:5px 9px 4px;margin:0 0 3px}}
.h b{{font:800 19px/1 'Barlow Condensed';color:{ORANGE};letter-spacing:1.3px}}
.h i{{font:700 15px/1 Vazirmatn;color:{SOFT};font-style:normal;direction:rtl}}
.n{{flex:0 0 18px;height:18px;border-radius:3px;background:{INK};color:{ORANGE};font:800 11px/18px 'Barlow Condensed';text-align:center}}"""
