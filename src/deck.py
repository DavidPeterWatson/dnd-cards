import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm

class Deck():
    def __init__(self, deck_definition):
        self.definition = deck_definition
        self.canvas = Canvas(self.definition['Name'] + '.pdf')
        self.style = self.definition['Deck Styles'][self.definition['Style']]
        self.root_folder = self.definition['Root Folder']
        self.style_folder = self.style['Style Folder']
        self.style_path: str = os.path.join(self.root_folder, self.style_folder)
        self.page = self.style['Page']
        self.page_size = self.definition['Page Sizes'][self.page['Size']]
        self.page_height = self.page_size['Height'] * mm
        self.page_width = self.page_size['Width'] * mm
        self.page_left_margin = self.page['Left Margin'] * mm
        self.page_bottom_margin = self.page['Bottom Margin'] * mm
        self.columns = self.style['Columns']
        self.rows = self.style['Columns']
        self.card_size = self.definition['Card Sizes'][self.style['Card Size']]
        self.card_width = self.card_size['Width'] * mm
        self.card_height = self.card_size['Height'] * mm
        self.image = self.style['Image']
        self.image_folder = self.image['Folder']
        self.image_path = os.path.join(self.root_folder, self.image_folder)