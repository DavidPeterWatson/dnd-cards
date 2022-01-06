from card import Card
import traceback
from deck import Deck


def get_class_name():
    return 'Action'

def get_card_type():
    return 'Action'

class Action(Card):

    def draw_specifications(self, position):
        try:
            for spec in self.info.get('Specifications', []):
                self.draw_specification(spec, 'x', position)

        except Exception:
            traceback.print_exc()

    def set_header(self):
        self.info['Header'] = f'{self.type} - {self.name}'