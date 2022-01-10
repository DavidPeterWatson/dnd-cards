from card import Card
import traceback
from deck import Deck
import yaml

def get_class_name():
    return 'SpellSlot'

def get_card_type():
    return 'Spell Slot'

class SpellSlot(Card):

    def draw_specifications(self, position):
        try:
            self.draw_specification('Level', self.info['Level'], position)
        except Exception:
            traceback.print_exc()

    def has_specifications(self):
        return True
