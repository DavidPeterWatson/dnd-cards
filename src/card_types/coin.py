from card_types.item import Item
import traceback
from deck import Deck


def get_class_name():
    return 'Coin'

def get_card_type():
    return 'Coin'

class Coin(Item):

    def draw_specifications(self, position):
        try:
            pass
        except Exception:
            traceback.print_exc()
