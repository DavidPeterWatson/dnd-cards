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
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
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


class Card:
    def __init__(self, deck: Deck, info, canvas, column, row):
        self.name = info['Name']
        self.deck = deck
        self.info = info
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

    def is_in_deck(deck: Deck, card_info):
        if deck.info['Type'] == 'Character':
            return False
        return True

    def draw(self):
        try:
            self.pre_draw()
            self.draw_background()
            if self.are_details_on_front():
                self.draw_details()
            else:
                self.draw_artwork()
                self.draw_description()
                self.draw_specifications()
                self.draw_category()
            self.draw_border()
            self.draw_header()
        except Exception:
            traceback.print_exc()

    def are_details_on_front(self):
        return not 'Image' in self.info and not 'Description' in self.info

    def pre_draw(self):
        pass

    def draw_background(self):
        try:
            background_filename =  self.deck.style['Background']
            background_filepath = os.path.join(self.deck.style_path, background_filename)
            self.draw_image(background_filepath, 0, 0, self.width, self.height)
        except Exception:
            traceback.print_exc()


    def draw_back(self):
        try:
            self.x_offset = self.x_back_offset
            if 'Details' in self.info and not self.are_details_on_front():
                self.draw_back_with_details()
            else:
                self.draw_back_image()
        except Exception:
            traceback.print_exc()

    def draw_back_image(self):
        try:
            back = self.deck.info['Back']
            back_image =  back['Image']
            back_image_filepath = os.path.join(self.deck.back_path, back_image)
            self.draw_image(back_image_filepath, 0, 0, self.width, self.height)
        except Exception:
            traceback.print_exc()


    def draw_back_with_details(self):
        try:
            self.draw_background()
            self.draw_details()
            self.draw_border()
            self.draw_header()
        except Exception:
            traceback.print_exc()


    def get_character(self):
        character_name = self.deck.info.get('Character', '')
        cards = self.deck.info['Cards']
        return cards.get(character_name, {})

    def draw_details(self):
        try:
            header = self.deck.style['Header']
            header_height =  header['Height'] * mm
            details = self.deck.style['Details']
            details_font =  details['Font']
            details_font_size =  details['Font Size']
            details_padding =  details['Padding'] * mm
            detail_text = self.info.get('Details', '')
            x = self.x_offset + details_padding 
            y = self.y_offset + self.height - header_height
            self.draw_paragraph(detail_text, x, y, self.width - details_padding * 2, self.height - header_height, details_font, details_font_size, TA_LEFT, TOP)
        except Exception:
            traceback.print_exc()


    def draw_specifications(self):
        pass


    def draw_artwork(self):
        try:
            image = self.deck.style['Image']
            max_image_height =  image['Height'] * mm
            max_image_width =  image['Width'] * mm
            image_top =  image['Top'] * mm
            image_filename = self.info['Image']
            image_filepath = os.path.join(self.deck.image_path, image_filename)
            if os.path.isfile(image_filepath):
                iw, ih = utils.ImageReader(image_filepath).getSize()
                image_aspect_ratio = ih / float(iw)
                image_height = max_image_height
                image_width = image_height / image_aspect_ratio
                if image_width > max_image_width:
                    image_width = max_image_width
                    image_height = max_image_width * image_aspect_ratio
                    image_top = image_top + max_image_height - image_height
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
            detail = self.deck.style['Description']
            detail_height =  detail['Height'] * mm
            category = self.deck.style['Category']
            category_font =  category['Font']
            category_font_size =  category['Font Size']
            category_height =  category['Height'] * mm
            category_top_padding = category['Top Padding'] * mm
            category_left_padding = category['Left Padding'] * mm
            category_width = self.width - category_left_padding * 2
            category_text = self.info['Category']
            if self.info.get('Subcategory', '') != '':
                category_text = category_text + ' - ' + self.info['Subcategory']
            category_filename =  category.get('Image', '')
            category_filepath = os.path.join(self.deck.style_path, category_filename)
            self.draw_image(category_filepath, category_left_padding, detail_height, category_width, category_height)
            
            self.draw_paragraph(category_text, self.x_offset + category_left_padding, self.y_offset + detail_height + category_height - category_top_padding, category_width, category_height - category_top_padding, category_font, category_font_size, TA_CENTER, MIDDLE)
        except Exception:
            traceback.print_exc()


    def draw_description(self):
        try:
            description = self.deck.style['Description']
            description_filename =  description['Image']
            description_height =  description['Height'] * mm
            description_font =  description['Font']
            description_font_size =  description['Font Size']
            description_left_padding =  description['Left Padding'] * mm
            description_top_padding =  description['Top Padding'] * mm
            description_text = self.info.get('Description', '')
            description_filepath = os.path.join(self.deck.style_path, description_filename)
            self.draw_image(description_filepath, 0, 0, self.width, description_height)
            x = self.x_offset + description_left_padding 
            y = self.y_offset + description_height - description_top_padding 
            self.draw_paragraph(description_text, x, y, self.width - description_left_padding * 2, description_height, description_font, description_font_size, TA_LEFT, TOP)
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
            header_text = self.info['Header']
            self.draw_image(header_filepath, 0, self.height - header_height, self.width, header_height)
            self.draw_paragraph(header_text, self.x_offset, self.y_offset + self.height - text_top, self.width, header_height - text_top, header_font, header_font_size, TA_CENTER, MIDDLE)
        except Exception:
            traceback.print_exc()


    def draw_image(self, image_filepath, x_offset, y_offset, width, height):
        if os.path.isfile(image_filepath):
            self.canvas.drawImage(image_filepath, self.x_offset + x_offset, self.y_offset + y_offset, width, height, mask='auto')


    def draw_paragraph(self, msg, x, y, max_width, max_height, fontName, fontSize, alignment, vertical_alignment):
        self.register_font(fontName)

        style = ParagraphStyle(
            name='Normal',
            fontName=fontName,
            fontSize=fontSize,
            alignment=alignment,
            leading=fontSize
        )
        styles = getSampleStyleSheet()
        message = str(msg).replace('\n', '<br/>')
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