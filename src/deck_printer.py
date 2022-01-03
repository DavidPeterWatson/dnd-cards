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
from card import Card
from card_back import CardBack
from position import Position

FRONT_PAGE = 0.5
BACK_PAGE = 10

def print_decks(decks):
    for deck in decks:
        print_deck(deck)

def print_deck(deck: Deck):
    draw_cut_lines(deck, FRONT_PAGE)
    row = -1
    column = deck.style.columns
    cards: list[Card] = deck.cards
    card_backs: list[CardBack] = []
    for card in cards:
        print(f'printing card {card.name}')
        column += 1
        if column >= deck.style.columns:
            column = 0
            row += 1
        if row >= deck.style.rows:
            row = 0
            if deck.collate:
                new_page(deck, BACK_PAGE)
                for card_back in card_backs:
                    print(f'printing back of card {card_back.card.name}')
                    card_back.draw_back()
                card_backs = []
            new_page(deck, FRONT_PAGE)
        front_position = Position(deck.style, deck.canvas, column, row)
        card.draw_front(front_position)
        back_card = CardBack(card, front_position)
        card_backs.append(back_card)

    if not deck.collate:
        row = 0
        column = -1
        new_page(deck, BACK_PAGE)
        for card_back in card_backs:
            print(f'printing back of card {card_back.card.name}')
            column += 1
            if column >= deck.style.columns:
                column = 0
                row += 1
            if row >= deck.style.rows:
                row = 0
                new_page(deck, BACK_PAGE)
            card_back.draw_back()
    else:
        if len(card_backs) > 0:
            new_page(deck, BACK_PAGE)
            for card_back in card_backs:
                print(f'printing back of card {card_back.card.name}')
                card_back.draw_back()
            card_backs = []
    deck.canvas.showPage()
    deck.canvas.save()


def draw_cut_lines(deck: Deck, line_width):
    deck.canvas.setLineWidth(line_width)
    # self.pdf.setFillColor(colors.black)
    for column in range(deck.style.columns + 1):
        deck.canvas.line(column * deck.style.card_width + deck.style.page_left_margin, 0, column * deck.style.card_width + deck.style.page_left_margin, deck.style.page_height)
    for row in range(deck.style.rows + 1):
        deck.canvas.line(0, row * deck.style.card_height + deck.style.page_bottom_margin, deck.style.page_width, row * deck.style.card_height + deck.style.page_bottom_margin)

def new_page(deck: Deck, line_width):
    deck.canvas.showPage()
    draw_cut_lines(deck, line_width)
