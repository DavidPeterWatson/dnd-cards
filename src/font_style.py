from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


TOP = 'top'
BOTTOM = 'bottom'
MIDDLE = 'middle'
LEFT = TA_LEFT
CENTER = TA_CENTER
RIGHT = TA_RIGHT

class FontStyle():
    def __init__(self, name, size, line_spacing, horizontal_alignment, vertical_alignment):
        self.name = name
        self.size = size
        self.line_spacing = line_spacing
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment

