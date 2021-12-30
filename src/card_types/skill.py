from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Skill'


class Skill(Card):

    def pre_draw(self):
        super().pre_draw()
        self.set_categories()
        pass

    def draw_specifications(self):
        try:
            self.draw_specification(self.info['Ability'], 'x')

            if self.is_proficient():
                self.draw_specification('Proficiency', 'x')
            return
        except Exception:
            traceback.print_exc()

    def set_categories(self):
        self.info['Category'] = 'Skill'
        self.info['Subcategory'] = self.info.get('Ability', '')

    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            return True
        return False

    def is_proficient(self):
        if self.deck.type == 'Character':
            if self.name in self.deck.character_info['Proficiencies']['Skills']:
                 return True
        return False
