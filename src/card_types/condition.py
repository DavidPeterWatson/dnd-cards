from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Condition'


class Condition(Card):

    def draw_specifications(self):
        try:
            self.draw_specification('Level', self.info['Level'])

        except Exception:
            traceback.print_exc()

    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            return True
        return False
