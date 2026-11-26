"""The printed A4 menu, built from the list below (Mama's corrections up to 18 Nov 2026), in the look of
menu/Full_Menu_A4.pdf. Replaces tools/update-menu.py, which patched that PDF and can't renumber or add items.
18 Nov (Mama): 14 and 15 new ingredients; burgers run to 21 (18 Chicken Fillet, 19 Zapata Chicken Burger NEW (renamed Zapata Fillet Chicken Burger on 26 Nov),
20 Royal, 21 Giant), so everything after moves up one. Prices from Mama's notebook (photos, 18 Nov; written with the old numbers, mapped here).
Anything with pickle sauce has no Zapata special sauce (14, 15, 21, 33-35).
Later on 18 Nov (Mama gave the old numbers; here +1): Giant Zapata Doner without cheese; platters just 'with salad',
in medium and large (prices to come); shawarma with red cabbage, jalapeños and garlic or chilli sauce, no Zapata sauce. PLACEHOLDER prices chosen by Claude at Ryan's request (18 Nov, "u choose placeholder"), until Mama gives hers:
19 Zapata Fillet Chicken Burger £11.50; platters M/L 26 £12.50/£15.50, 27 £11.50/£14.50, 28 £13.50/£16.50.
26 Nov 2026, Mama's sheet via Ryan (his dictation, 15:17): 3 Fries M £2.99 / L £4.99; 14 and 15 + tomato; 18 £7.50; 19 £9.50;
22-25 + lettuce; 24 £12.50; 25 £17.50 + cheese + red cabbage; platters one size, with chips & salad: 26 £10.50, 27 £9.50,
28 £10.50; shawarma 29 £6.99, 30 £5.99, 31 £6.99, "with garlic and chilli sauce" (was "garlic or chilli"). No placeholder
prices left: 19 and the platters are Mama's now.
26 Nov 2026 (Ryan): English "Meat" is Lamb (doner, platter, shawarma; Persian stays گوشت, which is right); 6 Zapata Loaded Fries gets mushroom; 32 Hot Dog £9.50 (was £8.50); no NEW / HOUSE SIGNATURE tags any more; phone 020 8259 4026 only (not 07773 001111); allergy notice no longer claims every dish lists its ingredients (fries, wings, nuggets, drinks don't); 19 is now Zapata Fillet Chicken Burger (Persian فیله برگر مرغ زاپاتا is Claude's, for Mama to check).
    python3 tools/make-menu.py && node tools/menu-pdf.cjs   ->  menu/Ajdar_Zapata_Menu.pdf
"""
import html, json, subprocess, pathlib
OUT_HTML = pathlib.Path('menu/menu.html')

def it(n, en, fa, price, old=None, den='', dfa='', badge='', q=''):
    return dict(n=n, en=en, fa=fa, price=price, old=old, den=den, dfa=dfa, badge=badge, q=q)

