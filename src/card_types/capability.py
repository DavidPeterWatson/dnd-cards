from card_types.action import Action


def get_class_name():
    return 'Capability'

def get_card_type():
    return 'Capability'

class Capability(Action):

    def set_categories(self):
        self.info['Category'] = self.info.get('Subrace') + ' ' + self.info.get('Race')
        self.info['Subcategory'] = self.info.get('Class')
