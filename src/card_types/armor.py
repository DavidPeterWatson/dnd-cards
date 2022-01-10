from card_types.item import Item
import traceback

from position import Position

def get_class_name():
    return 'Armor'

def get_card_type():
    return 'Armor'

class Armor(Item):

    def draw_specifications(self, position: Position):
        try:
            super().draw_specifications(position)
            self.draw_specification('Dexterity', 'x', position)

            if self.is_proficient():
                self.draw_specification('Proficiency', 'x', position)
            self.draw_specification('Armor Class', self.info.get('Armor Class', ''), position)
            self.draw_specification('Armor Type', self.info.get('Armor Type', ''), position)
        except Exception:
            traceback.print_exc()

    def is_proficient(self):
        if self.name in self.creature_info.get('Proficiencies', {}).get('Armor', []):
             return True
        if self.info.get('Armor Type', 'Unspecified') in self.creature_info.get('Proficiencies', {}).get('Armor Type', []):
             return True
        return False

    def has_specifications(self):
        return True
