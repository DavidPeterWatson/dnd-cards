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
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from deck import Deck
import importlib
import logging

TOP = 'top'
BOTTOM = 'bottom'
MIDDLE = 'middle'

class BaseCard:
    def __init__(self, deck: Deck, definition, canvas, column, row):
        self.deck = deck
        self.definition = definition
        self.canvas = canvas
        self.row = row
        page_row = abs(self.row - deck.rows + 1)
        self.column = column
        
        self.card_size = deck.card_size
        self.width = self.card_size['Width'] * mm
        self.height = self.card_size['Height'] * mm

        self.x_offset = self.column * self.width + deck.page_left_margin
        self.y_offset =  page_row * self.height + deck.page_bottom_margin
        self.x_back_offset = abs(self.column - 2) * self.width + deck.page_left_margin


    def draw(self):
        try:
            self.draw_background()
            self.draw_artwork()
            self.draw_detail()
            self.draw_specifications()
            self.draw_category()
            self.draw_border()
            self.draw_header()
        except Exception:
            traceback.print_exc()


    def draw_background(self):
        try:
            background_filename =  self.deck.style['Background']
            background_filepath = os.path.join(self.deck.style_path, background_filename)
            self.canvas.drawImage(background_filepath, self.x_offset, self.y_offset, self.width, self.height, mask='auto')
        except Exception:
            traceback.print_exc()


    def draw_back(self):
        try:
            back = self.deck.definition['Back']
            back_image =  back['Image']
            back_image_filepath = os.path.join(self.deck.back_path, back_image)
            self.canvas.drawImage(back_image_filepath, self.x_back_offset, self.y_offset, self.width, self.height, mask='auto')
        except Exception:
            traceback.print_exc()


    def draw_specifications(self):
        pass


    def draw_artwork(self):
        try:
            image = self.deck.style['Image']
            image_height =  image['Height'] * mm
            image_top =  image['Top'] * mm
            image_filename = self.definition['Image']
            image_filepath = os.path.join(self.deck.image_path, image_filename)
            iw, ih = utils.ImageReader(image_filepath).getSize()
            image_aspect_ratio = ih / float(iw)
            image_width = image_height / image_aspect_ratio
            self.draw_image(image_filepath, (self.width - image_width) / 2, self.height - image_top - image_height, image_width, image_height)
        except Exception:
            traceback.print_exc()


    def draw_specification(self, label, value, row, alignment = TA_LEFT):
        try:
            if value == '':
                return
            image = self.deck.style['Image']
            image_top =  image['Top'] * mm
            specs = self.deck.style['Specifications']
            spec_label_font =  specs['Label Font']
            spec_label_font_size =  specs['Label Font Size']
            spec_value_font =  specs['Value Font']
            spec_value_font_size =  specs['Value Font Size']
            spec_offset =  specs['Offset'] * mm
            spec_height =  specs['Height'] * mm
            spec_width =  specs['Width'] * mm
            spec_spacing =  specs['Spacing'] * mm
            y_offset = self.height - image_top - row * (spec_height + spec_spacing)
            if alignment == TA_LEFT:
                x_offset = spec_offset
            if alignment == TA_RIGHT:
                x_offset = self.width - spec_offset - spec_width
            self.draw_paragraph(label, self.x_offset + x_offset, self.y_offset + y_offset, spec_width, spec_height, spec_label_font, spec_label_font_size, TA_CENTER, TOP)
            self.draw_paragraph(value, self.x_offset + x_offset, self.y_offset + y_offset, spec_width, spec_height, spec_value_font, spec_value_font_size, TA_CENTER, MIDDLE)

        except Exception:
            traceback.print_exc()


    def draw_category(self):
        try:
            detail = self.deck.style['Detail']
            detail_height =  detail['Height'] * mm
            category = self.deck.style['Category']
            category_font =  category['Font']
            category_font_size =  category['Font Size']
            category_height =  category['Height'] * mm
            category_top_text_offset = category['Top Text Offset'] * mm
            category_text = self.definition['Category'] + ' - ' + self.definition['Subcategory']
            self.draw_paragraph(category_text, self.x_offset, self.y_offset + detail_height + category_height - category_top_text_offset, self.width, category_height - category_top_text_offset, category_font, category_font_size, TA_CENTER, MIDDLE)
            # self.draw_centred_string(category_text, self.width / 2,  detail_height, category_font, category_font_size)
        except Exception:
            traceback.print_exc()


    def draw_detail(self):
        try:
            category = self.deck.style['Category']
            category_height =  category['Height'] * mm

            detail = self.deck.style['Detail']
            detail_filename =  detail['Image']
            detail_height =  detail['Height'] * mm
            detail_font =  detail['Font']
            detail_font_size =  detail['Font Size']
            detail_left_offset =  detail['Left Offset'] * mm
            detail_text = self.definition['Detail']
            detail_filepath = os.path.join(self.deck.style_path, detail_filename)
            self.canvas.drawImage(detail_filepath, self.x_offset, self.y_offset, self.width, detail_height + category_height, mask='auto')
            x = self.x_offset + detail_left_offset 
            y = self.y_offset + detail_height
            self.draw_paragraph(detail_text, x, y, self.width - detail_left_offset * 2, detail_height, detail_font, detail_font_size, TA_LEFT)
        except Exception:
            traceback.print_exc()


    def draw_border(self):
        try:
            border = self.deck.style['Border']
            border_filename =  border['Image']
            border_filepath = os.path.join(self.deck.style_path, border_filename)
            self.draw_image(border_filepath, 0, 0, self.width, self.height)
        except Exception:
            traceback.print_exc()


    def draw_header(self):
        try:
            header = self.deck.style['Header']
            header_filename =  header['Image']
            header_height =  header['Height'] * mm
            text_top = header['TextTop'] * mm
            header_font = header['Font'] 
            header_font_size = header['Font Size']
            header_filepath = os.path.join(self.deck.style_path, header_filename)
            header_text = self.definition['Header']
            self.draw_image(header_filepath, 0, self.height - header_height, self.width, header_height)
            self.draw_paragraph(header_text, self.x_offset, self.y_offset + self.height - text_top, self.width, header_height - text_top, header_font, header_font_size, TA_CENTER, MIDDLE)
        except Exception:
            traceback.print_exc()


    def draw_image(self, image_filepath, x_offset, y_offset, width, height):
        self.canvas.drawImage(image_filepath, self.x_offset + x_offset, self.y_offset + y_offset, width, height, mask='auto')


    def draw_paragraph(self, msg, x, y, max_width, max_height, fontName, fontSize, alignment = TA_LEFT, vertical_alignment = TOP):
        self.register_font(fontName)

        style = ParagraphStyle(
            name='Normal',
            fontName=fontName,
            fontSize=fontSize,
            alignment=alignment
        )
        w, font_height = Paragraph('T', style=style).wrap(max_width, max_height)
        style = ParagraphStyle(
            name='Normal',
            fontName=fontName,
            fontSize=fontSize,
            alignment=alignment,
            leading=font_height/2
        )
        message = str(msg).replace('\n', '<br />')
        message = Paragraph(message, style=style)
        w, h = message.wrap(max_width, max_height)
        effective_y = y - h
        if vertical_alignment == BOTTOM:
            effective_y = y - max_height
        if vertical_alignment == MIDDLE:
            effective_y = y - ((max_height - h) / 2.0) - h
        message.drawOn(self.canvas, x, effective_y)


    def register_font(self, font):
        detail_font_path = os.path.join(self.deck.style_path, font)
        pdfmetrics.registerFont(TTFont(font, detail_font_path))