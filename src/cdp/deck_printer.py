from cdp.deck import Deck
from cdp.card import Card
from cdp.card_back import CardBack
from cdp.position import Position
from cdp.card_box import CardBox
import os

FRONT_PAGE = 0.5
BACK_PAGE = 10

def render_decks(decks):
    for deck in decks:
        render_deck(deck)

def render_deck(deck: Deck):
    output_folder = deck.style.output_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder) 
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

    cardbox = CardBox(deck)
    cardbox.draw_box()


def draw_cut_lines(deck: Deck, line_width):
    deck.canvas.setLineWidth(line_width)
    for column in range(deck.style.columns + 1):
        deck.canvas.line(column * deck.style.card_width + deck.style.page_left_margin, 0, column * deck.style.card_width + deck.style.page_left_margin, deck.style.page_height)
    for row in range(deck.style.rows + 1):
        deck.canvas.line(0, row * deck.style.card_height + deck.style.page_bottom_margin, deck.style.page_width, row * deck.style.card_height + deck.style.page_bottom_margin)

def new_page(deck: Deck, line_width):
    deck.canvas.showPage()
    draw_cut_lines(deck, line_width)
