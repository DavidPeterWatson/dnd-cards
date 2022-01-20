from cdb.card import Card
import traceback
from reportlab.lib.units import mm
from cdb.position import Position

def get_class_name():
    return 'Creature'

def get_card_type():
    return 'Creature'

class Creature(Card):

    def draw_specifications(self, position: Position):
        try:
            self.draw_specification('Level', self.info.get('Level', ''), position)
            self.draw_specification('Speed', self.info.get('Speed', ''), position)
            self.draw_specification('Hit Points', self.info.get('Hit Points', ''), position)
            self.draw_specification('Hit Dice', self.info.get('Hit Dice', ''), position)
            self.draw_specification('Armor Class', self.info.get('Armor Class', ''), position)
            self.draw_specification('Initiative', self.info.get('Initiative', ''), position)
            self.draw_specification('Perception', self.info.get('Passive Perception', ''), position)

            ability_modifiers = self.info.get('Ability Modifiers', {})
            self.draw_specification('Strength', ability_modifiers.get('Strength', ''), position)
            self.draw_specification('Dexterity', ability_modifiers.get('Dexterity', ''), position)
            self.draw_specification('Constitution', ability_modifiers.get('Constitution', ''), position)
            self.draw_specification('Intelligence', ability_modifiers.get('Intelligence', ''), position)
            self.draw_specification('Wisdom', ability_modifiers.get('Wisdom', ''), position)
            self.draw_specification('Charisma', ability_modifiers.get('Charisma', ''), position)
            self.draw_specification('Proficiency', self.info.get('Proficiency Bonus', ''), position)
 
        except Exception:
            traceback.print_exc()

    def pre_draw(self):
        super().pre_draw()
        self.set_passive_perception()
        self.set_initiative()
        self.info['Back Image'] = self.info['Image']
        pass

    def draw_back_image(self, position, top_padding, bottom_padding, side_padding):
        super().draw_back_image(position, self.style.header_height, 10*mm, 5*mm)

    def set_passive_perception(self):
        if not 'Passive Perception' in self.info:
            ability_modifiers = self.info.get('Ability Modifiers', {})
            wisdom = ability_modifiers.get('Wisdom', '0')
            proficiency_bonus = ability_modifiers.get('Proficiency Bonus', '0')
            self.info['Passive Perception'] = int(10) + int(wisdom) + int(proficiency_bonus)

    def set_initiative(self):
        if not 'Initiative' in self.info:
            ability_modifiers = self.info.get('Ability Modifiers', {})
            dexterity = ability_modifiers.get('Dexterity', '0')
            self.info['Initiative'] = int(10) + int(dexterity)

    def has_specifications(self):
        return True
