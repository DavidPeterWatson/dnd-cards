from card import Card
import traceback
from reportlab.lib import utils
from reportlab.lib.units import mm
import os

from position import Position

def get_class_name():
    return 'Prop'


class Prop(Card):

    def draw_back(self, position: Position):
        try:
            self.draw_background()
            self.draw_back_image(position, 5*mm, 5*mm, 5*mm)
            self.draw_border()
        except Exception:
            traceback.print_exc()
