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
from card_type_provider import CardTypeProvider

FRONT_PAGE = 0.5
BACK_PAGE = 10

def print_deck(deck_definition):
    deck = Deck(deck_definition)
    draw_cut_lines(deck, FRONT_PAGE)

    card_type_provider = CardTypeProvider()
    row = -1
    column = deck.columns
    cards = deck.definition['Cards']
    # print(yaml.safe_dump(cards, sort_keys=False))
    card_backs = []
    for card_name in cards:
        card_definition = cards[card_name]
        print(f'printing card {card_name}')
        column += 1
        if column >= deck.columns:
            column = 0
            row += 1
        if row >= deck.rows:
            row = 0
            new_page(deck, BACK_PAGE)
            for card_back in card_backs:
                card_back.draw_back()
            card_backs = []
            new_page(deck, FRONT_PAGE)
        card_type = card_type_provider.get_card_type(card_definition['Type'])
        card = card_type(deck, card_definition, deck.canvas, column, row)
        card.draw()
        card_backs.append(card)

    if len(card_backs) > 0:
        new_page(deck, BACK_PAGE)
        for card_back in card_backs:
            card_back.draw_back()
        card_backs = []
    deck.canvas.showPage()
    deck.canvas.save()


def draw_cut_lines(deck: Deck, line_width):
    deck.canvas.setLineWidth(line_width)
    # self.pdf.setFillColor(colors.black)
    for column in range(deck.columns + 1):
        deck.canvas.line(column * deck.card_width + deck.page_left_margin, 0, column * deck.card_width + deck.page_left_margin, deck.page_height)
    for row in range(deck.rows + 1):
        deck.canvas.line(0, row * deck.card_height + deck.page_bottom_margin, deck.page_width, row * deck.card_height + deck.page_bottom_margin)

def new_page(deck: Deck, line_width):
    deck.canvas.showPage()
    draw_cut_lines(deck, line_width)
