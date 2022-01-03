import traceback
import os
import yaml
from decimal import Decimal
from version import __version__
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

from position import Position
from box import Box
from font_style import FontStyle, CENTER
from style import Style


TOP = 'top'
BOTTOM = 'bottom'
MIDDLE = 'middle'


class Card:
    def __init__(self, name, info, style: Style, quantity = 1):
        self.name = name
        self.quantity = quantity
        self.type = info.get('Type', 'General')
        self.style = style
        self.info = info
        self.card_size = style.card_size
        self.width = self.card_size['Width'] * mm
        self.height = self.card_size['Height'] * mm


    def draw_front(self, position: Position):
        try:
            self.pre_draw()
            self.draw_background(position)
            if self.use_long_description():
                self.draw_long_description(position)
            else:
                self.draw_artwork(position)
                self.draw_description(position)
                self.draw_specifications(position)
                self.draw_category(position)
            self.draw_version(position)
            self.draw_border(position)
            self.draw_header(position)
        except Exception:
            traceback.print_exc()


    def use_long_description(self):
        return not 'Image' in self.info


    def pre_draw(self):
        self.set_header()
        self.set_categories()
        pass


    def set_header(self):
        if self.info.get('Header', '') == '':
            self.info['Header'] = self.name


    def set_categories(self):
        self.info['Category'] = self.info.get('Category', self.info.get('Type', ''))


    def draw_background(self, position: Position):
        try:
            self.draw_image(self.style.background_filepath, position, self.style.card_box)
        except Exception:
            traceback.print_exc()


    def draw_back(self, position: Position):
        try:
            if 'Details' in self.info:
                self.draw_back_with_details(position)
            elif 'Back Image' in self.info:
                self.draw_back_with_image(position)
            else:
                self.draw_deck_back(position)
        except Exception:
            traceback.print_exc()


    def draw_back_with_image(self, position: Position):
        try:
            border_width =  self.style.border_width
            self.draw_background(position)
            self.draw_back_image(position, self.style.header_height, border_width*mm, border_width*mm)
            self.draw_border(position)
            self.draw_header(position)
        except Exception:
            traceback.print_exc()


    def draw_back_image(self, position: Position, top_padding, bottom_padding, side_padding):
        try:
            if 'Back Image' in self.info:
                back_image = self.info.get('Back Image', '')
                back_image_filepath = os.path.join(self.style.image_path, back_image)
                max_image_height =  self.height - (top_padding + bottom_padding)
                max_image_width =  self.width - side_padding
                if os.path.isfile(back_image_filepath):
                    iw, ih = utils.ImageReader(back_image_filepath).getSize()
                    image_aspect_ratio = ih / float(iw)
                    image_height = max_image_height
                    image_width = image_height / image_aspect_ratio
                    if image_width > max_image_width:
                        image_width = max_image_width
                        image_height = max_image_width * image_aspect_ratio
                    back_image_box = Box((self.width - image_width) / 2, (max_image_height - image_height) / 2 + bottom_padding, image_width, image_height)
                    self.draw_image(back_image_filepath, position, back_image_box)
            else:
                back = self.style.info['Back']
                back_image = back['Image']
                back_image_filepath = os.path.join(self.style.back_path, back_image)
                self.draw_image(back_image_filepath, position, self.style.card_box)
        except Exception:
            traceback.print_exc()


    def draw_deck_back(self, position: Position):
        try:
            back = self.style.info['Back']
            back_image = back['Image']
            back_image_filepath = os.path.join(self.style.back_path, back_image)
            self.draw_image(back_image_filepath, position, self.style.card_box)
        except Exception:
            traceback.print_exc()


    def draw_back_with_details(self, position: Position):
        try:
            self.draw_background(position)
            self.draw_details(position)
            self.draw_border(position)
            self.draw_header(position)
        except Exception:
            traceback.print_exc()


    def draw_details(self, position: Position):
        try:
            detail_text = self.info.get('Details', '')
            self.draw_paragraph(detail_text, position, self.style.details_box, self.style.details_font_style)
        except Exception:
            traceback.print_exc()

    def draw_long_description(self, position: Position):
        try:
            description_text = self.info.get('Description', '')
            self.draw_paragraph(description_text, position, self.style.details_box, self.style.details_font_style)
        except Exception:
            traceback.print_exc()


    def draw_specifications(self, position: Position):
        pass


    def draw_artwork(self, position: Position):
        try:
            image = self.style.info['Image']
            max_image_height =  image['Height'] * mm
            max_image_width =  image['Width'] * mm
            image_top =  image['Top'] * mm
            image_filename = self.info['Image']
            image_filepath = os.path.join(self.style.image_path, image_filename)
            if os.path.isfile(image_filepath):
                iw, ih = utils.ImageReader(image_filepath).getSize()
                image_aspect_ratio = ih / float(iw)
                image_height = max_image_height
                image_width = image_height / image_aspect_ratio
                if image_width > max_image_width:
                    image_width = max_image_width
                    image_height = max_image_width * image_aspect_ratio
                    image_top = image_top + (max_image_height - image_height) / 2
                image_box = Box((self.width - image_width) / 2, self.height - image_top - image_height, image_width, image_height)
                self.draw_image(image_filepath, position, image_box)
        except Exception:
            traceback.print_exc()


    def draw_specification(self, label, value, position: Position):
        try:
            if value == '':
                return
            image = self.style.info['Image']
            image_top =  image['Top'] * mm
            specs = self.style.info['Specifications']
            spec_label_font =  specs['Label Font']
            spec_label_font_size =  specs['Label Font Size']
            spec_value_font =  specs['Value Font']
            spec_value_font_size =  specs['Value Font Size']
            spec_line_spacing =  specs['Line Spacing']
            spec_offset =  specs['Offset'] * mm
            spec_height =  specs['Height'] * mm
            spec_width =  specs['Width'] * mm
            spec_spacing =  specs['Spacing'] * mm
            alignment = self.style.specifications[label]['Alignment']
            row = self.style.specifications[label]['Row']
            y_offset = self.height - image_top - row * (spec_height + spec_spacing)
            if alignment == 'Left':
                x_offset = spec_offset
            if alignment == 'Right':
                x_offset = self.width - spec_offset - spec_width
            spec_box = Box(x_offset, y_offset, spec_width, spec_height)
            spec_label_font_style = FontStyle(spec_label_font, spec_label_font_size, spec_line_spacing, CENTER, TOP)
            spec_value_font_style = FontStyle(spec_value_font, spec_value_font_size, spec_line_spacing, CENTER, MIDDLE)
            self.draw_paragraph(label, position, spec_box, spec_label_font_style)
            self.draw_paragraph(value, position, spec_box, spec_value_font_style)

        except Exception:
            traceback.print_exc()


    def draw_category(self, position: Position):
        try:
            # category_text = self.info['Category']
            # if self.info.get('Subcategory', '') != '':
            #     category_text = category_text + ' - ' + self.info['Subcategory']
            # self.draw_image(self.style.category_filepath, position, self.style.category_image_box)
            # self.draw_paragraph(category_text, position, self.style.category_box, self.style.category_font_style)
            pass
        except Exception:
            traceback.print_exc()


    def draw_description(self, position: Position):
        try:
            description_text = self.info.get('Description', '')
            self.draw_image(self.style.description_filepath, position, self.style.description_image_box)
            self.draw_paragraph(description_text, position, self.style.description_box, self.style.description_font_style)
        except Exception:
            traceback.print_exc()


    def draw_border(self, position: Position):
        try:
            self.draw_image(self.style.border_filepath, position, self.style.card_box)
        except Exception:
            traceback.print_exc()


    def draw_header(self, position: Position):
        try:
            header_text = self.info['Header']
            self.draw_image(self.style.header_filepath, position, self.style.header_image_box)
            self.draw_paragraph(header_text, position, self.style.header_box, self.style.header_font_style)
        except Exception:
            traceback.print_exc()

    def draw_version(self, position: Position):
        try:
            version_text = f'Deck Builder: {__version__}'
            self.draw_paragraph(version_text, position, self.style.version_box, self.style.version_font_style)
        except Exception:
            traceback.print_exc()


    def draw_image(self, image_filepath, position: Position, box: Box):
        if os.path.isfile(image_filepath):
            position.canvas.drawImage(image_filepath, position.x_offset + box.x_offset, position.y_offset + box.y_offset, box.width, box.height, mask='auto')


    def draw_paragraph(self, msg, position: Position, box: Box, font_style: FontStyle):
        self.register_font(font_style.name)
        style = ParagraphStyle(
            name='Normal',
            fontName=font_style.name,
            fontSize=font_style.size,
            alignment=font_style.horizontal_alignment,
            leading=font_style.size * font_style.line_spacing
        )
        message = str(msg).replace('\n', '<br/>')
        message = Paragraph(message, style=style)
        w, message_height = message.wrap(box.width, box.height)
        effective_y = box.y_offset - message_height
        if font_style.vertical_alignment == BOTTOM:
            effective_y = box.y_offset - box.height
        if font_style.vertical_alignment == MIDDLE:
            effective_y = box.y_offset - ((box.height - message_height) / 2.0) - message_height
        message.drawOn(position.canvas, position.x_offset + box.x_offset, position.y_offset + effective_y)


    def register_font(self, font):
        detail_font_path = os.path.join(self.style.style_path, font)
        pdfmetrics.registerFont(TTFont(font, detail_font_path))
