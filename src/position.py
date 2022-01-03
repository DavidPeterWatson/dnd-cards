import traceback
import os
import yaml
from decimal import Decimal
from version import __version__
from reportlab.pdfgen.canvas import Canvas

import importlib
import logging

from style import Style


TOP = 'top'
BOTTOM = 'bottom'
MIDDLE = 'middle'


class Position:
    def __init__(self, style: Style, canvas: Canvas, column, row):
        self.canvas = canvas
        self.column = column
        self.row = row
        self.style = style
        self.pdf_row = abs(self.row - style.rows + 1)
        self.x_offset = self.column * style.card_width + style.page_left_margin
        self.y_offset =  self.pdf_row * style.card_height + style.page_bottom_margin

    def get_back_position(self):
        return Position(self.style, self.canvas, abs(self.column - self.style.columns + 1), self.row)