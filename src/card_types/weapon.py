from card import Card
import traceback

def get_class_name():
    return 'Weapon'

def get_card_type():
    return 'Weapon'

class Weapon(Card):

    def pre_draw(self):
        super().pre_draw()
        self.info['Category'] = self.info.get('Skill Type', '') + ' ' + self.info.get('Attack Type')
        pass


    def draw_specifications(self, position):
        try:
            self.draw_specification('Cost', self.info.get('Cost', ''), position)
            self.draw_specification('Weight', self.info.get('Weight', ''), position)
            self.draw_specification('Damage', self.info.get('Damage', ''), position)
            self.draw_specification('Damage Type', self.info.get('Damage Type', ''), position)
            self.draw_specification('Range', self.info.get('Range', ''), position)
            self.draw_specification('Reach', self.info.get('Reach', ''), position)

            self.draw_specification(self.get_ability_modifier(), 'x', position)
            
            if self.is_proficient():
                self.draw_specification('Proficiency', 'x', position)

        except Exception:
            traceback.print_exc()

    def get_instructions(self):
        ability_modifier = self.get_ability_modifier()
        instructions = f'Attack Roll: 1d20 + {ability_modifier}'
        if self.is_proficient():
            instructions = f'{instructions} + Proficiency'
        damage = self.info.get('Damage', '')
        instructions = f'{instructions}\nDamage Roll: {damage} + {ability_modifier}'
        return instructions

    def is_proficient(self):
        if self.name in self.creature_info.get('Proficiencies', {}).get('Weapons', []):
             return True
        if self.info.get('Skill Type', 'Unspecified') in self.creature_info.get('Proficiencies', {}).get('Weapon Skill Types', []):
             return True
        return False

    def get_ability_modifier(self):
        if self.info['Attack Type'] == 'Melee':
            if 'Finesse' in self.info.get('Properties', []):
                ability_scores = self.creature_info.get('Ability Scores', {})
                if ability_scores.get('Dexterity') > ability_scores.get('Strength'):
                    return 'Dexterity'
            return 'Strength'
        if self.info['Attack Type'] == 'Ranged':
            return 'Dexterity'
