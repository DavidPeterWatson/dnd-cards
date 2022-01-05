from card_types.action import Action
import traceback


def get_class_name():
    return 'Capability'


class Capability(Action):

    def pre_draw(self):
        super().pre_draw()
        self.set_categories()
        pass

    def set_categories(self):
        self.info['Category'] = 'Skill'
        self.info['Subcategory'] = self.info.get('Ability', '')
