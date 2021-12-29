from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Creature'


class Creature(Card):

    def draw_specifications(self):
        try:
            self.draw_specification('Level', self.info.get('Level', ''), 0, TA_RIGHT)
            self.draw_specification('Weight', self.info.get('Weight', ''), 1, TA_RIGHT)
            self.draw_specification('Speed', self.info.get('Speed', ''), 2, TA_RIGHT)
            self.draw_specification('Can Carry', self.info.get('Carrying Capacity', ''), 3, TA_RIGHT)
            self.draw_specification('Hit Points', self.info.get('Hit Points', ''), 4, TA_RIGHT)
            self.draw_specification('Armor Class', self.info.get('Armor Class', ''), 5, TA_RIGHT)

            ability_modifiers = self.info.get('Ability Modifiers', {})
            self.draw_specification('Strength', ability_modifiers.get('Strength', ''), 0, TA_LEFT)
            self.draw_specification('Dexterity', ability_modifiers.get('Dexterity', ''), 1, TA_LEFT)
            self.draw_specification('Constitution', ability_modifiers.get('Constitution', ''), 2, TA_LEFT)
            self.draw_specification('Intelligence', ability_modifiers.get('Intelligence', ''), 3, TA_LEFT)
            self.draw_specification('Wisdom', ability_modifiers.get('Wisdom', ''), 4, TA_LEFT)
            self.draw_specification('Charisma', ability_modifiers.get('Charisma', ''), 5, TA_LEFT)
            self.draw_specification('Proficiency', self.info.get('Proficiency Bonus', ''), 6, TA_LEFT)
 
        except Exception:
            traceback.print_exc()

    def pre_draw(self):
        super().pre_draw()
        pass

    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Dungeon Master':
            return True
        return False

    def add_carrying_capacity(self):
        self.info['Carrying Capacity'] = str(int(self.info.get('Ability Scores', {}).get('Strength', 0)) * 15) + 'lb'

