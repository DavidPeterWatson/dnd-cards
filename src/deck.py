import os
import yaml
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

class Deck():
    def __init__(self, deck_info):
        self.info = deck_info
        self.canvas = Canvas(self.info['Name'] + '.pdf')
        self.style = self.info['Deck Styles'][self.info['Style']]
        self.root_folder = self.info['Root Folder']
        self.style_folder = self.style['Style Folder']
        self.style_path: str = os.path.join(self.root_folder, self.style_folder)
        self.page = self.style['Page']
        self.page_size = self.info['Page Sizes'][self.page['Size']]
        self.page_height = self.page_size['Height'] * mm
        self.page_width = self.page_size['Width'] * mm
        self.page_left_margin = self.page['Left Margin'] * mm
        self.page_bottom_margin = self.page['Bottom Margin'] * mm
        self.columns = self.style['Columns']
        self.rows = self.style['Columns']
        self.card_size = self.info['Card Sizes'][self.style['Card Size']]
        self.card_width = self.card_size['Width'] * mm
        self.card_height = self.card_size['Height'] * mm
        self.image = self.style['Image']
        self.image_folder = self.image['Folder']
        self.image_path = os.path.join(self.root_folder, self.image_folder)

        self.back = self.style['Back']
        self.back_folder = self.back['Folder']
        self.back_path: str = os.path.join(self.root_folder, self.back_folder)

        self.type = self.info.get('Type', '')
        self.cards = self.info['Cards']
        self.packs = self.info.get('Packs', {})
        self.coinage = self.info.get('Coinage', {})

        self.character_info = self.cards.get(self.info.get('Character', ''), {})
        self.build()
        self.specifications = self.style['Specifications']['Named']

    def build(self):
        if self.type == 'Character':
            for pack in self.character_info['Equipment'].get('Packs', []):
                print(pack)
                pack_info = self.packs.get(pack, {})
                for gear in pack_info.get('Gear', []):
                    if gear in self.cards:
                        self.character_info['Equipment']['Gear'].append(gear)

            for coinage in self.character_info['Equipment'].get('Coinage', []):
                coin_type = coinage['Coin Type']
                for quantity in range(1, int(coinage['Quantity']) + 1):
                    coinage_name = f'{quantity} of {coin_type}'
                    coinage_info = self.cards.get(coinage['Coin Type'], {})
                    self.cards[coinage_name] = coinage_info
                    self.character_info['Equipment']['Gear'].append(coinage_name)
