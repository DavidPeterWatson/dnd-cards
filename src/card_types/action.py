from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Action'

class Action(Card):

    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            return True
        return False

