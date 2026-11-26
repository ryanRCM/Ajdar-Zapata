"""Before a menu change goes live: what changed since the live menu, and does every output say exactly what the list says.
The one list is tools/make-menu.py (Ryan, 26 Nov 2026: "no more mix-ups"). This shows every change against the live
menu (origin/main, or --ref), for Ryan to confirm, then checks the three outputs word for word:
  the A4 to send out (menu/a4/*.dc.html), the TV panels (tools/.sections-1.html, -2.html) and the printed / phone menu
  (menu/menu.html), plus the number ranges in the TV pages' picture labels and the phone number.
    python3 tools/menu-check.py              # changes since origin/main, then all checks
    python3 tools/menu-check.py --ref c00ca01
    python3 tools/menu-check.py --diff       # only the changes (for Ryan to confirm before building)
Exit code 1 if any output is wrong.
"""
import ast, html, os, re, runpy, subprocess, sys, tempfile

U = html.unescape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE = '020 8259 4026'
ALLERGY_EN = 'If you have a food allergy, intolerance, or coeliac disease – please speak to the staff about the ingredients in your food and drink before you order. Thank you.'
ALLERGY_FA = 'اگر حساسیت یا عدم تحمل غذایی یا بیماری سلیاک دارید، لطفاً پیش از سفارش دربارهٔ مواد غذا و نوشیدنی با کارکنان ما صحبت کنید. سپاسگزاریم.'


def load(source):
    """Run a copy of the list in a scratch folder (it writes menu/menu.html when it runs) and return its contents."""
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, 'menu')); p = os.path.join(d, 'make-menu.py')
        open(p, 'w').write(source); here = os.getcwd(); os.chdir(d)
        try:
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()): g = runpy.run_path(p)
        finally: os.chdir(here)
    items = {x['n']: dict(x, section=t) for _, _, ss in g['PAGES'] for t, fa, its in ss if isinstance(its, list) for x in its}
    return items, g['SAUCES'], g['DRINKS'], [t for _, _, ss in g['PAGES'] for t, fa, its in ss if isinstance(its, list)]


def diff(ref):
    try: old_src = subprocess.check_output(['git', '-C', ROOT, 'show', f'{ref}:tools/make-menu.py'], text=True)
    except subprocess.CalledProcessError: print(f'(no {ref} to compare with)'); return
    a, sa, da, _ = load(old_src); b, sb, db, _ = load(open(os.path.join(ROOT, 'tools/make-menu.py')).read())
    out = []
    for n in sorted(set(a) | set(b)):
        if n not in a: out.append(f'+ NEW {n} {b[n]["en"]} {b[n]["price"]} ({b[n]["section"]})'); continue
        if n not in b: out.append(f'- GONE {n} {a[n]["en"]} {a[n]["price"]}'); continue
        for k, label in (('en', 'name'), ('fa', 'Persian name'), ('price', 'price'), ('den', 'ingredients'), ('dfa', 'Persian ingredients'), ('badge', 'tag'), ('section', 'section')):
            if a[n].get(k) != b[n].get(k): out.append(f'~ {n} {label}: {a[n].get(k)!r} -> {b[n].get(k)!r}')
    if sa != sb: out.append(f'~ sauces: {[s for s, _ in sa]} -> {[s for s, _ in sb]}' + ('' if [s for s, _ in sa] != [s for s, _ in sb] else ' (Persian changed)'))
    da_, db_ = {d[0]: d for d in da}, {d[0]: d for d in db}
    for n in sorted(set(da_) | set(db_)):
        if da_.get(n) != db_.get(n): out.append(f'~ drink {n}: {da_.get(n)} -> {db_.get(n)}')
    print(f'Changes since {ref} ({len(out)}):'); print('\n'.join('  ' + o for o in out) if out else '  none')


