"""Draft printed menu with Mama's notebook changes (18 Nov 2026), for Mama to check before anything goes live.
Changed prices show the old price; anything Claude had to assume from the handwriting carries a yellow question.
    python3 tools/draft-menu.py   ->  menu/draft/Ajdar_Zapata_Menu_DRAFT.pdf  (via Chromium print)
"""
import html, json, subprocess, pathlib
OUT_HTML = pathlib.Path('menu/draft/menu-draft.html')

def it(n, en, fa, price, old=None, den='', dfa='', badge='', q=''):
    return dict(n=n, en=en, fa=fa, price=price, old=old, den=den, dfa=dfa, badge=badge, q=q)

ZS, ZSF = 'with Zapata special sauce.', 'با سس مخصوص زاپاتا.'
PAGES = [
 ('Starters & Sides', 'پیش‌غذا', [
   ('STARTERS & SIDES', 'پیش‌غذا', [
     it(1, 'Chicken Wings · 5 pcs', 'بال مرغ ۵ تکه', '£5.49'),
     it(2, 'Chicken Wings · 8 pcs', 'بال مرغ ۸ تکه', '£7.99'),
     it(3, 'Fries', 'چیپس', '£2.99'),
     it(4, 'Cheesy Fries', 'چیپس پنیری', '£3.99'),
     it(5, 'Peri Peri Fries', 'چیپس پری‌پری', '£3.49'),
     it(6, 'Zapata Loaded Fries', 'چیپس ویژه زاپاتا', '£7.99', den='Chips, cheese, olives & beef salami.', dfa='چیپس، پنیر، زیتون و کالباس گوشت.'),
     it(7, 'Chicken Nuggets', 'ناگت مرغ', '£4.99'),
     it(8, 'Mexican Corn Cup', 'لیوان ذرت مکزیکی', '£8.99', den='Sweetcorn, mushroom, butter, lemon juice, cheese, mayonnaise & thyme, served in a cup.', dfa='ذرت شیرین، قارچ، کره، آبلیمو، پنیر، مایونز و آویشن، سرو در لیوان.'),
     it(10, 'Coleslaw', 'سالاد کلم', '£3.99', den='White cabbage, carrot, mayonnaise, lemon juice, salt & black pepper.', dfa='کلم سفید، هویج، مایونز، آبلیمو، نمک و فلفل سیاه.',
        q='قیمت پیش‌غذاها در دفترچه نبود، پس همه مثل قبل ماند. درست است؟'),
   ]),
   ('SAUCE SELECTION', 'انتخاب سس', 'SAUCES'),
 ]),
 ('Sandwiches & Burgers', 'ساندویچ و برگر', [
   ('SANDWICHES', 'ساندویچ', [
     it(11, 'Beef Salami Sandwich', 'ساندویچ کالباس گوشت', '£13.00', '£7.50', 'Beef salami, pickles, lettuce & tomato in a baguette ' + ZS, 'کالباس گوشت، خیارشور، کاهو و گوجه در نان باگت ' + ZSF, q='از ۷٫۵۰ به ۱۳ پوند. درست است؟'),
     it(12, 'Chicken Salami Sandwich', 'ساندویچ کالباس مرغ', '£12.00', '£7.50', 'Chicken salami, pickles, lettuce & tomato in a baguette ' + ZS, 'کالباس مرغ، خیارشور، کاهو و گوجه در نان باگت ' + ZSF, q='از ۷٫۵۰ به ۱۲ پوند. درست است؟'),
     it(13, 'Mixed Salami Sandwich', 'ساندویچ کالباس میکس', '£12.50', '£9.99', 'Chicken & beef salami, pickles, lettuce & tomato in a baguette ' + ZS, 'کالباس مرغ و گوشت، خیارشور، کاهو و گوجه در نان باگت ' + ZSF),
     it(14, 'Royal Zapata Sandwich', 'ساندویچ رویال زاپاتا', '£21.50', '£18.99', '1 beef steak, 2 slices beef salami, 1 hot dog, mushroom, cheese, pickles, tomato & pickle sauce in a baguette ' + ZS, '۱ استیک گوشت، ۲ ورق کالباس گوشت، ۱ عدد هات‌داگ، قارچ، پنیر، خیارشور، گوجه و سس خیارشور در نان باگت ' + ZSF, q='«سس خیارشور» را اضافه کردم. درست است؟'),
     it(15, 'Giant Ajdar Zapata', 'غول اژدر زاپاتا', '£22.50', '£19.99', '1 beef steak, 1 chicken steak, 2 slices salami, 1 hot dog, 1 beef patty, mushroom, cheese, pickles, tomato & pickle sauce in a baguette ' + ZS, '۱ استیک گوشت، ۱ استیک مرغ، ۲ ورق کالباس، ۱ عدد هات‌داگ، ۱ برگر گوشت، قارچ، پنیر، خیارشور، گوجه و سس خیارشور در نان باگت ' + ZSF, badge='NEW'),
   ]),
   ('BURGERS', 'برگر', [
     it(16, 'Classic Burger', 'برگر کلاسیک', '£9.50', '£9.99', 'Beef patty, pickles, tomato, lettuce & Zapata special sauce.', 'برگر گوشت، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(17, 'Double Cheeseburger', 'دبل چیزبرگر', '£11.50', '£10.99', 'Two beef patties, cheese, pickles, tomato, lettuce & Zapata special sauce.', 'دو برگر گوشت، پنیر، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(18, 'Royal Zapata Burger', 'رویال برگر زاپاتا', '£13.50', '£13.99', 'Two beef patties, 2 slices salami, mushroom, cheese, pickles, tomato, lettuce & Zapata special sauce.', 'دو برگر گوشت، ۲ ورق کالباس، قارچ، پنیر، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.'),
     it(19, 'Chicken Fillet Burger', 'فیله برگر مرغ', '£9.50', '£9.49', '1 chicken fillet, pickles, tomato, lettuce & Zapata special sauce.', '۱ فیله مرغ، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.', q='کنار ۱۹ یک ضربدر زده بودی. یعنی چه؟'),
     it('+', 'Zapata Chicken Fillet Burger', 'فیله برگر مرغ زاپاتا', '£ ?', None, 'Chicken fillet, cheese, mushroom, pickles, tomato, lettuce & Zapata special sauce.', 'فیله مرغ، پنیر، قارچ، خیارشور، گوجه، کاهو و سس مخصوص زاپاتا.', badge='NEW', q='برگر جدید: قیمتش چند است و چه شماره‌ای بگیرد؟'),
     it(20, 'Giant Zapata Burger', 'غول برگر زاپاتا', '£18.50', '£15.99', '1 beef patty, 2 slices salami, 1 chicken fillet steak, mushroom, cheese, pickles & tomato, with Zapata special sauce & mushroom sauce.', '۱ برگر گوشت، ۲ ورق کالباس، ۱ فیله استیک مرغ، قارچ، پنیر، خیارشور و گوجه، با سس مخصوص زاپاتا و سس قارچ.', q='خیارشور، گوجه و سس قارچ را اضافه کردم. درست است؟'),
   ]),
 ]),
 ('Doner & Shawarma', 'دونر و شاورما', [
   ('DONER BAGUETTES', 'دونر باگت', [
     it(21, 'Meat Doner', 'دونر گوشت', '£11.50', '£9.50', 'Meat doner, pickles, tomato, onion & parsley in a baguette ' + ZS, 'دونر گوشت، خیارشور، گوجه، پیاز و جعفری در نان باگت ' + ZSF),
     it(22, 'Chicken Doner', 'دونر مرغ', '£10.50', '£8.50', 'Chicken doner, pickles, tomato, onion & parsley in a baguette ' + ZS, 'دونر مرغ، خیارشور، گوجه، پیاز و جعفری در نان باگت ' + ZSF),
     it(23, 'Mixed Doner', 'دونر میکس', '£11.50', '£12.99', 'Meat & chicken doner, pickles, tomato, onion & parsley in a baguette ' + ZS, 'دونر گوشت و مرغ، خیارشور، گوجه، پیاز و جعفری در نان باگت ' + ZSF, q='ارزان‌تر شد و هم‌قیمت دونر گوشت است. درست است؟'),
     it(24, 'Giant Zapata Doner', 'غول دونر زاپاتا', '£12.50', '£10.99', 'Meat & chicken doner, mushrooms, cheese, pickles, tomato, onion & parsley in a baguette ' + ZS, 'دونر گوشت و مرغ، قارچ، پنیر، خیارشور، گوجه، پیاز و جعفری در نان باگت ' + ZSF, badge='HOUSE SIGNATURE', q='کنار ۲۴ دو کلمه نوشته بودی که نخواندم. چه بود؟'),
   ]),
   ('DONER PLATTERS', 'خوراک دونر', [
     it(25, 'Meat Doner Platter', 'خوراک دونر گوشت', 'M £ ? · L £ ?', '£10.99', 'Meat doner with salad, pickles, tomato, onion & parsley on the side, baguette bread & Zapata special sauce.', 'دونر گوشت، کنارش سالاد، خیارشور، گوجه، پیاز و جعفری، نان باگت و سس مخصوص زاپاتا.'),
     it(26, 'Chicken Doner Platter', 'خوراک دونر مرغ', 'M £ ? · L £ ?', '£10.49', 'Chicken doner with salad, pickles, tomato, onion & parsley on the side, baguette bread & Zapata special sauce.', 'دونر مرغ، کنارش سالاد، خیارشور، گوجه، پیاز و جعفری، نان باگت و سس مخصوص زاپاتا.'),
     it(27, 'Mixed Doner Platter', 'خوراک دونر میکس', 'M £ ? · L £ ?', '£11.49', 'Mixed doner with salad, pickles, tomato, onion & parsley on the side, baguette bread & Zapata special sauce.', 'دونر میکس، کنارش سالاد، خیارشور، گوجه، پیاز و جعفری، نان باگت و سس مخصوص زاپاتا.', q='دو اندازه (متوسط و بزرگ): قیمت هر کدام؟ و بعد از «سالاد و …» چه نوشته بودی؟'),
   ]),
   ('SHAWARMA', 'شاورما', [
     it(28, 'Meat Shawarma', 'شاورما گوشت', '£8.49', None, 'Meat shawarma, tomato, onion, parsley, red cabbage, jalapeños, garlic or chilli sauce & Zapata special sauce, wrapped in pitta bread.', 'شاورمای گوشت، گوجه، پیاز، جعفری، کلم قرمز، هالوپینو، سس سیر یا چیلی و سس مخصوص زاپاتا، پیچیده در نان پیتا.'),
     it(29, 'Chicken Shawarma', 'شاورما مرغ', '£7.49', None, 'Chicken shawarma, tomato, onion, parsley, red cabbage, jalapeños, garlic or chilli sauce & Zapata special sauce, wrapped in pitta bread.', 'شاورمای مرغ، گوجه، پیاز، جعفری، کلم قرمز، هالوپینو، سس سیر یا چیلی و سس مخصوص زاپاتا، پیچیده در نان پیتا.'),
     it(30, 'Mixed Shawarma', 'شاورما میکس', '£9.49', None, 'Meat & chicken shawarma, tomato, onion, parsley, red cabbage, jalapeños, garlic or chilli sauce & Zapata special sauce, wrapped in pitta bread.', 'شاورمای گوشت و مرغ، گوجه، پیاز، جعفری، کلم قرمز، هالوپینو، سس سیر یا چیلی و سس مخصوص زاپاتا، پیچیده در نان پیتا.', q='کلم قرمز، هالوپینو و سس سیر یا چیلی را اضافه کردم. قیمت‌ها مثل قبل مانده: قیمت جدید چند است؟'),
   ]),
 ]),
 ('Hot Dogs & Drinks', 'هات‌داگ و نوشیدنی', [
   ('HOT DOGS', 'هات‌داگ', [
     it(31, 'Hot Dog', 'هات‌داگ', '£8.50', '£7.99', 'Hot dog, pickles, tomato & lettuce in a baguette ' + ZS, 'هات‌داگ، خیارشور، گوجه و کاهو در نان باگت ' + ZSF),
     it(32, 'Zapata Hot Dog', 'هات‌داگ زاپاتا', '£11.50', '£8.99', 'Hot dog, mushrooms, cheese, pickles, tomato & lettuce in a baguette ' + ZS, 'هات‌داگ، قارچ، پنیر، خیارشور، گوجه و کاهو در نان باگت ' + ZSF),
     it(33, 'Doner Hot Dog', 'هات‌داگ دونر', '£14.50', '£9.99', 'Hot dog, meat doner, mushrooms, cheese, pickles, tomato & lettuce in a baguette ' + ZS, 'هات‌داگ، دونر گوشت، قارچ، پنیر، خیارشور، گوجه و کاهو در نان باگت ' + ZSF),
     it(34, 'Ajdar Hot Dog', 'هات‌داگ اژدر', '£15.50', '£11.99', 'Hot dog, 2 slices beef salami, 1 chicken fillet steak, mushrooms, cheese & pickle sauce in a baguette ' + ZS, 'هات‌داگ، ۲ ورق کالباس گوشت، ۱ فیله استیک مرغ، قارچ، پنیر و سس خیارشور در نان باگت ' + ZSF, q='برای ۳۲ تا ۳۴ یک سس نوشته بودی. سس خیارشور است؟ برای هر سه؟'),
     it(35, 'Sosis Bandari', 'سوسیس بندری', '£9.50', '£8.99', 'Sausage with pickles, tomato, onion, parsley & spicy sauce, served in a baguette.', 'سوسیس با خیارشور، گوجه، پیاز و جعفری و سس تند، سرو در نان باگت.', badge='NEW'),
   ]),
   ('DRINKS', 'نوشیدنی‌ها', 'DRINKS'),
 ]),
]
SAUCES = [('Zapata Special Sauce', 'سس مخصوص زاپاتا'), ('Garlic', 'سس سیر'), ('Garlic & Dill', 'سس سیر و شوید'), ('Spicy Chilli', 'سس چیلی تند'), ('Mushroom', 'سس قارچ'), ('Ketchup', 'سس کچاپ'), ('Mayo', 'سس مایونز')]
DRINKS = [(36, 'Coca-Cola', 'کوکاکولا', '£1.50'), (37, 'Diet Coke', 'کوکا رژیمی', '£1.50'), (39, 'Fanta', 'فانتا', '£1.50'), (40, '7UP', 'سون‌آپ', '£1.50'),
          (41, 'Ayran', 'دوغ', '£2.00'), (42, 'Still Water', 'آب معدنی', '£1.50'), (43, 'Sparkling Water', 'آب گازدار', '£2.00')]
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
        h += ('<div class="extra"><div class="row"><span class="en">Extra cheese or a sauce of your choice</span><span class="price">£1.00</span></div>'
              '<div class="fa" dir="rtl">پنیر اضافه یا سس انتخابی</div><div class="q" dir="rtl">❓ از دفترچه: «سس انتخابی، پنیر، ۱ پوند». همین را روی منو بنویسیم؟</div></div>')
        h += ('<div class="allergy"><b>Food Allergies &amp; Intolerances</b><br>Before you order, please tell a member of our staff about any allergy or intolerance. '
              'Every dish on this menu lists its main ingredients, and full information on the 14 major allergens is available on request. '
              'Our food is prepared in a kitchen where allergens are present, so we cannot guarantee that any dish is completely free from allergens.'
              '<div dir="rtl" class="afa"><b>حساسیت و عدم تحمل غذایی</b><br>لطفاً قبل از سفارش، اگر به غذایی حساسیت یا عدم تحمل دارید به همکاران ما اطلاع دهید. '
              'مواد اصلی همه غذاها در این منو نوشته شده و اطلاعات کامل ۱۴ آلرژن اصلی در صورت درخواست در اختیار شما قرار می‌گیرد. '
              'غذاهای ما در آشپزخانه‌ای آماده می‌شوند که در آن مواد آلرژی‌زا وجود دارد، بنابراین نمی‌توانیم تضمین کنیم که هیچ غذایی کاملاً بدون آلرژن باشد.</div></div>')
    elif items == 'DRINKS':
        h += ''.join(f'<div class="item small"><span class="num">{n}</span><div class="body"><div class="row"><span class="en">{e(a)}</span><span class="price">{p}</span></div><div class="fa" dir="rtl">{e(b)}</div></div></div>' for n, a, b, p in DRINKS)
        h += '<div class="hello"><b>COME SAY HELLO.</b><br>864 High Road, London N12 9RH<br>07773 001111<br>ajdarzapata.co.uk</div>'
    else:
        h += ''.join(item(x) for x in items)
    return h + '</div>'

def page(i, p):
    title, fa, secs = p
    # two columns: first section left, the rest right (as on the printed menu)
    left, right = secs[0], secs[1:]
    return (f'<div class="page"><div class="draft" dir="rtl">پیش‌نویس برای تأیید مامان · DRAFT, not final · قیمت‌های عوض‌شده قیمت قبلی را هم نشان می‌دهند · ❓ = لطفاً جواب بده</div>'
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
.sec { margin-bottom: 3mm; }
.sh { display: flex; justify-content: space-between; font-size: 9pt; font-weight: 800; letter-spacing: .3pt; padding: 1.5mm 0 1.2mm; border-bottom: .4mm solid #3a1a00; margin-bottom: 1.6mm; }
.item { display: flex; gap: 2.2mm; padding: 1.4mm 0 1.6mm; border-bottom: .25mm solid rgba(90,30,0,.35); }
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
