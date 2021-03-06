from card_types.skill import Skill

def get_class_name():
    return 'PassiveSkill'

def get_card_type():
    return 'Passive Skill'

class PassiveSkill(Skill):

    def get_instructions(self):
        ability = self.info['Ability']
        instructions = f'Check = 10 + {ability}'
        if self.is_proficient():
            # proficiency_bonus = self.creature_info.get('Proficiency Bonus', '')
            instructions = f'{instructions} + Proficiency'
        return instructions

    def is_proficient(self):
        if self.info['Skill'] in self.creature_info.get('Proficiencies', {}).get('Skills', []):
             return True

    def has_specifications(self):
        return True
