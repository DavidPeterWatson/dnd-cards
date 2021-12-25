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
from reportlab.lib.units import mm

from deck import Deck
from card import print_card

def print_deck(deck_definition):
    deck = Deck(deck_definition)
    draw_cut_lines(deck)

    header = deck.style['Header']
    header_font = header['Font']
    header_font_path = os.path.join(deck.style_path, header_font)
    pdfmetrics.registerFont(TTFont(header_font, header_font_path))

    detail = deck.style['Detail']
    detail_font = detail['Font']
    detail_font_path = os.path.join(deck.style_path, detail_font)
    pdfmetrics.registerFont(TTFont(detail_font, detail_font_path))


    row = -1

    column = deck.columns
    cards = deck.definition['Cards']
    print(yaml.safe_dump(cards, sort_keys=False))
    for card in cards:
        column += 1
        if column >= deck.columns:
            column = 0
            row += 1
        if row >= deck.rows:
            row = 0
            new_page(deck)
        print_card(deck, cards[card], deck.canvas, column, row)

    deck.canvas.showPage()
    deck.canvas.save()

def draw_cut_lines(deck: Deck):
    deck.canvas.setLineWidth(1)
    for column in range(deck.columns + 1):
        deck.canvas.line(column * deck.card_width + deck.page_left_margin, 0, column * deck.card_width + deck.page_left_margin, deck.page_height)
    for row in range(deck.rows + 1):
        deck.canvas.line(0, row * deck.card_height + deck.page_bottom_margin, deck.page_width, row * deck.card_height + deck.page_bottom_margin)

def new_page(deck: Deck):
    deck.canvas.showPage()
    draw_cut_lines(deck)
