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
        self.set_details()
        pass


    def set_carrying_capacity(self):
        self.info['Carrying Capacity'] = str(int(self.info.get('Ability Scores', {}).get('Strength', 0)) * 15) + 'lb'


    def set_categories(self):
        self.info['Category'] = self.info.get('Subrace') + ' ' + self.info.get('Race')
        self.info['Subcategory'] = self.info.get('Class')


    def set_details(self):
        info_labels = [
            'Level',
            'Race',
            'Class',
            'Subclass',
            'Background',
            'Gender',
            'Alignment',
            'Background Story'
            'Bonds',
            'Traits',
            'Ideals',
            'Flaws',
            'Personal Goal'
        ]
        details = ''
        for info_label in info_labels:
            details = details + self.get_info_with_label(info_label)
        self.info['Details'] = details

    def get_info_with_label(self, info_name):
        info_value = self.info.get(info_name, '')
        if info_value != '':
            return f'{info_name}: {info_value}\n'
        return ''
