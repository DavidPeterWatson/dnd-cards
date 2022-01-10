import os
import yaml
from reportlab.lib.units import mm
from library import Library
from font_style import FontStyle, TOP, BOTTOM, MIDDLE, LEFT, CENTER, RIGHT
from box import Box

class Style():
    def __init__(self, name, library: Library):
        self.name = name
        self.info = library.get_style(name)
        self.style_folder = self.info['Style Folder']
        self.style_path: str = os.path.join(library.root_path, self.style_folder)
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
        self.tab_length = self.card_size['Tab Length'] * mm
        self.tab_cutout_length = self.card_size['Tab Cutout Length'] * mm
        self.tab_cutout_width = self.card_size['Tab Cutout Width'] * mm
        self.tongue_length = self.card_size['Tongue Length'] * mm
        self.tongue_curve_height = self.card_size['Tongue Curve Height'] * mm
        self.pull_depth = self.card_size['Pull Depth'] * mm
        self.pull_width = self.card_size['Pull Width'] * mm
        
        self.image = self.info['Image']
        self.image_folder = self.image['Folder']
        self.image_path = os.path.join(library.root_path, self.image_folder)

        self.back = self.info['Back']
        self.back_folder = self.back['Folder']
        self.back_path: str = os.path.join(library.root_path, self.back_folder)

        self.specifications = self.info['Specifications']['Named']

        self.background_filename =  self.info['Background']
        self.background_filepath = os.path.join(self.style_path, self.background_filename)

        self.border = self.info['Border']
        border_width =  self.border['Width'] * mm
        self.border_width =  border_width
        border_filename =  self.border['Image']
        self.border_filepath = os.path.join(self.style_path, border_filename)
        self.card_box = Box(0, 0, card_width, card_height)

        header = self.info['Header']
        header_height = header['Height'] * mm
        self.header_height = header_height
        header_filename =  header['Image']
        text_top = header['TextTop'] * mm
        header_font = header['Font'] 
        header_font_size = header['Font Size']
        header_line_spacing = header['Line Spacing']
        self.header_filepath = os.path.join(self.style_path, header_filename)
        self.header_image_box = Box(0, card_height - header_height, card_width, header_height)
        self.header_box = Box(border_width, card_height - text_top, card_width - border_width * 2, header_height - text_top)
        self.header_font_style = FontStyle(header_font, header_font_size, header_line_spacing, CENTER, MIDDLE)

        details = self.info['Details']
        details_padding =  details['Padding'] * mm
        details_font =  details['Font']
        details_font_size =  details['Font Size']
        details_line_spacing =  details['Line Spacing']
        self.details_font_style = FontStyle(details_font, details_font_size, details_line_spacing, LEFT, TOP)
        self.details_box = Box(details_padding, card_height - header_height, card_width - details_padding * 2, card_height - header_height)

        version = self.info['Version']
        version_font = version['Font'] 
        version_font_size = version['Font Size']
        version_height = 5*mm
        self.version_box = Box(border_width, border_width + version_height, card_width - border_width * 2, version_height)
        self.version_font_style = FontStyle(version_font, version_font_size, 1, RIGHT, BOTTOM)

        description = self.info['Description']
        description_filename =  description['Image']
        description_height =  description['Height'] * mm
        description_font =  description['Font']
        description_font_size =  description['Font Size']
        description_line_spacing =  description['Line Spacing']
        description_left_padding =  description['Left Padding'] * mm
        description_top_padding =  description['Top Padding'] * mm
        self.description_filepath = os.path.join(self.style_path, description_filename)
        self.description_image_box = Box(0, 0, card_width, description_height)
        self.description_box = Box(description_left_padding, description_height - description_top_padding, card_width - description_left_padding * 2, description_height)
        self.description_font_style = FontStyle(description_font, description_font_size, description_line_spacing, LEFT, TOP)

        category = self.info['Category']
        category_font =  category['Font']
        category_font_size =  category['Font Size']
        category_line_spacing =  category['Line Spacing']
        # category_height =  category['Height'] * mm
        category_top_padding = category['Top Padding'] * mm
        category_left_padding = category['Left Padding'] * mm
        # category_vertical_alignment = category['Vertical Alignment']
        # category_horizonal_alignment = category['Horizontal Alignment']

        # category_width = card_width - category_left_padding * 2
        # category_filename =  category.get('Image', '')
        # self.category_filepath = os.path.join(self.style_path, category_filename)
        # self.category_image_box = Box(category_left_padding, description_height, category_width, category_height)
        self.category_box = Box(border_width + category_left_padding, card_height - category_top_padding - border_width, card_width - category_left_padding * 2 - border_width * 2, header_height - category_top_padding - border_width)
        # self.category_box = Box(category_left_padding, description_height + category_height - category_top_padding, category_width, category_height - category_top_padding)
        self.category_font_style = FontStyle(category_font, category_font_size, category_line_spacing, CENTER, TOP)
