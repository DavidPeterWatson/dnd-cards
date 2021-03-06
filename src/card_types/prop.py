from cdp.card import Card
import traceback
from reportlab.lib.units import mm
import os
from cdp.draw import draw_image
from cdp.position import Position

def get_class_name():
    return 'Prop'

def get_card_type():
    return 'Prop'

class Prop(Card):

    def draw_back(self, position: Position):
        try:
            self.draw_prop_background(position)
            self.draw_back_image(position, 5*mm, 5*mm, 5*mm)
        except Exception:
            traceback.print_exc()

    def draw_prop_background(self, position: Position):
        try:
            back_background_image = self.info.get('Background', 'Backgrounds/Road Back.png')
            back_filepath = os.path.join(self.style.image_path, back_background_image)
            draw_image(back_filepath, position, self.style.card_box)
        except Exception:
            traceback.print_exc()
