from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import traceback
from cdb.position import Position
from cdb.box import Box
from cdb.font_style import FontStyle
from cdb.fitting import fit_image
from cdb.alignment import TOP, BOTTOM, MIDDLE, LEFT, CENTER, RIGHT
from cdb.style import Style
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


def draw_paragraph(msg, position: Position, box: Box, font_style: FontStyle):
    try:
        register_font(font_style)
        style = ParagraphStyle(
            name='Normal',
            fontName=font_style.name,
            fontSize=font_style.size,
            alignment=font_style.horizontal_alignment,
            leading=font_style.size * font_style.line_spacing
        )
        message = Paragraph(str(msg).replace('\n', '<br/>'), style=style)
        w, message_height = message.wrap(box.width, box.height)
        effective_y = box.y_offset + box.height - message_height
        if font_style.vertical_alignment == BOTTOM:
            effective_y = box.y_offset
        if font_style.vertical_alignment == MIDDLE:
            effective_y = box.y_offset + ((box.height - message_height) / 2.0)
        message.drawOn(position.canvas, position.x_offset + box.x_offset, position.y_offset + effective_y)
    except Exception:
        pass
        # traceback.print_exc()


def register_font(font_style: FontStyle):
    try:
        if not os.path.isfile(font_style.font_path):
            print(f'Font not found: {font_style.font_path}')
        pdfmetrics.registerFont(TTFont(font_style.name, font_style.font_path))
    except Exception:
        traceback.print_exc()