from card import Card
import traceback


def get_class_name():
    return 'Skill'

def get_card_type():
    return 'Skill'

class Skill(Card):

    def pre_draw(self):
        super().pre_draw()
        self.ability = self.info['Ability']
        self.description = self.info['Description']
        self.set_categories()
        pass

    def draw_specifications(self, position):
        try:
            self.draw_specification(self.info['Ability'], 'x', position)

            if self.is_proficient():
                self.draw_specification('Proficiency', 'x', position)
            return
        except Exception:
            traceback.print_exc()

    def set_categories(self):
        self.info['Category'] = 'Skill'
        self.info['Subcategory'] = self.info.get('Ability', '')

    def get_instructions(self):
        ability = self.info['Ability']
        instructions = f'Check: 1d20 + {ability}'
        if self.is_proficient():
            proficiency_bonus = self.info.get('Proficiency Bonus', '')
            instructions = f'{instructions} + {proficiency_bonus}'
        return instructions

    def is_proficient(self):
        if self.name in self.creature_info.get('Proficiencies', {}).get('Skills', []) and self.info.get('Proficiency Bonus', '') != '':
             return True

    def has_specifications(self):
        return True
