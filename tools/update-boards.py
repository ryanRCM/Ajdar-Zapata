"""Mama's corrections (Ryan, 16-17 Nov 2026) on the board design the TVs are built from: reads
menu/Ajdar_Zapata_Boards_original.pdf (Ryan's 30 Oct design, kept as it was) and writes menu/Ajdar_Zapata_Boards.pdf.
Only board 1 changes; boards 2 and 3 are copied as they are.

  Starters  · No. 9 Cheesy Corn Balls removed (Coleslaw moves up; numbers kept).
  Sauces    · Cheddar Sauce and Green Sauce removed.
  Drinks    · Pepsi removed from the soft-drinks line (English and Persian: the original lettering, with the gap
              closed, nothing retyped). Soft drinks £1.00 -> £1.50; Sparkling Water £1.30 -> £2.00 (Ayran stays £2.00).

The new prices are made of the board's own glyphs: the 5 of £5.49 moved into £1.00, Ayran's £2.00 copied onto Sparkling
Water. Coordinates are PDF points from the TOP of the 810 x 1440 page, as pdftotext -bbox reports them.
Then rebuild the TVs: pdftoppm -png -r 108 -f 1 -l 3 menu/Ajdar_Zapata_Boards.pdf site/board, and the scripts in
CLAUDE.md (yellow-boards, orange-boards, build-walls, build-sauces).
    python3 tools/update-boards.py
"""
import io
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from pypdf.generic import ContentStream, NameObject
from reportlab.pdfgen import canvas

SRC, OUT = 'menu/Ajdar_Zapata_Boards_original.pdf', 'menu/Ajdar_Zapata_Boards.pdf'
PW, PH = 810, 1440
BLACK, ORANGE = (18, 17, 16), (240, 124, 26)
PRICE = 37.43                     # the board's price size
BASE = 0.7517                     # baseline = top of the text box + BASE * size (measured on the board's own lines)

# (x0, y0, x1, y1) boxes, top-based.
REMOVE = [
    (40, 631.5, 775, 726.5),      # rows 9 (Cheesy Corn Balls) and 10 (Coleslaw comes back, moved up)
    (285, 907.5, 526, 963),       # Cheddar Sauce cell, with its divider
    (532, 907.5, 775, 963),       # Green Sauce cell, with its divider
    (254, 1040, 482, 1069),       # English soft-drinks line from PEPSI to the end (the rest moves left)
    (300, 1072, 532.6, 1098),     # Persian soft-drinks line from its start to the end of Pepsi (the rest moves right)
    (735.6, 1050, 750.4, 1089),   # the first 0 after the point in £1.00 (soft drinks): a 5 goes there
    (695, 1157, 770, 1196),       # £1.30 (Sparkling Water)
]
MOVE = [
    ((40, 678.3, 775, 726.5), 0, -47.3),     # Coleslaw into row 9's place
    ((303.2, 1040, 482, 1069), -48.9, 0),    # "FANTA · 7UP · STILL WATER" closes up over "PEPSI · "
    ((300, 1072, 484.6, 1098), 48.1, 0),     # Persian "...فانتا،" closes up over "پپسی،"
    # Prices are built from the board's own lettering (its figures are all one width, so they line up exactly):
    ((715.3, 256.4, 729.5, 294.1), 21.17, 794.25),   # the 5 of £5.49 (row 1) into £1.00 -> £1.50
    ((695, 1110.7, 770, 1148.4), 0, 47.2),           # Ayran's £2.00 copied onto Sparkling Water
]
TEXT = []  # nothing typed: every new price is made of the board's own glyphs (MOVE above)


def clip_ops(rects, outside=False):
    s = f'0 0 {PW} {PH} re ' if outside else ''
    for x0, y0, x1, y1 in rects:
        s += f'{x0} {PH - y1} {x1 - x0} {y1 - y0} re '
    return s + ('W* n ' if outside else 'W n ')


def clipped(page, reader, ops):
    w = PdfWriter(); p = w.add_page(page)
    data = ContentStream(p.get_contents(), reader).get_data()
    p[NameObject('/Contents')] = ContentStream(None, reader)
    p[NameObject('/Contents')].set_data(b'q ' + ops.encode() + b'\n' + data + b'\nQ')
    return p


def drawn(fn):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(PW, PH)); fn(c); c.save(); buf.seek(0)
    return PdfReader(buf).pages[0]


def underlay(c):
    """The board's black under the whole page, so cut edges blend into black (no seams)."""
    c.setFillColorRGB(*[v / 255 for v in BLACK]); c.rect(0, 0, PW, PH, stroke=0, fill=1)


def overlay(c):
    c.setFillColorRGB(*[v / 255 for v in ORANGE])
    for x, top, t in TEXT: c.drawRightString(x, PH - (top + BASE * PRICE), t)


reader = PdfReader(SRC)
out = PdfWriter()
for i, page in enumerate(reader.pages):
    if i != 0:
        out.add_page(page); continue
    new = PageObject.create_blank_page(width=PW, height=PH)
    new.merge_page(drawn(underlay))   # first, so the cut edges blend into black (no seams)
    new.merge_page(clipped(page, reader, clip_ops(REMOVE, outside=True)))
    for box, dx, dy in MOVE:
        new.merge_transformed_page(clipped(page, reader, clip_ops([box])), Transformation().translate(dx, -dy))
    new.merge_page(drawn(overlay))
    out.add_page(new)
out.add_metadata({'/Title': 'Ajdar Zapata boards'})
out.write(OUT)
print('wrote', OUT)
