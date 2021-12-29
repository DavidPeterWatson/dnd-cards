from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Gear'


class Gear(Card):

    def draw_specifications(self):
        try:
            self.draw_specification('Cost', self.info.get('Cost', ''), 0, TA_RIGHT)
            self.draw_specification('Weight', self.info.get('Weight', ''), 1, TA_RIGHT)
            self.draw_specification('Rarity', self.info.get('Rarity', ''), 2, TA_RIGHT)
            self.draw_specification('Hit Points', self.info.get('Hit Points', ''), 3, TA_RIGHT)
        except Exception:
            traceback.print_exc()

    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            character_info = deck.info['Cards'][deck.info['Character']]
            gear = character_info['Equipment']['Gear']
            if card_info['Name'] in gear:
                 return True

        return False

