from card_types.item import Item
import traceback
from deck import Deck


def get_class_name():
    return 'Coin'


class Coin(Item):

    def draw_specifications(self, position):
        try:
            pass
        except Exception:
            traceback.print_exc()

    # def is_in_deck(deck: Deck, card_info):
    #     if deck.type == 'Character':
    #         character_info = deck.info['Cards'][deck.info['Character']]
    #         gear = character_info['Equipment']['Gear']
    #         if card_info['Name'] in gear:
    #              return True

    #     return False