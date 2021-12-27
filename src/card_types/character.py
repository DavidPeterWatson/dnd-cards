from card import BaseCard
import traceback
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


def get_card_type():
    return 'Character'


class Card(BaseCard):

    def draw_specifications(self):
        try:
            self.draw_specification('Level', self.definition['Level'], 0, TA_RIGHT)
            self.draw_specification('Weight', self.definition['Weight'], 1, TA_RIGHT)
            self.draw_specification('Speed', self.definition['Speed'], 2, TA_RIGHT)
            self.draw_specification('Hit Points', self.definition['Hit Points'], 3, TA_RIGHT)
            self.draw_specification('Armor Class', self.definition['Armor Class'], 4, TA_RIGHT)
            self.draw_specification('Proficiency', self.definition['Proficiency Bonus'], 5, TA_RIGHT)

            ability_modifiers = self.definition['Ability Modifiers']
            self.draw_specification('Strength', ability_modifiers['Strength'], 0, TA_LEFT)
            self.draw_specification('Dexterity', ability_modifiers['Dexterity'], 1, TA_LEFT)
            self.draw_specification('Constitution', ability_modifiers['Constitution'], 2, TA_LEFT)
            self.draw_specification('Intelligence', ability_modifiers['Intelligence'], 3, TA_LEFT)
            self.draw_specification('Wisdom', ability_modifiers['Wisdom'], 4, TA_LEFT)
            self.draw_specification('Charisma', ability_modifiers['Charisma'], 5, TA_LEFT)

 
        except Exception:
            traceback.print_exc()
