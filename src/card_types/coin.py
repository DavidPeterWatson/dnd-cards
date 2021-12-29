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
