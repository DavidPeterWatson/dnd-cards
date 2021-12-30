from card import Card
import traceback
from reportlab.lib import utils
from reportlab.lib.units import mm
from deck import Deck
import os

def get_class_name():
    return 'Prop'


class Prop(Card):

    # def draw_specifications(self):
    #     try:
    #         self.draw_specification('Cost', self.info.get('Cost', ''))
    #         self.draw_specification('Weight', self.info.get('Weight', ''))
    #         self.draw_specification('Rarity', self.info.get('Rarity', ''))
    #         self.draw_specification('Hit Points', self.info.get('Hit Points', ''))
    #     except Exception:
    #         traceback.print_exc()

    def is_in_deck(deck: Deck, card_info):
        return True
