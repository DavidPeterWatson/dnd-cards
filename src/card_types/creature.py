from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Creature'


class Creature(Card):

    def draw_specifications(self):
        try:
            self.draw_specification('Level', self.info.get('Level', ''))
            self.draw_specification('Weight', self.info.get('Weight', ''))
            self.draw_specification('Speed', self.info.get('Speed', ''))
            self.draw_specification('Can Carry', self.info.get('Carrying Capacity', ''))
            self.draw_specification('Hit Points', self.info.get('Hit Points', ''))
            self.draw_specification('Armor Class', self.info.get('Armor Class', ''))

            ability_modifiers = self.info.get('Ability Modifiers', {})
            self.draw_specification('Strength', ability_modifiers.get('Strength', ''))
            self.draw_specification('Dexterity', ability_modifiers.get('Dexterity', ''))
            self.draw_specification('Constitution', ability_modifiers.get('Constitution', ''))
            self.draw_specification('Intelligence', ability_modifiers.get('Intelligence', ''))
            self.draw_specification('Wisdom', ability_modifiers.get('Wisdom', ''))
            self.draw_specification('Charisma', ability_modifiers.get('Charisma', ''))
            self.draw_specification('Proficiency', self.info.get('Proficiency Bonus', ''))
 
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

