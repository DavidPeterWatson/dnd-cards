from card_types.gear import Gear
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Coin'


class Coin(Gear):

    def draw_specifications(self):
        try:
            pass
        except Exception:
            traceback.print_exc()

    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            character_info = deck.info['Cards'][deck.info['Character']]
            gear = character_info['Equipment']['Gear']
            if card_info['Name'] in gear:
                 return True

        return False