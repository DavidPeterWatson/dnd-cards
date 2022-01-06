import os
import logging
import importlib
from card import Card

logging.getLogger().setLevel(logging.INFO)

CARD_TYPES_FOLDER = 'card_types'

class CardTypeProvider:

    def __init__(self):
        self.card_types = self.load_card_types()


    def get_card_type(self, card_type: str):
        return self.card_types.get(card_type, Card)


    def load_card_types(self):
        card_types = {}
        for filename in filter(lambda x: x.endswith('.py') and x != '__init__.py', os.listdir(CARD_TYPES_FOLDER)):
            try:
                card_type, card_class = self.load_card_type('{}.{}'.format(CARD_TYPES_FOLDER, filename[:-3]))
                card_types[card_type] = card_class
            except Exception as e:
                logging.error(e, exc_info=True)
        return card_types


    def load_card_type(self, filename):
        module = importlib.import_module(filename)
        class_name = module.get_class_name()
        card_type = module.get_card_type()
        return card_type, getattr(module, class_name)
