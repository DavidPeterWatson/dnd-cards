import os
import yaml
from reportlab.pdfgen.canvas import Canvas
from cdb.library import Library
from cdb.style import Style


class Deck():
    def __init__(self, name, deck_info, library: Library):
        self.name = name
        self.info = deck_info
        self.label = self.info.get('Label', name)
        self.library = library
        self.collate = self.info.get('Collate', True)
        style_name = self.info.get('Style')
        self.style = Style(style_name, library)
        filepath =  os.path.join(self.style.output_folder, self.name + '.pdf')
        self.canvas = Canvas(filepath)
        self.type = self.info.get('Type', '')
        self.cards = []
        self.box = None
        self.min_cards = self.info.get('Minimum Cards', 10)