ZS, ZSF = 'with Zapata special sauce.', 'با سس مخصوص زاپاتا.'
PAGES = [
 ('Starters & Sides', 'پیش‌غذا', [
   ('STARTERS & SIDES', 'پیش‌غذا', [
     it(1, 'Chicken Wings · 5 pcs', 'بال مرغ ۵ تکه', '£5.49'),
     it(2, 'Chicken Wings · 8 pcs', 'بال مرغ ۸ تکه', '£7.99'),
     it(3, 'Fries', 'چیپس', 'M £2.99 · L £4.99'),
     it(4, 'Cheesy Fries', 'چیپس پنیری', '£3.99'),
     it(5, 'Peri Peri Fries', 'چیپس پری‌پری', '£3.49'),
     it(6, 'Zapata Loaded Fries', 'چیپس ویژه زاپاتا', '£7.99', den='Chips, cheese, olives, mushroom & beef salami.', dfa='چیپس، پنیر، زیتون، قارچ و کالباس گوشت.'),
     it(7, 'Chicken Nuggets', 'ناگت مرغ', '£4.99'),
     it(8, 'Mexican Corn Cup', 'لیوان ذرت مکزیکی', '£8.99', den='Sweetcorn, mushroom, butter, lemon juice, cheese, mayonnaise & thyme, served in a cup.', dfa='ذرت شیرین، قارچ، کره، آبلیمو، پنیر، مایونز و آویشن، سرو در لیوان.'),
     it(10, 'Coleslaw', 'سالاد کلم', '£3.99', den='White cabbage, carrot, mayonnaise, lemon juice, salt & black pepper.', dfa='کلم سفید، هویج، مایونز، آبلیمو، نمک و فلفل سیاه.'),
   ]),
   ('SAUCE SELECTION', 'انتخاب سس', 'SAUCES'),
 ]),
 ('Sandwiches & Burgers', 'ساندویچ و برگر', [
   ('SANDWICHES', 'ساندویچ', [
     it(11, 'Beef Salami Sandwich', 'ساندویچ کالباس گوشت', '£13.00', den='Beef salami, pickles, lettuce & tomato in a baguette ' + ZS, dfa='کالباس گوشت، خیارشور، کاهو و گوجه در نان باگت ' + ZSF),
     it(12, 'Chicken Salami Sandwich', 'ساندویچ کالباس مرغ', '£12.00', den='Chicken salami, pickles, lettuce & tomato in a baguette ' + ZS, dfa='کالباس مرغ، خیارشور، کاهو و گوجه در نان باگت ' + ZSF),
     it(13, 'Mixed Salami Sandwich', 'ساندویچ کالباس میکس', '£12.50', den='Chicken & beef salami, pickles, lettuce & tomato in a baguette ' + ZS, dfa='کالباس مرغ و گوشت، خیارشور، کاهو و گوجه در نان باگت ' + ZSF),
     it(14, 'Royal Zapata Sandwich', 'ساندویچ رویال زاپاتا', '£21.50', den='1 beef steak, 1 chicken steak, 2 slices beef salami, mushroom, cheese & tomato in a baguette with pickle sauce.', dfa='۱ استیک گوشت، ۱ استیک مرغ، ۲ ورق کالباس گوشت، قارچ، پنیر و گوجه در نان باگت با سس خیارشور.'),
     it(15, 'Giant Ajdar Zapata', 'غول اژدر زاپاتا', '£22.50', den='1 beef steak, 1 chicken steak, 2 slices salami, 1 hot dog, 1 beef patty, mushroom, cheese & tomato in a baguette with pickle sauce.', dfa='۱ استیک گوشت، ۱ استیک مرغ، ۲ ورق کالباس، ۱ عدد هات‌داگ، ۱ برگر گوشت، قارچ، پنیر و گوجه در نان باگت با سس خیارشور.'),
   ]),
   ('BURGERS', 'برگر', [
     it(16, 'Classic Burger', 'برگر کلاسیک', '£9.50', den='Beef patty, pickles, tomato, lettuce & Zapata special sauce.', dfa='برگر گوشت، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(17, 'Double Cheeseburger', 'دبل چیزبرگر', '£11.50', den='Two beef patties, cheese, pickles, tomato, lettuce & Zapata special sauce.', dfa='دو برگر گوشت، پنیر، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(18, 'Chicken Fillet Burger', 'فیله برگر مرغ', '£7.50', den='1 chicken fillet, pickles, tomato, lettuce & Zapata special sauce.', dfa='۱ فیله مرغ، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(19, 'Zapata Fillet Chicken Burger', 'فیله برگر مرغ زاپاتا', '£9.50', den='Chicken fillet, cheese & mushroom, pickles, tomato, lettuce & Zapata special sauce.', dfa='فیله مرغ، پنیر و قارچ، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(20, 'Royal Zapata Burger', 'رویال برگر زاپاتا', '£13.50', den='Two beef patties, 2 slices salami, mushroom, cheese, pickles, tomato, lettuce & Zapata special sauce.', dfa='دو برگر گوشت، ۲ ورق کالباس، قارچ، پنیر، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(21, 'Giant Zapata Burger', 'غول برگر زاپاتا', '£18.50', den='1 beef patty, 2 slices salami, 1 chicken fillet steak, mushroom, cheese, pickles & tomato with pickle sauce.', dfa='۱ برگر گوشت، ۲ ورق کالباس، ۱ فیله استیک مرغ، قارچ، پنیر، خیارشور و گوجه با سس خیارشور.'),
   ]),
 ]),
 ('Doner & Shawarma', 'دونر و شاورما', [
   ('DONER BAGUETTES', 'دونر باگت', [
     it(22, 'Lamb Doner', 'دونر گوشت', '£11.50', den='Lamb doner, pickles, lettuce, tomato, onion & parsley in a baguette ' + ZS, dfa='دونر گوشت، خیارشور، کاهو، گوجه، پیاز و جعفری در نان باگت ' + ZSF),
     it(23, 'Chicken Doner', 'دونر مرغ', '£10.50', den='Chicken doner, pickles, lettuce, tomato, onion & parsley in a baguette ' + ZS, dfa='دونر مرغ، خیارشور، کاهو، گوجه، پیاز و جعفری در نان باگت ' + ZSF),
     it(24, 'Mixed Doner', 'دونر میکس', '£12.50', den='Lamb & chicken doner, pickles, lettuce, tomato, onion & parsley in a baguette ' + ZS, dfa='دونر گوشت و مرغ، خیارشور، کاهو، گوجه، پیاز و جعفری در نان باگت ' + ZSF),
     it(25, 'Giant Zapata Doner', 'غول دونر زاپاتا', '£17.50', den='Lamb & chicken doner, mushrooms, cheese, pickles, lettuce, red cabbage, tomato, onion & parsley in a baguette ' + ZS, dfa='دونر گوشت و مرغ، قارچ، پنیر، خیارشور، کاهو، کلم قرمز، گوجه، پیاز و جعفری در نان باگت ' + ZSF),
   ]),
   ('DONER PLATTERS', 'خوراک دونر', [
     it(26, 'Lamb Doner Platter', 'خوراک دونر گوشت', '£10.50', den='Lamb doner with chips & salad.', dfa='دونر گوشت با چیپس و سالاد.'),
     it(27, 'Chicken Doner Platter', 'خوراک دونر مرغ', '£9.50', den='Chicken doner with chips & salad.', dfa='دونر مرغ با چیپس و سالاد.'),
     it(28, 'Mixed Doner Platter', 'خوراک دونر میکس', '£10.50', den='Mixed lamb & chicken doner with chips & salad.', dfa='دونر میکس گوشت و مرغ با چیپس و سالاد.'),
   ]),
   ('SHAWARMA', 'شاورما', [
     it(29, 'Lamb Shawarma', 'شاورما گوشت', '£6.99', den='Lamb shawarma, tomato, onion, parsley, red cabbage & jalapeños with garlic and chilli sauce, wrapped in pitta bread.', dfa='شاورمای گوشت، گوجه، پیاز، جعفری، کلم قرمز و هالاپینو با سس سیر و چیلی، پیچیده در نان پیتا.'),
     it(30, 'Chicken Shawarma', 'شاورما مرغ', '£5.99', den='Chicken shawarma, tomato, onion, parsley, red cabbage & jalapeños with garlic and chilli sauce, wrapped in pitta bread.', dfa='شاورمای مرغ، گوجه، پیاز، جعفری، کلم قرمز و هالاپینو با سس سیر و چیلی، پیچیده در نان پیتا.'),
     it(31, 'Mixed Shawarma', 'شاورما میکس', '£6.99', den='Lamb & chicken shawarma, tomato, onion, parsley, red cabbage & jalapeños with garlic and chilli sauce, wrapped in pitta bread.', dfa='شاورمای گوشت و مرغ، گوجه، پیاز، جعفری، کلم قرمز و هالاپینو با سس سیر و چیلی، پیچیده در نان پیتا.'),
   ]),
 ]),
 ('Hot Dogs & Drinks', 'هات‌داگ و نوشیدنی', [
   ('HOT DOGS', 'هات‌داگ', [
     it(32, 'Hot Dog', 'هات‌داگ', '£9.50', den='Hot dog, pickles, tomato & lettuce in a baguette ' + ZS, dfa='هات‌داگ، خیارشور، گوجه و کاهو در نان باگت ' + ZSF),
     it(33, 'Zapata Hot Dog', 'هات‌داگ زاپاتا', '£11.50', den='Hot dog, mushrooms, cheese, tomato & lettuce in a baguette with pickle sauce.', dfa='هات‌داگ، قارچ، پنیر، گوجه و کاهو در نان باگت با سس خیارشور.'),
     it(34, 'Doner Hot Dog', 'هات‌داگ دونر', '£14.50', den='Hot dog, lamb doner, mushrooms, cheese, tomato & lettuce in a baguette with pickle sauce.', dfa='هات‌داگ، دونر گوشت، قارچ، پنیر، گوجه و کاهو در نان باگت با سس خیارشور.'),
     it(35, 'Ajdar Hot Dog', 'هات‌داگ اژدر', '£15.50', den='Hot dog, 2 slices beef salami, 1 chicken fillet steak, mushrooms & cheese in a baguette with pickle sauce.', dfa='هات‌داگ، ۲ ورق کالباس گوشت، ۱ فیله استیک مرغ، قارچ و پنیر در نان باگت با سس خیارشور.'),
     it(36, 'Sosis Bandari', 'سوسیس بندری', '£9.50', den='Sausage with pickles, tomato, onion, parsley & spicy sauce, served in a baguette.', dfa='سوسیس با خیارشور، گوجه، پیاز و جعفری و سس تند، سرو در نان باگت.'),
   ]),
   ('DRINKS', 'نوشیدنی‌ها', 'DRINKS'),
 ]),
]
SAUCES = [('Zapata Special Sauce', 'سس مخصوص زاپاتا'), ('Garlic', 'سس سیر'), ('Garlic & Dill', 'سس سیر و شوید'), ('Spicy Chilli', 'سس چیلی تند'), ('Ketchup', 'سس کچاپ'), ('Mayo', 'سس مایونز'), ('BBQ', 'سس باربیکیو')]   # Ryan, 26 Nov 2026 (photo): these six; 15:38 "add Zapata Special Sauce" (first, the house sauce). BBQ Persian is Claude's
DRINKS = [(37, 'Coca-Cola', 'کوکاکولا', '£1.50'), (38, 'Diet Coke', 'کوکا رژیمی', '£1.50'), (39, 'Fanta', 'فانتا', '£1.50'), (40, '7UP', 'سون‌آپ', '£1.50'),
          (41, 'Ayran', 'دوغ', '£2.00'), (42, 'Still Water', 'آب معدنی', '£1.50'), (43, 'Sparkling Water', 'آب گازدار', '£2.00'),
          (44, 'Istak', 'ایستک', '£1.50')]   # Mama, 24 Nov 2026: Istak £1.50. Ryan, 26 Nov 15:38: 41 just "Ayran" (دوغ), £2.00
e = html.escape

def item(x):
    num = f'<span class="num{" plus" if x["n"] == "+" else ""}">{e(str(x["n"]))}</span>'
    old = f'<div class="old">was {e(x["old"])} · قبلاً</div>' if x['old'] and x['old'] != x['price'] else ''
    badge = f'<span class="badge">{e(x["badge"])}</span>' if x['badge'] else ''
    q = f'<div class="q" dir="rtl">❓ {e(x["q"])}</div>' if x['q'] else ''
    desc = f'<div class="den">{e(x["den"])}</div>' if x['den'] else ''
    dfa = f'<div class="dfa" dir="rtl">{e(x["dfa"])}</div>' if x['dfa'] else ''
    unk = ' unk' if '?' in x['price'] else ''
    return (f'<div class="item">{num}<div class="body"><div class="row"><span class="en">{e(x["en"])}</span>'
            f'<span class="price{unk}">{e(x["price"])}</span></div>{old}{badge}{desc}<div class="fa" dir="rtl">{e(x["fa"])}</div>{dfa}{q}</div></div>')

def section(s):
    title, fa, items = s
    h = f'<div class="sec"><div class="sh"><span>{e(title)}</span><span dir="rtl">{e(fa)}</span></div>'
    if items == 'SAUCES':
        h += ''.join(f'<div class="srow"><span class="en">{e(a)}</span><span class="fa" dir="rtl">{e(b)}</span></div>' for a, b in SAUCES)
        # the food allergy notice: exactly the Food Standards Agency sign in the shop (Ryan, 26 Nov 2026 15:39: "exactly this"),
        # English, then the Persian of the same words
        h += ('<div class="allergy"><b>Food Allergy or Intolerance?</b><br>If you have a food allergy, intolerance, or coeliac disease – please speak to the staff about the ingredients in your food and drink before you order. Thank you.'
              '<div dir="rtl" class="afa"><b>حساسیت یا عدم تحمل غذایی؟</b><br>اگر حساسیت یا عدم تحمل غذایی یا بیماری سلیاک دارید، لطفاً پیش از سفارش دربارهٔ مواد غذا و نوشیدنی با کارکنان ما صحبت کنید. سپاسگزاریم.</div></div>')
    elif items == 'DRINKS':
        h += ''.join(f'<div class="item small"><span class="num">{n}</span><div class="body"><div class="row"><span class="en">{e(a)}</span><span class="price">{p}</span></div><div class="fa" dir="rtl">{e(b)}</div></div></div>' for n, a, b, p in DRINKS)
        h += '<div class="hello"><b>COME SAY HELLO.</b><br>864 High Road, London N12 9RH<br>020 8259 4026<br>ajdarzapata.co.uk</div>'
    else:
        h += ''.join(item(x) for x in items)
    return h + '</div>'

def page(i, p):
    title, fa, secs = p
    # two columns: first section left, the rest right (as on the printed menu)
    left, right = secs[0], secs[1:]
    return (f'<div class="page">'
            f'<div class="top"><span>AJDAR ZAPATA</span><span dir="rtl">اژدر زاپاتا</span></div>'
            f'<div class="title"><span>{e(title)}</span><span dir="rtl">{e(fa)}</span></div>'
            f'<div class="cols"><div class="col">{section(left)}</div><div class="col">{"".join(section(s) for s in right)}</div></div>'
            f'<div class="foot"><span>Allergies? Please tell our staff before ordering.<br><span dir="rtl">حساسیت غذایی دارید؟ لطفاً قبل از سفارش به ما بگویید.</span></span><b>{i + 1} / 4</b></div></div>')

CSS = '''
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'DejaVu Sans', sans-serif; color: #111; }
[dir=rtl], .fa, .dfa { font-family: 'Vazirmatn', 'DejaVu Sans', sans-serif; }
.page { width: 210mm; height: 297mm; background: #fa9817; padding: 9mm 11mm 8mm; position: relative; page-break-after: always; overflow: hidden; }
.draft { background: #fff27a; border: 1.5px dashed #8a1c00; color: #5a1400; font-size: 8.4pt; font-weight: 700; text-align: center; padding: 1.3mm 2mm; border-radius: 2mm; margin-bottom: 3mm; }
.top { background: #111; color: #fff; border-radius: 3mm; border-bottom: 1.6mm solid #e01b1b; display: flex; justify-content: space-between; align-items: center; padding: 3.2mm 6mm; font-size: 19pt; font-weight: 700; }
.title { display: flex; justify-content: space-between; align-items: baseline; font-size: 19pt; font-weight: 800; margin: 5mm 0 2.5mm; padding-bottom: 2.5mm; border-bottom: .6mm solid #c0161a; }
.cols { display: flex; gap: 8mm; }
.col { flex: 1; min-width: 0; }
.sec { margin-bottom: 5mm; }
.sh { display: flex; justify-content: space-between; font-size: 9pt; font-weight: 800; letter-spacing: .3pt; padding: 1.5mm 0 1.2mm; border-bottom: .4mm solid #3a1a00; margin-bottom: 1.6mm; }
.item { display: flex; gap: 2.2mm; padding: 2.2mm 0 2.6mm; border-bottom: .25mm solid rgba(90,30,0,.35); }
.item.small { padding: 1.2mm 0 1.3mm; }
.num { flex: 0 0 5.6mm; height: 5.6mm; border-radius: 50%; background: #d7141a; color: #fff; font-size: 7.4pt; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-top: .2mm; }
.num.plus { background: #111; }
.body { flex: 1; min-width: 0; }
.row { display: flex; justify-content: space-between; gap: 2mm; align-items: baseline; }
.en { font-size: 9pt; font-weight: 700; }
.price { font-size: 9.6pt; font-weight: 800; white-space: nowrap; }
.price.unk { background: #fff27a; padding: 0 1.2mm; border-radius: 1mm; }
.old { text-align: right; font-size: 6.6pt; color: #6b1500; margin-top: -.3mm; }
.badge { display: inline-block; background: #111; color: #fff; font-size: 5.6pt; font-weight: 700; padding: .3mm 1.4mm; border-radius: 2mm; margin: .6mm 0 .2mm; }
.den { font-size: 7.1pt; line-height: 1.28; color: #3a2310; margin-top: .4mm; }
.fa { font-size: 8.2pt; font-weight: 700; text-align: right; margin-top: .6mm; }
.dfa { font-size: 7pt; line-height: 1.45; text-align: right; color: #3a2310; }
.q { background: #fff27a; border-radius: 1.2mm; font-size: 7.2pt; font-weight: 700; color: #5a1400; padding: .8mm 1.6mm; margin-top: 1mm; text-align: right; }
.srow { display: flex; justify-content: space-between; padding: 1.5mm 0; border-bottom: .25mm solid rgba(90,30,0,.35); }
.srow .en { font-size: 8.8pt; } .srow .fa { margin: 0; font-size: 8.6pt; }
.extra { margin-top: 3mm; padding: 2mm 2.4mm; background: rgba(255,255,255,.35); border-radius: 2mm; }
.allergy { margin-top: 4mm; background: #111; color: #fff; border-radius: 2.5mm; padding: 3mm 3.4mm; font-size: 6.9pt; line-height: 1.35; }
.allergy b { font-size: 8pt; } .afa { margin-top: 2mm; text-align: right; line-height: 1.6; }
.hello { margin-top: 5mm; background: #111; color: #fff; border-radius: 2.5mm; padding: 4mm; font-size: 9pt; line-height: 1.55; }
.foot { position: absolute; left: 11mm; right: 11mm; bottom: 7mm; border-top: .3mm solid #3a1a00; padding-top: 1.6mm; display: flex; justify-content: space-between; font-size: 6.8pt; }
'''
doc = ('<!doctype html><html><head><meta charset="utf-8">'
       '<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;800&display=swap" rel="stylesheet">'
       f'<style>{CSS}</style></head><body>' + ''.join(page(i, p) for i, p in enumerate(PAGES)) + '</body></html>')
OUT_HTML.write_text(doc)
print('wrote', OUT_HTML)
