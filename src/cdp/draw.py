from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import black

import traceback
from cdp.position import Position
from cdp.box import Box
from cdp.font_style import FontStyle
from cdp.fitting import fit_image
from cdp.alignment import TOP, BOTTOM, MIDDLE, LEFT, CENTER, RIGHT
import os


def draw_image(image_filepath, position: Position, box: Box, placement = 'None'):
    if not os.path.isfile(image_filepath):
        print(f'Image not found: {image_filepath}')
    if os.path.isfile(image_filepath):
        if placement == 'Fit':
            box = fit_image(image_filepath, box)
        position.canvas.drawImage(image_filepath, position.x_offset + box.x_offset, position.y_offset + box.y_offset, box.width, box.height, mask='auto')


def draw_rectangle(position: Position, box: Box, corner_radius, stroke=1, fill=1):
    position.canvas, position.x_offset + box.x_offset, position.y_offset
    position.canvas.roundRect(position.x_offset + box.x_offset, position.y_offset + box.y_offset, box.width, box.height, corner_radius, stroke=stroke, fill=fill)


def draw_paragraph(text, position: Position, box: Box, font_style: FontStyle):
    try:
        register_font(font_style)
        # styles = getSampleStyleSheet()
        style = ParagraphStyle(
            name='Normal',
            # parent=styles['default'],
            # fontFamily = font_style.name,
            fontName=font_style.name,
            fontSize=font_style.size,
            alignment=font_style.horizontal_alignment,
            leading=font_style.size * font_style.line_spacing
        )
        # style = getSampleStyleSheet()['BodyText']
        # style.fontFamily = font_style.name
        # style.fontSize = font_style.size
        # style.alignment = font_style.horizontal_alignment
        # style.leading = font_style.size * font_style.line_spacing
        # text = '<font name="{}">{}</font>'.format(font_style.name, text)
        position.canvas.setLineWidth(0.5)
        position.canvas.setStrokeColor(black)
        paragraph = Paragraph(str(text).replace('\n', '<br/>'), style)
        w, message_height = paragraph.wrap(box.width, box.height)
        effective_y = box.y_offset + box.height - message_height
        if font_style.vertical_alignment == BOTTOM:
            effective_y = box.y_offset
        if font_style.vertical_alignment == MIDDLE:
            effective_y = box.y_offset + ((box.height - message_height) / 2.0)
        paragraph.drawOn(position.canvas, position.x_offset + box.x_offset, position.y_offset + effective_y)
    except Exception:
        pass
        # traceback.print_exc()

        # styleSheet = getSampleStyleSheet()
        # B = styleSheet['BodyText']
        # text = "X<font name=Courier>Y</font>Z"
        # P = Paragraph(text, B)

def register_font(font_style: FontStyle):
    try:
        regular_font_path = f'{font_style.font_path}-Regular.ttf'
        bold_font_path = f'{font_style.font_path}-Bold.ttf'
        italic_font_path = f'{font_style.font_path}-Italic.ttf'

        if os.path.isfile(regular_font_path):
            registerFont(TTFont(font_style.name, regular_font_path))
        else:
            print(f'Font not found: {regular_font_path}')
        if os.path.isfile(bold_font_path):
            registerFont(TTFont(f'{font_style.name}-bold', bold_font_path))
        else:
            registerFont(TTFont(f'{font_style.name}-bold', regular_font_path))
        if os.path.isfile(italic_font_path):
            registerFont(TTFont(f'{font_style.name}-italic', italic_font_path))
        else:
            registerFont(TTFont(f'{font_style.name}-italic', regular_font_path))
        registerFontFamily(font_style.name, 
            normal=font_style.name,
            bold=f'{font_style.name}-bold',
            italic=f'{font_style.name}-italic',
            boldItalic=f'{font_style.name}-bold')
    except Exception:
        traceback.print_exc()