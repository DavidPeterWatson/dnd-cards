from card import Card
import traceback
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from deck import Deck

damage_type_string = {
    'acid': 'acid',
    'bludgeoning': 'bludgeon',
    'cold': 'cold',
    'fire': 'fire',
    'force': 'force',
    'lightning': 'lightning',
    'necrotic': 'necrotic',
    'piercing': 'pierce',
    'poison': 'poison',
    'psychic': 'psychic',
    'radiant': 'radiant',
    'slashing': 'slash',
    'thunder': 'thunder',
}

def get_class_name():
    return 'Weapon'


class Weapon(Card):

    def pre_draw(self):
        super().pre_draw()
        self.info['Category'] = self.info.get('Skill Type', '')
        self.info['Subcategory'] = self.info.get('Attack Type')
        pass


    def draw_specifications(self, position):
        try:
            self.draw_specification('Cost', self.info.get('Cost', ''), position)
            self.draw_specification('Weight', self.info.get('Weight', ''), position)
            self.draw_specification('Damage', self.info.get('Damage', ''), position)
            self.draw_specification('Damage Type', damage_type_string[self.info.get('Damage Type', '')], position)
            self.draw_specification('Range', self.info.get('Range', ''), position)
            self.draw_specification('Reach', self.info.get('Reach', ''), position)

            if self.info['Attack Type'] == 'Melee':
                self.draw_specification('Strength', 'x', position)
            if self.info['Attack Type'] == 'Ranged':
                self.draw_specification('Dexterity', 'x', position)
            
            if self.is_proficient():
                self.draw_specification('Proficiency', 'x', position)

        except Exception:
            traceback.print_exc()


    def is_proficient(self):
        if self.deck.type == 'Character':
            if self.name in self.deck.character_info['Proficiencies'].get('Weapons', []):
                 return True
            if self.info.get('Skill Type', 'Unspecified') in self.deck.character_info['Proficiencies'].get('Weapon Skill Type', []):
                 return True
        return False


    def is_in_deck(deck: Deck, card_info):
        if deck.type == 'Character':
            if card_info['Name'] in deck.character_info['Equipment'].get('Weapons', []):
                 return True

        return False
