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

    def draw_specifications(self, position):
        try:
            self.draw_specification(self.info['Ability'], 'x', position)

            if self.is_proficient():
                self.draw_specification('Proficiency', 'x', position)
            return
        except Exception:
            traceback.print_exc()

    def set_categories(self):
        self.info['Category'] = 'Skill'
        self.info['Subcategory'] = self.info.get('Ability', '')

    def is_proficient(self):
        if self.name in self.character_info['Proficiencies']['Skills']:
             return True
