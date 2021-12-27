from card import BaseCard
import traceback
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def get_card_type():
    return 'Creature'


class Card(BaseCard):

    def draw_specifications(self):
        try:
            self.draw_specification('Level', self.definition.get('Level', ''), 0, TA_RIGHT)
            self.draw_specification('Weight', self.definition.get('Weight', ''), 1, TA_RIGHT)
            self.draw_specification('Speed', self.definition.get('Speed', ''), 2, TA_RIGHT)
            self.draw_specification('Hit Points', self.definition.get('Hit Points', ''), 3, TA_RIGHT)
            self.draw_specification('Armor Class', self.definition.get('Armor Class', ''), 4, TA_RIGHT)
            self.draw_specification('Proficiency', self.definition.get('Proficiency Bonus', ''), 5, TA_RIGHT)

            ability_modifiers = self.definition.get('Ability Modifiers', {})
            self.draw_specification('Strength', ability_modifiers.get('Strength', ''), 0, TA_LEFT)
            self.draw_specification('Dexterity', ability_modifiers.get('Dexterity', ''), 1, TA_LEFT)
            self.draw_specification('Constitution', ability_modifiers.get('Constitution', ''), 2, TA_LEFT)
            self.draw_specification('Intelligence', ability_modifiers.get('Intelligence', ''), 3, TA_LEFT)
            self.draw_specification('Wisdom', ability_modifiers.get('Wisdom', ''), 4, TA_LEFT)
            self.draw_specification('Charisma', ability_modifiers.get('Charisma', ''), 5, TA_LEFT)

 
        except Exception:
            traceback.print_exc()
