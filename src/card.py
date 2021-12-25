# from borb.pdf.document import Document
# from borb.pdf.page.page import Page
# from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
# from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
# from borb.pdf.canvas.layout.text.paragraph import Paragraph
# from borb.pdf.canvas.layout.image.image import Image
# from borb.pdf.canvas.layout.layout_element import Alignment
import traceback
import os
import yaml
from decimal import Decimal
from reportlab.lib import utils
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from deck import Deck

class Card:
    def __init__(self, deck: Deck, card_definition, canvas, column, row):
        self.deck = deck
        # self.style = deck['Deck Styles'][deck['Style']]
        self.card_definition = card_definition
        self.canvas = canvas
        self.row = row
        page_row = abs(self.row - deck.rows + 1)
        self.column = column
        
        self.card_size = deck.card_size
        self.width = self.card_size['Width'] * mm
        self.height = self.card_size['Height'] * mm

        # self.root_folder = deck['Root Folder']
        # self.style_folder = self.style['Style Folder']
        # self.style_path: str = os.path.join(self.root_folder, self.style_folder)
        # image = self.style['Image']
        # self.image_folder = image['Folder']
        # self.image_path = os.path.join(deck.root_folder, deck.image_folder)

        # self.page_left_margin = self.page['Left Margin'] * mm
        # self.page_bottom_margin = self.page['Bottom Margin'] * mm
        self.x_offset = self.column * self.width + deck.page_left_margin
        self.y_offset =  page_row * self.height + deck.page_bottom_margin


def print_card(deck, card_definition, canvas, column, row):
    try:
        card_header = card_definition['Header']
        print(f'printing card {card_header}')
        card = Card(deck, card_definition, canvas, column, row)
        draw_background(card)
        draw_artwork(card)
        draw_detail(card)
        draw_category(card)
        draw_border(card)
        draw_header(card)
    except Exception:
        traceback.print_exc()

def draw_background(card: Card):
    try:
        background_filename =  card.deck.style['Background']
        background_filepath = os.path.join(card.deck.style_path, background_filename)
        card.canvas.drawImage(background_filepath, card.x_offset, card.y_offset, card.width, card.height, mask='auto')
    except Exception:
        traceback.print_exc()

def draw_artwork(card: Card):
    try:
        image = card.deck.style['Image']
        image_filename = card.card_definition['Image']
        image_height =  image['Height'] * mm
        image_top =  image['Top'] * mm
        image_filepath = os.path.join(card.deck.image_path, image_filename)
        img = utils.ImageReader(image_filepath)
        iw, ih = utils.ImageReader(image_filepath).getSize()
        image_aspect_ratio = ih / float(iw)
        image_width = image_height / image_aspect_ratio
        draw_image(card, image_filepath, (card.width - image_width) / 2, card.height - image_top - image_height, image_width, image_height)
    except Exception:
        traceback.print_exc()

def draw_detail(card: Card):
    try:
        detail = card.deck.style['Detail']
        detail_filename =  detail['Image']
        detail_height =  detail['Height'] * mm
        detail_font =  detail['Font']
        detail_font_size =  detail['Font Size']
        detail_top_offset =  detail['Top Offset'] * mm
        detail_left_offset =  detail['Left Offset'] * mm
        detail_text = card.card_definition['Detail']
        detail_filepath = os.path.join(card.deck.style_path, detail_filename)
        card.canvas.drawImage(detail_filepath, card.x_offset, card.y_offset, card.width, detail_height, mask='auto')
        # card.canvas.setFont(detail_font, detail_font_size)
        # card.canvas.drawString(card.x_offset + detail_left_offset, card.y_offset + detail_height - detail_top_offset, detail_text)
        x = card.x_offset + detail_left_offset 
        y = card.y_offset + detail_height - detail_top_offset
        draw_paragraph(card.canvas, detail_text, x, y, card.width - detail_left_offset * 2, detail_height, detail_font, detail_font_size)
    except Exception:
        traceback.print_exc()

def draw_category(card: Card):
    try:
        detail = card.deck.style['Detail']
        detail_height =  detail['Height'] * mm
        category = card.deck.style['Category']
        category_font =  category['Font']
        category_font_size =  category['Font Size']
        category_top_offset =  category['Top Offset'] * mm
        category_text = card.card_definition['Category'] + ' - ' + card.card_definition['Subcategory']
        card.canvas.setFont(category_font, category_font_size)
        # canvas.drawCentredString((column + 0.5) * card_width * mm, (pdf_row * card_height + detail_height - category_top_offset ) * mm, category_text)
        draw_centred_string(card, category_text, card.width / 2,  detail_height - category_top_offset)
    except Exception:
        traceback.print_exc()

def draw_border(card: Card):
    try:
        border = card.deck.style['Border']
        border_filename =  border['Image']
        border_filepath = os.path.join(card.deck.style_path, border_filename)
        # canvas.drawImage(border_filepath, column * card_width * mm, pdf_row * card_height * mm, card_width * mm, card_height * mm, mask='auto')
        draw_image(card, border_filepath, 0, 0, card.width, card.height)
    except Exception:
        traceback.print_exc()

def draw_header(card: Card):
    try:
        header = card.deck.style['Header']
        header_filename =  header['Image']
        header_height =  header['Height'] * mm
        text_top = header['TextTop'] * mm
        header_font = header['Font'] 
        header_font_size = header['Font Size']
        header_filepath = os.path.join(card.deck.style_path, header_filename)
        # canvas.drawImage(header_filepath, column * card_width * mm, (pdf_row * card_height + card_height - header_height) * mm, card_width * mm, header_height * mm, mask='auto')
        draw_image(card, header_filepath, 0, card.height - header_height, card.width, header_height)
        card.canvas.setFont(header_font, header_font_size)
        draw_centred_string(card, card.card_definition['Header'], card.width / 2, card.height - text_top)
        # card.canvas.drawCentredString((column + 0.5) * card_width * mm, (pdf_row * card_height + card_height - text_top) * mm, card['Header'])
    except Exception:
        traceback.print_exc()

def draw_image(card: Card, image_filepath, x_offset, y_offset, width, height):
    card.canvas.drawImage(image_filepath, card.x_offset + x_offset, card.y_offset + y_offset, width, height, mask='auto')

def draw_centred_string(card: Card, text: str, x_offset, y_offset):
    card.canvas.drawCentredString(card.x_offset + x_offset, card.y_offset + y_offset, text)
    # style = ParagraphStyle(
    #     name='Normal',
    #     fontName=fontName,
    #     fontSize=fontSize,
    #     alignment=TA_CENTER,
    #     spaceAfter=1 * mm
    # )
    # message_style = ParagraphStyle('Normal', alignment=TA_CENTER)
    # message = text.replace('\n', '<br />')
    # message = Paragraph(message, style=message_style)
    # w, h = message.wrap(width, height)
    # message.drawOn(card.canvas, card.x_offset + x_offset, card.y_offset + y_offset - height)

def draw_paragraph(canvas, msg, x, y, max_width, max_height, fontName, fontSize):
    style = ParagraphStyle(
        name='Normal',
        fontName=fontName,
        fontSize=fontSize,
        # alignment=alignment,
        leading=fontSize+2
    )
    message = msg.replace('\n', '<br />')
    message = Paragraph(message, style=style)
    w, h = message.wrap(max_width, max_height)
    message.drawOn(canvas, x, y - h)