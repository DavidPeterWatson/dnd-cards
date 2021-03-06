from cdp.card import Card
import traceback

def get_class_name():
    return 'Spell'

def get_card_type():
    return 'Spell'

class Spell(Card):

    def pre_draw(self):
        super().pre_draw()
        self.info['Category'] = 'Spell'
        self.info['Subcategory'] = self.info.get('School')
        pass

    def draw_specifications(self, position):
        try:
            self.draw_specification('Level', self.info['Level'], position)
            self.draw_specification('Range', self.info['Range'], position)
            self.draw_specification('Casting Time', self.info['Casting Time'], position)
            self.draw_specification('Duration', self.info['Duration'], position)
        except Exception:
            traceback.print_exc()

    def has_specifications(self):
        return True
