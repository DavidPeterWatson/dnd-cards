from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Weapon'


class Weapon(Card):

    def pre_draw(self):
        super().pre_draw()
        self.info['Category'] = self.info.get('Skill Type', '')
        self.info['Subcategory'] = self.info.get('Attack Type')
        pass


    def draw_specifications(self):
        try:
            self.draw_specification('Cost', self.info.get('Cost', ''), 0, TA_RIGHT)
            self.draw_specification('Weight',  self.info.get('Weight', ''), 1, TA_RIGHT)
            self.draw_specification('Damage', self.info.get('Damage', ''), 2, TA_RIGHT)
            self.draw_specification('Range', self.info.get('Range', ''), 3, TA_RIGHT)

            if self.info['Attack Type'] == 'Melee':
                self.draw_specification('Strength', 'x', 0, TA_LEFT)
            if self.info['Attack Type'] == 'Ranged':
                self.draw_specification('Dexterity', 'x', 1, TA_LEFT)
            
            if self.is_proficient():
                self.draw_specification('Proficiency', 'x', 6, TA_LEFT)

        except Exception:
            traceback.print_exc()


    def is_proficient(self):
        if self.deck.type == 'Character':
            if self.name in self.deck.character_info['Proficiencies']['Weapons']:
                 return True
            if self.info.get('Skill Type', 'Unspecified') in self.deck.character_info['Proficiencies']['Weapon Skill Type']:
                 return True
        return False


    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            if card_info['Name'] in deck.character_info['Equipment']['Weapons']:
                 return True

        return False
