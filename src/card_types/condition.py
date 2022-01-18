from cdb.card import Card
import traceback

def get_class_name():
    return 'Condition'

def get_card_type():
    return 'Condition'

class Condition(Card):

    def draw_specifications(self, position):
        try:
            self.draw_specification('Level', self.info['Level'], position)

        except Exception:
            traceback.print_exc()

    def has_specifications(self):
        return True
