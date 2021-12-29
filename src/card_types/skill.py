from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Skill'


class Skill(Card):

    def draw_specifications(self):
        try:
            self.draw_specification('Strength', '+', 0, TA_LEFT)
            return
        except Exception:
            traceback.print_exc()

    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            return True
        return False
