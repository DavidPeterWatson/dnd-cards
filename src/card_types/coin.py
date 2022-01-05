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
