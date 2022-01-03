from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck


def get_class_name():
    return 'Action'

class Action(Card):

    def set_header(self):
        
        self.info['Header'] = f'{self.type} - {self.name}'