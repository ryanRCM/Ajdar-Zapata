"""The menu as A4 pages to print or send for checking (Ryan, 16 Nov 2026: "just the menu, not the TV menu, in PDF").
Puts each page of the current board design (menu/Ajdar_Zapata_Boards.pdf, the source of every price on the TVs)
onto its own A4 page, as vector, so nothing is retyped and it prints sharp.
    python3 tools/menu-a4.py   ->  menu/Ajdar_Zapata_Menu_A4.pdf
"""
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
A4W, A4H, M = 595.28, 841.89, 22
w = PdfWriter()
for page in PdfReader('menu/Ajdar_Zapata_Boards.pdf').pages:
    pw, ph = float(page.mediabox.width), float(page.mediabox.height)
    s = min((A4W - 2 * M) / pw, (A4H - 2 * M) / ph)
    out = PageObject.create_blank_page(width=A4W, height=A4H)
    out.merge_transformed_page(page, Transformation().scale(s).translate((A4W - pw * s) / 2, (A4H - ph * s) / 2))
    w.add_page(out)
w.add_metadata({'/Title': 'Ajdar Zapata menu'})
w.write('menu/Ajdar_Zapata_Menu_A4.pdf')
