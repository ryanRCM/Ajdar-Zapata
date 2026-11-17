"""Mama's corrections to the printed menu (Ryan, 16 Nov 2026), applied to menu/Full_Menu_A4.pdf (left untouched)
and written to menu/Ajdar_Zapata_Menu.pdf. Every other word and price on the menu is kept exactly as it was.

  Starters  · No. 9 Cheesy Corn Balls removed (Coleslaw moves up; numbers kept).
            · No. 6 Zapata Loaded Fries: ingredients as Mama gave them.
  Sauces    · Cheddar Sauce and Green Sauce removed.
  Drinks    · Pepsi removed. Coca-Cola, Diet Coke, Fanta, 7UP, Still Water £1.50; Ayran and Sparkling Water £2.00.
  Contact   · phone and website as on the current boards (menu/Ajdar_Zapata_Boards.pdf).

Coordinates are PDF points measured from the TOP of the page (as pdftotext -bbox reports them).
    python3 tools/update-menu.py
"""
import io
import arabic_reshaper
from bidi.algorithm import get_display
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from pypdf.generic import ContentStream, NameObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SRC, OUT = 'menu/Full_Menu_A4.pdf', 'menu/Ajdar_Zapata_Menu.pdf'
# The pages are A4 (the crop box) inside an 8.5 pt bleed: the whole sheet is MW x MH. Positions above are measured
# from the sheet's top-left corner (as pdftotext reports them), so a sheet y is YT - top.
MW, MH = 612.2835, 858.8976
X0, YT = 0, MH
ORANGE, INK, BROWN, CREAM, BOX = (250, 152, 23), (17, 17, 17), (56, 39, 18), (255, 244, 225), (17, 17, 17)
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

# Edits, per page: regions removed (x0, y0, x1, y1), regions moved up (box, dy), and new text.
# A text item: (font, size, colour, x, top, text, align, persian). `top` is the top of the text's box as pdftotext
# reports it; the baseline is top + 0.759 * size (measured on the original's prices). Sizes match the original's.
LOADED_EN = 'Chips, cheese, olives & beef salami.'
LOADED_FA = 'چیپس، پنیر، زیتون و کالباس گوشت.'
EDITS = {
    0: {  # page 1: starters and sauces
        'remove': [(30, 401, 300, 480),            # Loaded Fries' old ingredient lines (redrawn below)
                   (30, 606.5, 300, 757.5),        # Cheesy Corn Balls and Coleslaw (Coleslaw comes back, moved up)
                   (310, 340, 580, 384.5)],        # Cheddar Sauce and Green Sauce rows
        'move': [((30, 676, 300, 757.5), -70)],    # Coleslaw into Cheesy Corn Balls' place
        'keep': [(30, 401, 300, 424)],             # Loaded Fries' name and price line stay as they were
        'text': [('DV', 8.2, BROWN, 59.5, 425.1, LOADED_EN, 'left', False),
                 ('DVB', 8.8, INK, 294.8, 438.7, 'چیپس ویژه زاپاتا', 'right', True),
                 ('DV', 7.6, BROWN, 294.8, 452.4, LOADED_FA, 'right', True)],
    },
    3: {  # page 4: drinks, contact box
        'remove': [(310, 270, 580, 533.5)],                         # Pepsi .. Sparkling
        'move': [((310, 313.8, 580, 533.5), -44)],                  # Fanta .. Sparkling up into Pepsi's place
        'keep': [],
        'cover': [((535, y, 577, y + 11), ORANGE) for y in (193.0, 237.0, 281.0, 325.0, 412.5, 456.5)]  # old prices, after moving
                 + [((328, 615, 560, 650), BOX)],                 # old phone and website, inside the dark contact box
        'text': [('DVB', 10.5, INK, 575.4, y, p, 'right', False) for y, p in
                 ((193.4, '£1.50'), (237.3, '£1.50'), (281.1, '£1.50'), (325.0, '£1.50'), (412.7, '£1.50'), (456.6, '£2.00'))]
                + [('DVB', 12.0, CREAM, 331.7, 618.3, '07773 001111', 'left', False),
                   ('DVB', 8.5, ORANGE, 331.7, 637.9, 'ajdarzapata.co.uk', 'left', False)],
    },
}


def clip_ops(rects, outside=False):
    """PDF operators that clip to the union of rects (or, outside=True, to the whole page minus them)."""
    s = f'0 0 {MW} {MH} re ' if outside else ''
    for x0, y0, x1, y1 in rects:
        s += f'{X0 + x0} {YT - y1} {x1 - x0} {y1 - y0} re '
    return s + ('W* n ' if outside else 'W n ')


def clipped(page, reader, ops):
    """A copy of `page` whose drawing is clipped by `ops`."""
    w = PdfWriter(); p = w.add_page(page)
    cs = ContentStream(p.get_contents(), reader)
    p[NameObject('/Contents')] = ContentStream(None, reader)
    data = b'q ' + ops.encode() + b'\n' + cs.get_data() + b'\nQ'
    p[NameObject('/Contents')].set_data(data)
    return p


def underlay(e):
    """The page's background where regions were cut out: orange, and anything listed in 'fill'."""
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(MW, MH))
    c.setFillColorRGB(*[v / 255 for v in ORANGE]); c.rect(0, 0, MW, MH, stroke=0, fill=1)
    for (x0, y0, x1, y1), col in e.get('fill', []):
        c.setFillColorRGB(*[v / 255 for v in col]); c.rect(X0 + x0, YT - y1, x1 - x0, y1 - y0, stroke=0, fill=1)
    c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]


def overlay(e):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(MW, MH))
    for (x0, y0, x1, y1), col in e.get('cover', []):
        c.setFillColorRGB(*[v / 255 for v in col]); c.rect(X0 + x0, YT - y1, x1 - x0, y1 - y0, stroke=0, fill=1)
    for font, size, col, x, top, text, align, fa in e['text']:
        if fa: text = get_display(arabic_reshaper.reshape(text))
        c.setFont(font, size); c.setFillColorRGB(*[v / 255 for v in col])
        base = YT - (top + 0.759 * size)
        (c.drawRightString if align == 'right' else c.drawString)(X0 + x, base, text)
    c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]


reader = PdfReader(SRC)
out = PdfWriter()
for i, page in enumerate(reader.pages):
    e = EDITS.get(i)
    if not e:
        out.add_page(page); continue
    new = PageObject.create_blank_page(width=MW, height=MH)
    for b in ('/CropBox', '/TrimBox', '/BleedBox', '/ArtBox'):
        if b in page: new[NameObject(b)] = page[b]
    new.merge_page(underlay(e))
    new.merge_page(clipped(page, reader, clip_ops(e['remove'], outside=True)))
    if e['keep']:
        new.merge_page(clipped(page, reader, clip_ops(e['keep'])))
    for box, dy in e['move']:
        new.merge_transformed_page(clipped(page, reader, clip_ops([box])), Transformation().translate(0, -dy))
    new.merge_page(overlay(e))
    out.add_page(new)
out.add_metadata({'/Title': 'Ajdar Zapata menu'})
out.write(OUT)
print('wrote', OUT)
