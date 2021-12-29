from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck
import yaml

def get_class_name():
    return 'Spell'


class Spell(Card):

    def pre_draw(self):
        super().pre_draw()
        self.info['Category'] = 'Spell'
        self.info['Subcategory'] = self.info.get('School')
        pass

    def draw_specifications(self):
        try:
            self.draw_specification('Level', self.info['Level'], 0, TA_RIGHT)
            self.draw_specification('Range', self.info['Range'], 3, TA_RIGHT)

            # self.draw_specification('Strength', ability_modifiers.get('Strength', ''), 0, TA_LEFT)
            # self.draw_specification('Dexterity', ability_modifiers.get('Dexterity', ''), 1, TA_LEFT)
            # self.draw_specification('Constitution', ability_modifiers.get('Constitution', ''), 2, TA_LEFT)
            # self.draw_specification('Intelligence', ability_modifiers.get('Intelligence', ''), 3, TA_LEFT)
            # self.draw_specification('Wisdom', ability_modifiers.get('Wisdom', ''), 4, TA_LEFT)
            # self.draw_specification('Charisma', ability_modifiers.get('Charisma', ''), 5, TA_LEFT)

        except Exception:
            traceback.print_exc()

    def is_in_deck(deck: Deck, card_info):
        if deck.info['Type'] == 'Character':
            character_info = deck.info['Cards'][deck.info['Character']]
            if card_info['Name'] in character_info.get('Prepared Spells', []):
                 return True
            merged = list(set(card_info.get('Capabilities', [])) & set(character_info.get('Capabilities', [])))
            if len(merged) > 0:
                return True
        return False
