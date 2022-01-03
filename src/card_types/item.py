from card import Card
import traceback

from position import Position


def get_class_name():
    return 'Item'


class Item(Card):

    def draw_specifications(self, position: Position):
        try:
            self.draw_specification('Cost', self.info.get('Cost', ''), position)
            self.draw_specification('Weight', self.info.get('Weight', ''), position)
            self.draw_specification('Rarity', self.info.get('Rarity', ''), position)
            self.draw_specification('Hit Points', self.info.get('Hit Points', ''), position)
        except Exception:
            traceback.print_exc()

    # def is_in_deck(deck: Deck, card_info):
    #     if deck.type == 'Character':
    #         character_info = deck.info['Cards'][deck.info['Character']]
    #         gear = character_info['Equipment']['Items']
    #         if card_info['Name'] in gear:
    #              return True

    #     return False

