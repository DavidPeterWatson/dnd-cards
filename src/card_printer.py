# from borb.pdf.document import Document
# from borb.pdf.page.page import Page
# from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
# from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
# from borb.pdf.canvas.layout.text.paragraph import Paragraph
# from borb.pdf.canvas.layout.image.image import Image
# from borb.pdf.canvas.layout.layout_element import Alignment
from reportlab.lib.units import mm
import os
import yaml

from decimal import Decimal

def print_card(deck, card, canvas, column, row):
    print(yaml.safe_dump(card, sort_keys=False))
    style = deck['Deck Styles'][deck['Style']]
    root_folder = deck['Root Folder']
    style_folder = style['StyleFolder']

    # Draw Background
    background_filename =  style['Background']
    background_filepath = os.path.join(root_folder, style_folder, background_filename)
    card_size = deck['Card Sizes'][style['Card Size']]
    card_width = card_size['Width']
    card_height = card_size['Height']
    rows = style['Rows']
    pdf_row = abs(row - rows + 1)
    canvas.drawImage(background_filepath, column * card_width * mm, pdf_row * card_height * mm, card_width * mm, card_height * mm, mask='auto')

    #Draw Image
    image = style['Image']
    image_folder = image['Folder']
    image_filename = card['Image']
    image_height =  image['Height']
    image_width =  image['Width']
    image_top =  image['Top']
    image_filepath = os.path.join(root_folder, image_folder, image_filename)
    canvas.drawImage(image_filepath, (column * card_width + (card_width - image_width) / 2) * mm, (pdf_row * card_height + card_height - image_top - image_height) * mm, image_width * mm, image_height * mm, mask='auto')

    # Draw Detail
    detail = style['Detail']
    detail_filename =  detail['Image']
    detail_height =  detail['Height']
    detail_font =  detail['Font']
    detail_font_size =  detail['Font Size']
    detail_top_offset =  detail['Top Offset']
    detail_left_offset =  detail['Left Offset']
    detail_text = card['Detail']
    detail_filepath = os.path.join(root_folder, style_folder, detail_filename)
    canvas.drawImage(detail_filepath, column * card_width * mm, pdf_row * card_height * mm, card_width * mm, detail_height * mm, mask='auto')
    canvas.setFont(detail_font, detail_font_size)
    canvas.drawString((column * card_width + detail_left_offset) * mm , (pdf_row * card_height + detail_height - detail_top_offset) * mm, detail_text)

    # Draw Category
    category = style['Category']
    category_font =  category['Font']
    category_font_size =  category['Font Size']
    category_top_offset =  category['Top Offset']
    category_text = card['Subcategory'] + ' ' + card['Category']
    canvas.setFont(category_font, category_font_size)
    canvas.drawCentredString((column + 0.5) * card_width * mm, (pdf_row * card_height + detail_height - category_top_offset ) * mm, category_text)

    # Draw Border
    border = style['Border']
    border_filename =  border['Image']
    border_filepath = os.path.join(root_folder, style_folder, border_filename)
    canvas.drawImage(border_filepath, column * card_width * mm, pdf_row * card_height * mm, card_width * mm, card_height * mm, mask='auto')

    # Draw Header
    header = style['Header']
    header_filename =  header['Image']
    header_height =  header['Height']
    text_top = header['TextTop']
    header_font = header['Font']
    header_font_size = header['Font Size']
    header_filepath = os.path.join(root_folder, style_folder, header_filename)
    canvas.drawImage(header_filepath, column * card_width * mm, (pdf_row * card_height + card_height - header_height) * mm, card_width * mm, header_height * mm, mask='auto')
    canvas.setFont(header_font, header_font_size)
    canvas.drawCentredString((column + 0.5) * card_width * mm, (pdf_row * card_height + card_height - text_top) * mm, card['Header'])
