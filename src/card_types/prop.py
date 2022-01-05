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
            self.draw_prop_background(position)
            self.draw_back_image(position, 5*mm, 5*mm, 5*mm)
            # self.draw_border(position)
        except Exception:
            traceback.print_exc()

    def draw_prop_background(self, position: Position):
        try:
            back_filepath = os.path.join(self.style.back_path, 'Road Back.png')
            self.draw_image(back_filepath, position, self.style.card_box)
        except Exception:
            traceback.print_exc()