def check():
    items, sauces, drinks, sections = load(open(os.path.join(ROOT, 'tools/make-menu.py')).read())
    bad = []
    rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
    # 1. the A4 to send out
    try:
        a4 = rd('menu/a4/Main.dc.html') + rd('menu/a4/Back.dc.html')
        rows = re.findall(r'<div class="r"><span class="n">(\d+)</span><div class="b"><div class="l1"><span class="t">(.*?)</span><span class="f">(.*?)</span><span class="p">(.*?)</span></div>(?:<div class="d">(.*?)</div>)?(?:<div class="dfa">(.*?)</div>)?</div></div>', a4)
        got = {int(n): (U(en), U(fa), U(p).replace('<br>', ' · '), U(d), U(dfa)) for n, en, fa, p, d, dfa in rows}
        if len(rows) != len(got): bad.append('A4: an item number is on it twice')
        for n, x in items.items():
            want = (x['en'], x['fa'], x['price'], x['den'], x['dfa'])
            if n not in got: bad.append(f'A4: {n} {x["en"]} missing')
            elif got[n] != want: bad.append(f'A4: {n} differs: {got[n]} vs list {want}')
        for n in set(got) - set(items): bad.append(f'A4: {n} is not in the list')
        s = [(U(a), U(b)) for a, b in re.findall(r'<div class="s"><span>([^<]*)</span><em>([^<]*)</em></div>', a4)]
        if s != list(sauces): bad.append(f'A4 sauces {s} vs list {sauces}')
        d = [(int(n), U(a), U(b), p) for n, a, b, p in re.findall(r'<div class="s"><span><b class="dn">(\d+)</b>(.*?) <em>(.*?)</em></span><strong>(.*?)</strong></div>', a4)]
        if d != list(drinks): bad.append(f'A4 drinks differ from the list')
        if PHONE not in a4 or '07773' in a4: bad.append('A4: phone must be 020 8259 4026 only')
    except FileNotFoundError as e: bad.append(f'A4 not built: {e.filename}')
    # 2. the TV panels (what tools/sections.cjs photographs)
    src = rd('tools/make-sections.py'); tree = ast.parse(src)
    const = {t.id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) for t in n.targets
             if isinstance(t, ast.Name) and t.id in ('DESC', 'HALVES', 'KEY')}
    strip = lambda s: ' '.join(U(re.sub(r'<[^>]+>', ' ', s)).split())
    for mon in (1, 2):
        try: tv = rd(f'tools/.sections-{mon}.html')
        except FileNotFoundError: bad.append(f'TV panels {mon} not built'); continue
        secs = dict(re.findall(r'<div class="sec[^"]*" id="(\w+)"(.*?)(?=<div class="sec[^"]*" id=|</body>)', tv, re.S))
        seen = set()
        for sid, body in secs.items():
            for r in re.split(r'(?=<div class="r">)', body)[1:]:
                m = re.match(r'<div class="r"><span class="n">(\d+)</span>', r)
                if not m or sid == 'drinks': continue
                n = int(m.group(1)); seen.add(n); x = items.get(n); full = strip(r)
                if not x: bad.append(f'TV{mon}: {n} is not in the list'); continue
                need = [x['en'].upper().split(' · ')[0], x['fa']] + [p.replace('M ', '').replace('L ', '') for p in x['price'].split(' · ')]
                if sid in const['DESC'] and x['den']: need.append(x['den'])
                for v in need:
                    if v not in full: bad.append(f'TV{mon}: {n} missing "{v[:50]}"')
        for n in set(items) - seen: bad.append(f'TV{mon}: {n} {items[n]["en"]} missing')
        sv = strip(secs.get('sauces', ''))
        for a, b in sauces:
            if a.upper() not in sv or b not in sv: bad.append(f'TV{mon}: sauce {a} missing')
        dv = strip(secs.get('drinks', ''))
        for n, a, b, p in drinks:
            if f'{n} {a.upper().split(" · ")[0]}' not in dv or p not in dv or b not in dv: bad.append(f'TV{mon}: drink {n} {a} wrong')
    shown = {k for c in const['HALVES'].values() for col in c for k in col}
    for t in sections:
        k = const['KEY'].get(t)
        if not k: bad.append(f'TV: new section {t} has no key in make-sections.py (KEY, WIDTH, HALVES)')
        elif k not in shown: bad.append(f'TV: section {t} is on neither TV (HALVES in make-sections.py)')
    # 3. the printed / phone menu
    try:
        pm = rd('menu/menu.html')
        for n, x in items.items():
            for k in ('en', 'fa', 'price', 'den', 'dfa'):
                if x[k] and html.escape(x[k]) not in pm: bad.append(f'phone menu: {n} {k} missing')
        if '07773' in pm: bad.append('phone menu: old mobile number 07773 001111')
        pages = int(re.search(r'Pages:\s+(\d+)', subprocess.check_output(['pdfinfo', os.path.join(ROOT, 'menu/Ajdar_Zapata_Menu.pdf')], text=True)).group(1))
        shown = len(re.findall(r'src="/menu/page-\d+\.png"', rd('site/menu/index.html')))
        if pages != shown: bad.append(f'phone menu: the PDF has {pages} pages but site/menu/index.html shows {shown}')
    except FileNotFoundError: bad.append('phone menu not built')
    # 4. the number ranges in the TV pages' picture labels ("Burgers, 16 to 21")
    for page in ('site/monitor-1/index.html', 'site/monitor-2/index.html'):
        for label, lo, hi in re.findall(r'alt="([^",]+), (\d+) to (\d+)"', rd(page)):
            norm = lambda t: ' '.join(t.lower().replace('&', 'and').split())
            nums = sorted(n for n, x in items.items() if norm(x['section']) == norm(label))
            if not nums: bad.append(f'{page}: label "{label}" matches no section in the list'); continue
            if (int(lo), int(hi)) != (nums[0], nums[-1]): bad.append(f'{page}: label "{label}, {lo} to {hi}" but the list has {nums[0]} to {nums[-1]}')
    # 5. the food allergy notice: exactly the Food Standards Agency sign (Ryan, 26 Nov 2026), on the A4, the TVs and the phone menu
    for f in ('menu/a4/Back.dc.html', 'site/monitor-1/index.html', 'menu/menu.html'):
        t = U(rd(f))
        if ALLERGY_EN not in t or ALLERGY_FA not in t: bad.append(f'{f}: the food allergy notice is not exactly the FSA sign')
    print(f'Checked {len(items)} items, {len(sauces)} sauces, {len(drinks)} drinks on the A4, both TVs and the phone menu:',
          'all match the list' if not bad else f'{len(bad)} problems')
    for b in bad: print('  ✗', b)
    return not bad


if __name__ == '__main__':
    a = sys.argv[1:]; ref = a[a.index('--ref') + 1] if '--ref' in a else 'origin/main'
    diff(ref)
    if '--diff' not in a: sys.exit(0 if check() else 1)
