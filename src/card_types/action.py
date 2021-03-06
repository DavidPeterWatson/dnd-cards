from cdp.card import Card
import traceback

def get_class_name():
    return 'Action'

def get_card_type():
    return 'Action'

class Action(Card):

    def draw_specifications(self, position):
        try:
            for spec in self.info.get('Specifications', []):
                self.draw_specification(spec, 'x', position)

        except Exception:
            traceback.print_exc()

    def has_specifications(self):
        return True
