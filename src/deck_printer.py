# from borb.pdf.document import Document
# from borb.pdf.page.page import Page
# from borb.pdf.pdf import PDF
# from borb.pdf.canvas.layout.image.image import Image
# from borb.pdf.canvas.layout.layout_element import Alignment
# from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
# from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
import yaml
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from card_printer import print_card

def print_deck(deck):
    canvas = Canvas(deck['Name'] + '.pdf')
    style = deck['Deck Styles'][deck['Style']]
    root_folder = deck['Root Folder']
    style_folder = style['StyleFolder']

    header = style['Header']
    header_font = header['Font']
    header_font_path = os.path.join(root_folder, style_folder, header_font)
    pdfmetrics.registerFont(TTFont(header_font, header_font_path))

    detail = style['Detail']
    detail_font = detail['Font']
    detail_font_path = os.path.join(root_folder, style_folder, detail_font)
    pdfmetrics.registerFont(TTFont(detail_font, detail_font_path))

    row = -1
    columns = style['Columns']
    rows = style['Columns']
    column = columns
    cards = deck['Cards']
    print(yaml.safe_dump(cards, sort_keys=False))
    for card in cards:
        column += 1
        if column >= columns:
            column = 0
            row += 1
        if row >= rows:
            row = 0
            canvas.showPage()
        print_card(deck, cards[card], canvas, column, row)

    canvas.showPage()
    canvas.save()