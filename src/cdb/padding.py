from reportlab.lib.units import mm


class Padding():
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


def padding_from_dict(padding):
    return Padding(padding.get('Top', 0) * mm, padding.get('Bottom', 0) * mm, padding.get('Left', 0) * mm, padding.get('Right', 0) * mm)
