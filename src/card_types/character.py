from card_types.creature import Creature
import traceback
import yaml

def get_class_name():
    return 'Character'

class Character(Creature):

    def pre_draw(self):
        super().pre_draw()
        self.set_carrying_capacity()
        self.set_categories()
        pass


    def set_carrying_capacity(self):
        self.info['Carrying Capacity'] = str(int(self.info.get('Ability Scores', {}).get('Strength', 0)) * 15) + 'lb'


    def set_categories(self):
        self.info['Category'] = self.info.get('Subrace') + ' ' + self.info.get('Race')
        self.info['Subcategory'] = self.info.get('Class')

