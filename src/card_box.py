import os
import traceback
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import gray, black, lightsteelblue

from deck import Deck

class CardBox:
    def __init__(self, deck: Deck):
        self.deck = deck

    def draw_box(self):
        try:
            print('printing box')
            self.canvas = Canvas('output/' + self.deck.name + ' Box.pdf', pagesize=landscape(A4))
            card_thickness = self.deck.style.card_thickness
            extra_box_space = self.deck.style.extra_box_space
            thickness = len(self.deck.cards) * card_thickness + extra_box_space
            width = self.deck.style.card_width
            height = self.deck.style.card_height
            tab_length = self.deck.style.tab_length
            tab_cutout_width = self.deck.style.tab_cutout_width
            tab_cutout_length = self.deck.style.tab_cutout_length
            tongue_length = self.deck.style.tongue_length
            tongue_curve_height = self.deck.style.tongue_curve_height
            pull_depth = self.deck.style.pull_depth
            pull_width = self.deck.style.pull_width
            self.x_offset = self.deck.style.page_left_margin
            self.y_offset = self.deck.style.page_bottom_margin + max(tab_length, thickness)


            self.canvas.setLineWidth(0.5)
            self.canvas.setStrokeColor(lightsteelblue)
            self.draw_line(0, height, thickness + width + thickness + width, height)
            self.draw_line(thickness + width + thickness, height + thickness, thickness + width + thickness + width, height + thickness)

            self.draw_line(0, 0, thickness + width + thickness + width, 0)
            self.draw_line(thickness, 0, thickness, height)
            self.draw_line(thickness + width, 0, thickness + width, height)
            self.draw_line(thickness + width + thickness, 0, thickness + width + thickness, height)
            self.draw_line(thickness + width + thickness + width, 0, thickness + width + thickness + width, height)

            self.canvas.setStrokeColor(black)

            self.draw_line(0, 0, 0, height + tab_length)
            self.draw_line(0, height + tab_length, thickness - tab_cutout_width, height + tab_length)
            self.draw_line(thickness - tab_cutout_width, height + tab_length, thickness, height + tab_length - tab_cutout_length)
            self.draw_line(thickness, height + tab_length - tab_cutout_length, thickness, height)
            
            # front top line
            self.draw_line(thickness, height, thickness + width, height)
            self.draw_arc(thickness + (width - pull_width) / 2, height - pull_depth, thickness + (width - pull_width) / 2 + pull_width, height + pull_depth, 180, 180)

            # tab lines
            self.draw_line(thickness + width, height, thickness + width, height + tab_length - tab_cutout_length)
            self.draw_line(thickness + width, height + tab_length - tab_cutout_length, thickness + width + tab_cutout_width, height + tab_length)
            self.draw_line(thickness + width + tab_cutout_width, height + tab_length, thickness + width + thickness, height + tab_length)

            # tongue lines
            self.draw_arc(thickness + width + thickness, height + thickness + tongue_length - tongue_curve_height, thickness + width + thickness + width, height + thickness + tongue_length, 0, 180)
            self.draw_line(thickness + width + thickness, height, thickness + width + thickness, height + thickness + tongue_length - tongue_curve_height / 2)
            # self.draw_line(thickness + width + thickness, height + thickness + tongue_length, thickness + width + thickness + width, height + thickness + tongue_length)
            self.draw_line(thickness + width + thickness + width, height + thickness + tongue_length - tongue_curve_height / 2, thickness + width + thickness + width, height)

            # pull cuts
            self.draw_line(thickness + width + thickness + (width - pull_width) / 2, height + thickness, thickness + width + thickness + (width - pull_width) / 2, height - pull_depth)
            self.draw_line(thickness + width + thickness + (width - pull_width) / 2 + pull_width, height + thickness, thickness + width + thickness + (width - pull_width) / 2 + pull_width, height - pull_depth)

            # glue tab lines
            self.draw_line(thickness + width + thickness + width, height, thickness + width + thickness + width + thickness, height)
            self.draw_line(thickness + width + thickness + width + thickness, height, thickness + width + thickness + width + thickness, 0)
            self.draw_line(thickness + width + thickness + width + thickness, 0, thickness + width + thickness + width, 0)

            # bottom back
            self.draw_line(thickness + width + thickness + width, 0, thickness + width + thickness + width, -thickness)
            self.draw_line(thickness + width + thickness + width, -thickness, thickness + width + thickness, -thickness)
            self.draw_line(thickness + width + thickness, -thickness, thickness + width + thickness, 0)
            
            # tab bottom left 
            self.draw_line(thickness + width + thickness, 0, thickness + width + thickness, -tab_length)
            self.draw_line(thickness + width + thickness, -tab_length, thickness + width + tab_cutout_width, -tab_length)
            self.draw_line(thickness + width + tab_cutout_width, -tab_length, thickness + width, -tab_length + tab_cutout_length)
            self.draw_line(thickness + width, -tab_length + tab_cutout_length, thickness + width, 0)

            # front bottom line
            self.draw_line(thickness + width, -thickness, thickness + width, 0)

            # front bottom base
            self.draw_line(thickness + width, -thickness, thickness, -thickness)
            self.draw_line(thickness, -thickness, thickness, 0)


            self.draw_line(thickness, 0 , thickness, -tab_length + tab_cutout_length)
            self.draw_line(thickness, -tab_length + tab_cutout_length, thickness - tab_cutout_width, -tab_length)
            self.draw_line(thickness - tab_cutout_width, -tab_length, 0, -tab_length)
            self.draw_line(0, -tab_length, 0, 0)

            self.canvas.showPage()

            
            self.canvas.save()
        except Exception:
            traceback.print_exc()

    def draw_line(self, x1, y1, x2, y2):
        self.canvas.line(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2)

    def draw_ellipse(self, x1, y1, x2, y2):
        self.canvas.ellipse(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2)

    def draw_arc(self, x1, y1, x2, y2, start_angle, extent):
        self.canvas.arc(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2, start_angle, extent)