from cdb.card import Card
import traceback

def get_class_name():
    return 'Basic'

def get_card_type():
    return 'Basic'

class Basic(Card):

    def has_specifications(self):
        return super().has_specifications()
