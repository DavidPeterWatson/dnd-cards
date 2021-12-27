from card import BaseCard
import traceback
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def get_card_type():
    return 'Weapon'


class Card(BaseCard):

    def draw_specifications(self):
        try:
            self.draw_specification('Cost', self.definition['Cost'], 0, TA_RIGHT)
            self.draw_specification('Weight',  self.definition['Weight'], 1, TA_RIGHT)
            self.draw_specification('Damage', self.definition['Damage'], 2, TA_RIGHT)
            self.draw_specification('Range', self.definition.get('Range', ''), 3, TA_RIGHT)
        except Exception:
            traceback.print_exc()
