import os
import yaml
from reportlab.lib.units import mm
from cdp.library import Library
from cdp.font_style import FontStyle
from cdp.alignment import TOP, BOTTOM, MIDDLE, LEFT, CENTER, RIGHT
from cdp.box import Box, add_padding
from cdp.padding import Padding, padding_from_dict

class Style():
    def __init__(self, name, library: Library):
        self.name = name
        self.info = library.get_style(name)
        self.style_folder = self.info['Style Folder']
        self.output_folder = self.info['Output Folder']
        self.font_path: str = self.info['Fonts']['Folder']
        self.full_font_path: str = os.path.join(os.getcwd(), self.info['Fonts']['Folder'])
        self.page = self.info['Page']
        self.page_size = library.info['Page Sizes'][self.page['Size']]
        self.page_height = self.page_size['Height'] * mm
        self.page_width = self.page_size['Width'] * mm
        self.page_left_margin = self.page['Left Margin'] * mm
        self.page_bottom_margin = self.page['Bottom Margin'] * mm
        self.columns = self.info['Columns']
        self.rows = self.info['Columns']
        self.card_size = library.info['Card Sizes'][self.info['Card Size']]
        card_width = self.card_size['Width'] * mm
        self.card_width = card_width
        card_height = self.card_size['Height'] * mm
        self.card_height = card_height
        self.card_thickness = self.card_size['Thickness'] * mm
        self.extra_box_space = self.card_size['Extra Box Space'] * mm
        self.extra_box_width = self.card_size['Extra Box Width'] * mm
        self.min_box_thickness = self.card_size['Minimum Box Thickness'] * mm
        self.tab_length = self.card_size['Tab Length'] * mm
        self.tab_cutout_length = self.card_size['Tab Cutout Length'] * mm
        self.tab_cutout_width = self.card_size['Tab Cutout Width'] * mm
        self.tongue_length = self.card_size['Tongue Length'] * mm
        self.tongue_curve_height = self.card_size['Tongue Curve Height'] * mm
        self.pull_depth = self.card_size['Pull Depth'] * mm
        self.pull_width = self.card_size['Pull Width'] * mm
        
        self.image = self.info['Image']
        self.image_folder = self.image['Folder']
        self.image_path = os.path.join(self.image_folder)

        self.back = self.info['Back']
        self.specifications = self.info['Specifications']['Named']

        self.background = self.info['Background']
        self.background_filename =  self.background['Image']
        self.background_filepath = os.path.join(self.image_path, self.background_filename)

        self.border = self.info['Border']
        border_width =  self.border['Width'] * mm
        self.border_width =  border_width
        border_filename =  self.border['Image']
        self.border_filepath = os.path.join(self.image_path, border_filename)
        self.card_box = Box(0, 0, card_width, card_height)

        header = self.info['Header']
        header_height = header['Height'] * mm
        self.header_height = header_height
        header_filename =  header['Image']
        header_font = header['Font']
        self.header_padding = padding_from_dict(header.get('Padding', {}))
        header_font_path = os.path.join(self.full_font_path, header_font)
        header_font_size = header['Font Size']
        header_line_spacing = header['Line Spacing']
        self.header_filepath = os.path.join(self.image_path, header_filename)
        self.header_box = Box(0, card_height - header_height, card_width, header_height)
        self.header_text_box = add_padding(self.header_box, self.header_padding)
        self.header_font_style = FontStyle(header_font, header_font_path, header_font_size, header_line_spacing, CENTER, MIDDLE)

        category = self.info['Category']
        category_font = category['Font']
        category_font_path = os.path.join(self.font_path, category_font)
        category_font_size =  category['Font Size']
        category_line_spacing =  category['Line Spacing']
        self.category_padding = padding_from_dict(category.get('Padding', {}))
        self.category_text_box =  add_padding(self.header_box, self.category_padding)
        self.category_font_style = FontStyle(category_font, category_font_path, category_font_size, category_line_spacing, CENTER, TOP)

        details = self.info['Details']
        self.details_padding = padding_from_dict(details.get('Padding', {}))
        details_font = details['Font']
        details_font_path = os.path.join(self.full_font_path, details_font)
        details_font_size =  details['Font Size']
        details_line_spacing =  details['Line Spacing']
        self.details_font_style = FontStyle(details_font, details_font_path, details_font_size, details_line_spacing, LEFT, TOP)
        self.details_box = Box(border_width + self.details_padding.left, border_width + self.details_padding.bottom, card_width - self.details_padding.left - self.details_padding.right - border_width * 2, card_height - header_height - border_width - self.details_padding.top - self.details_padding.bottom)

        version = self.info['Version']
        version_font = version['Font']
        version_font_path = os.path.join(self.full_font_path, version_font)
        version_font_size = version['Font Size']
        self.version_padding = padding_from_dict(version.get('Padding', {}))
        version_height = 5*mm
        self.version_box = Box(border_width, border_width, card_width - border_width * 2, version_height)
        self.version_text_box = add_padding(self.version_box, self.version_padding)
        self.version_font_style = FontStyle(version_font, version_font_path, version_font_size, 1, RIGHT, BOTTOM)

        description = self.info['Description']
        description_filename =  description['Image']
        description_height =  description['Height'] * mm
        description_font = description['Font']
        description_font_path = os.path.join(self.full_font_path, description_font)
        description_font_size =  description['Font Size']
        description_line_spacing =  description['Line Spacing']
        self.description_padding = padding_from_dict(description.get('Padding', {}))
        self.description_filepath = os.path.join(self.image_path, description_filename)
        self.description_image_box = Box(border_width, border_width, card_width - border_width * 2, description_height)
        self.description_text_box = add_padding(self.description_image_box, self.description_padding)
        self.description_font_style = FontStyle(description_font, description_font_path, description_font_size, description_line_spacing, LEFT, TOP)
