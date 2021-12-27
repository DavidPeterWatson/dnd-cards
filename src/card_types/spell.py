from card import BaseCard
import traceback
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def get_card_type():
    return 'Spell'


class Card(BaseCard):

    def draw_specifications(self):
        try:
            self.draw_specification('Level', self.definition['Level'], 0, TA_RIGHT)
            self.draw_specification('Range', self.definition['Range'], 3, TA_RIGHT)

        except Exception:
            traceback.print_exc()
