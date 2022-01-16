from padding import Padding

class Box():
    def __init__(self, x_offset, y_offset, width, height):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height

def add_padding(box: Box, padding: Padding):
    return Box(box.x_offset + padding.left, box.y_offset + padding.bottom, box.width - padding.left - padding.right, box.height - padding.top - padding.bottom)