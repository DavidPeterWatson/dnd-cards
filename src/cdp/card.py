import traceback
import os
from cdp.version import __version__
from reportlab.lib.units import mm
from reportlab.lib.colors import black

from cdp.position import Position
from cdp.box import Box
from cdp.font_style import FontStyle
from cdp.alignment import TOP, BOTTOM, MIDDLE, LEFT, CENTER, RIGHT
from cdp.style import Style
from cdp.draw import draw_image, draw_rectangle, draw_paragraph


class Card:
    def __init__(self, name, info, style: Style):
        self.name = name
        self.type = info.get('Type', 'General')
        self.style = style
        self.info = info
        self.card_size = style.card_size
        self.width = self.card_size['Width'] * mm
        self.height = self.card_size['Height'] * mm
        self.creature_info = None


    def draw_front(self, position: Position):
        try:
            self.pre_draw()
            self.draw_background(position)
            if self.use_long_description():
                self.draw_long_description(position)
            else:
                if self.has_front_image(): self.draw_artwork(position)
                self.draw_description(position)
                if self.has_specifications(): self.draw_specifications(position)
            self.draw_version(position)
            self.draw_border(position)
            self.draw_header(position)
           
        except Exception:
            traceback.print_exc()


    def use_long_description(self):
        return not self.has_specifications() and not self.has_front_image()


    def pre_draw(self):
        self.set_header()
        self.set_categories()
        pass


    def set_header(self):
        if self.info.get('Header', '') == '':
            self.info['Header'] = self.name


    def set_categories(self):
        self.info['Category'] = self.info.get('Category', self.info.get('Type', ''))


    def draw_back(self, position: Position):
        try:
            if 'Details' in self.info:
                self.draw_back_with_details(position)
            elif self.has_back_image():
                self.draw_back_with_image(position)
            else:
                self.draw_deck_back(position)
        except Exception:
            traceback.print_exc()

    def has_back_image(self):
        return self.get_back_image() != ''

    def get_back_image(self):
        return self.info.get('Back Image', '')

    def has_front_image(self):
        return 'Image' in self.info

    def get_front_image(self):
        return self.info['Image']

    def draw_back_with_image(self, position: Position):
        try:
            border_width =  self.style.border_width
            self.draw_background(position)
            self.draw_back_image(position, self.style.header_height + self.style.header_top_margin + self.style.header_bottom_margin, border_width, border_width)
            self.draw_border(position)
            self.draw_header(position)
        except Exception:
            traceback.print_exc()


    def draw_back_image(self, position: Position, top_padding, bottom_padding, side_padding):
        try:
            if self.has_back_image():
                back_image = self.get_back_image()
                back_image_filepath = os.path.join(self.style.image_path, back_image)
                max_image_height =  self.height - (top_padding + bottom_padding)
                max_image_width =  self.width - side_padding
                back_image_box = Box((self.width - max_image_width) / 2, bottom_padding, max_image_width, max_image_height)
                draw_image(back_image_filepath, position, back_image_box, 'Fit')
            else:
                back = self.style.info['Back']
                back_image = back['Image']
                back_image_filepath = os.path.join(self.style.image_path, back_image)
                draw_image(back_image_filepath, position, self.style.card_box)
        except Exception:
            traceback.print_exc()


    def draw_deck_back(self, position: Position):
        try:
            back = self.style.info['Back']
            back_image = back['Image']
            back_image_filepath = os.path.join(self.style.image_path, back_image)
            draw_image(back_image_filepath, position, self.style.card_box)
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
            draw_paragraph(detail_text, position, self.style.details_box, self.style.details_font_style)
        except Exception:
            traceback.print_exc()


    def draw_long_description(self, position: Position):
        try:
            description_text = self.info.get('Description', '')
            draw_paragraph(description_text, position, self.style.details_box, self.style.details_font_style)
        except Exception:
            traceback.print_exc()


    def has_specifications(self):
        return False


    def draw_specifications(self, position: Position):
        pass


    def draw_artwork(self, position: Position):
        try:
            image = self.style.info['Image']
            image_height =  image['Height'] * mm
            full_width = self.width - self.style.border_width * 2
            image_width = image['Width'] * mm if self.has_specifications() else full_width
            image_top =  image['Top'] * mm
            image_filename = self.get_front_image()
            image_filepath = os.path.join(self.style.image_path, image_filename)
            if os.path.isfile(image_filepath):
                image_box = Box((self.width - image_width) / 2, self.height - image_top - image_height, image_width, image_height)
                draw_image(image_filepath, position, image_box, 'Fit')
        except Exception:
            traceback.print_exc()


    def draw_specification(self, label, value, position: Position):
        try:
            if value == '':
                return
            value = str(value)
            image = self.style.info['Image']
            specs = self.style.info['Specifications']
            spec_label_font =  specs['Label Font']
            spec_label_font_path = os.path.join(self.style.full_font_path, spec_label_font)
            spec_label_font_size =  specs['Label Font Size']
            spec_value_font =  specs['Value Font']
            spec_value_font_path = os.path.join(self.style.full_font_path, spec_value_font)
            spec_value_font_size =  specs['Value Font Size']
            long_value_count =  specs['Long Value Character Count']
            if len(value) >= long_value_count:
                spec_value_font_size = specs['Long Value Font Size']
            spec_line_spacing =  specs['Line Spacing']
            spec_offset =  specs['Offset'] * mm
            spec_height =  specs['Height'] * mm
            spec_width =  specs['Width'] * mm
            spec_spacing =  specs['Spacing'] * mm
            specification = self.style.specifications.get(label, None)
            if not specification:
                print(f'Specification not found: {label}')
                return
            alignment = specification['Alignment']
            row = specification['Row']
            y_offset = self.style.header_box.y_offset- self.style.header_bottom_margin - row * (spec_height + spec_spacing)
            if alignment == 'Left':
                x_offset = spec_offset
            if alignment == 'Right':
                x_offset = self.width - spec_offset - spec_width
            spec_box = Box(x_offset, y_offset, spec_width, spec_height)
            spec_label_font_style = FontStyle(spec_label_font, spec_label_font_path, spec_label_font_size, spec_line_spacing, CENTER, TOP)
            spec_value_font_style = FontStyle(spec_value_font, spec_value_font_path, spec_value_font_size, spec_line_spacing, CENTER, MIDDLE)
            draw_paragraph(label, position, spec_box, spec_label_font_style)
            draw_paragraph(value, position, spec_box, spec_value_font_style)

        except Exception:
            traceback.print_exc()


    def draw_category(self, position: Position):
        try:
            category_text =  self.info['Category'].lower()
            draw_paragraph(category_text, position, self.style.category_text_box, self.style.category_font_style)
            pass
        except Exception:
            traceback.print_exc()


    def draw_description(self, position: Position):
        try:
            description_text = self.info.get('Description', '')
            if description_text != '':
                description_text = f'{description_text}\n'
            instructions = self.get_instructions()
            description_text = f'{description_text}{instructions}'
            draw_image(self.style.description_filepath, position, self.style.description_image_box)
            draw_paragraph(description_text, position, self.style.description_text_box, self.style.description_font_style)
        except Exception:
            traceback.print_exc()


    def get_instructions(self):
        return ''


    def draw_border(self, position: Position):
        try:
            border_width =  self.style.border_width
            half_border_width = border_width / 2.0
            position.canvas.setLineWidth(border_width)
            position.canvas.setStrokeColor(black)
            draw_rectangle(position, Box(half_border_width, half_border_width, self.width - border_width, self.height - border_width), half_border_width, stroke=1, fill=0)
        except Exception:
            traceback.print_exc()


    def draw_background(self, position: Position):
        try:
            border_width =  self.style.border_width
            background_box = Box(border_width, border_width, self.width - border_width * 2, self.height - border_width * 2)
            draw_image(self.style.background_filepath, position, background_box)
        except Exception:
            traceback.print_exc()


    def draw_header(self, position: Position):
        try:
            header_text = self.info['Header']
            draw_image(self.style.header_filepath, position, self.style.header_box)
            draw_paragraph(header_text, position, self.style.header_text_box, self.style.header_font_style)
            self.draw_category(position)
        except Exception:
            traceback.print_exc()


    def draw_version(self, position: Position):
        try:
            version_text = f'Deck Builder: {__version__}'
            draw_paragraph(version_text, position, self.style.version_text_box, self.style.version_font_style)
        except Exception:
            traceback.print_exc()
