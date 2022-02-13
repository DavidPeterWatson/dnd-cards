from card_types.action import Card

def get_class_name():
    return 'Narrative'

def get_card_type():
    return 'Narrative'

class Narrative(Card):

    def set_categories(self):
        self.info['Category'] = 'Narrative ' + str(self.info.get('Number', ''))