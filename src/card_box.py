import os
import traceback
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import gray, black, lightsteelblue
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

TOP = 'top'
BOTTOM = 'bottom'
MIDDLE = 'middle'

from font_style import FontStyle, CENTER
from deck import Deck
from fitting import fit_image
from box import Box
from point import Point

class CardBox:
    def __init__(self, deck: Deck):
        self.deck = deck

    def draw_box(self):
        try:
            print('printing box')
            self.canvas = Canvas('output/' + self.deck.name + ' Box.pdf', pagesize=landscape(A4))
            card_thickness = self.deck.style.card_thickness
            extra_box_space = self.deck.style.extra_box_space
            thickness = max(self.deck.style.min_box_thickness, len(self.deck.cards) * card_thickness + extra_box_space)
            width = self.deck.style.card_width + self.deck.style.extra_box_width
            height = self.deck.style.card_height
            tab_length = self.deck.style.tab_length
            tab_cutout_width = self.deck.style.tab_cutout_width
            tab_cutout_length = self.deck.style.tab_cutout_length
            tongue_length = self.deck.style.tongue_length
            tongue_curve_height = self.deck.style.tongue_curve_height
            border_width = self.deck.style.border_width
            pull_depth = self.deck.style.pull_depth
            pull_width = self.deck.style.pull_width
            self.x_offset = self.deck.style.page_left_margin
            self.y_offset = self.deck.style.page_bottom_margin + thickness

            self.full_box = Box(0, -thickness, thickness + width + thickness + width + thickness, height + thickness + thickness)
            self.tongue_box = Box(thickness + width + thickness, height, width, thickness + tongue_length)
            self.front_box = Box(thickness, 0, width, height)
            self.back_box = Box(thickness + width + thickness, 0, width, height)
            self.top_box = Box(thickness + width + thickness + border_width, height + border_width, width - border_width * 2, thickness - border_width * 2)
            self.bottom_box = Box(thickness + width + thickness + border_width, -thickness + border_width, width - border_width * 2, thickness - border_width * 2)

            self.draw_outside()
            self.canvas.showPage()
            
            self.canvas.setLineWidth(0.5)
            self.canvas.setStrokeColor(lightsteelblue)
            self.draw_line(0, height, thickness + width + thickness + width, height)
            self.draw_line(thickness + width + thickness, height + thickness, thickness + width + thickness + width, height + thickness)

            self.draw_line(0, 0, thickness + width + thickness + width, 0)
            self.draw_line(thickness, 0, thickness, height)
            self.draw_line(thickness + width, 0, thickness + width, height)
            self.draw_line(thickness + width + thickness, 0, thickness + width + thickness, height)
            self.draw_line(thickness + width + thickness + width, 0, thickness + width + thickness + width, height)

            self.canvas.setLineWidth(0.5)
            self.canvas.setStrokeColor(black)

            self.draw_line(0, 0, 0, height + tab_length)
            self.draw_line(0, height + tab_length, thickness - tab_cutout_width, height + tab_length)
            self.draw_line(thickness - tab_cutout_width, height + tab_length, thickness, height + tab_length - tab_cutout_length)
            self.draw_line(thickness, height + tab_length - tab_cutout_length, thickness, height)
            
            # front top line
            self.draw_line(thickness, height, thickness + (width - pull_width) / 2, height)
            self.draw_line( thickness + (width - pull_width) / 2 + pull_width, height, thickness + width, height)
            self.draw_arc(thickness + (width - pull_width) / 2, height - pull_depth, thickness + (width - pull_width) / 2 + pull_width, height + pull_depth, 180, 180)

            # tab lines
            self.draw_line(thickness + width, height, thickness + width, height + tab_length - tab_cutout_length)
            self.draw_line(thickness + width, height + tab_length - tab_cutout_length, thickness + width + tab_cutout_width, height + tab_length)
            self.draw_line(thickness + width + tab_cutout_width, height + tab_length, thickness + width + thickness, height + tab_length)

            # tongue lines
            self.draw_arc(thickness + width + thickness, height + thickness + tongue_length - tongue_curve_height, thickness + width + thickness + width, height + thickness + tongue_length, 0, 180)
            self.draw_line(thickness + width + thickness, height, thickness + width + thickness, height + thickness + tongue_length - tongue_curve_height / 2)
            self.draw_line(thickness + width + thickness + width, height + thickness + tongue_length - tongue_curve_height / 2, thickness + width + thickness + width, height)

            # pull cuts
            self.draw_line(thickness + width + thickness + (width - pull_width) / 2, height + pull_depth, thickness + width + thickness + (width - pull_width) / 2, height - pull_depth)
            self.draw_line(thickness + width + thickness + (width - pull_width) / 2 + pull_width, height + pull_depth, thickness + width + thickness + (width - pull_width) / 2 + pull_width, height - pull_depth)

            # glue tab lines
            self.draw_line(thickness + width + thickness + width, height, thickness + width + thickness + width + thickness, height)
            self.draw_line(thickness + width + thickness + width + thickness, height, thickness + width + thickness + width + thickness, 0)
            self.draw_line(thickness + width + thickness + width + thickness, 0, thickness + width + thickness + width, 0)

            # bottom back
            self.draw_line(thickness + width + thickness + width, 0, thickness + width + thickness + width, -thickness)
            self.draw_line(thickness + width + thickness + width, -thickness, thickness + width + thickness, -thickness)
            self.draw_line(thickness + width + thickness, -thickness, thickness + width + thickness, 0)
            
            # tab bottom left 
            self.draw_line(thickness + width + thickness, 0, thickness + width + thickness, -thickness)
            self.draw_line(thickness + width + thickness, -thickness, thickness + width, -thickness)
            self.draw_line(thickness + width, -thickness + tab_cutout_length, thickness + width, 0)

            # front bottom line
            self.draw_line(thickness + width, -thickness, thickness + width, 0)

            # front bottom base
            self.draw_line(thickness + width, -thickness, thickness, -thickness)
            self.draw_line(thickness, -thickness, thickness, 0)

            self.draw_line(thickness, 0 , thickness, -thickness)
            self.draw_line(thickness, -thickness, 0, -thickness)
            self.draw_line(0, -thickness, 0, 0)

            self.canvas.showPage()

            self.canvas.save()

        except Exception:
            traceback.print_exc()

    def draw_outside(self):
            self.canvas.setFillColor(black)
            self.canvas.setLineWidth(10)
            self.canvas.setStrokeColor(black)

            self.draw_rectangle(self.full_box, 0, black)
            self.draw_rectangle(self.tongue_box, 0, black)
            self.draw_front(self.front_box)
            self.draw_back(self.back_box)

            self.draw_label(self.top_box)
            self.draw_label(self.bottom_box)

            # self.draw_rectangle(self.reverse_box(self.full_box), 0, black)
            # self.draw_rectangle(self.reverse_box(self.tongue_box), 0, black)
            # self.draw_front(self.reverse_box(self.front_box))
            # self.draw_back(self.reverse_box(self.back_box))

            # self.draw_label(self.reverse_box(self.top_box))
            # self.draw_label(self.reverse_box(self.bottom_box))


    def reverse_box(self, box: Box):
        return Box(box.x_offset, self.deck.style.page_width - self.y_offset - box.y_offset - box.height - self.y_offset, box.width, box.height)


    def reverse_point(self, point: Point):
        return Point(point.x, self.deck.style.page_width - self.y_offset - point.y - self.y_offset)


    def draw_line(self, x1, y1, x2, y2):
        self.canvas.line(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2)


    def draw_ellipse(self, x1, y1, x2, y2):
        self.canvas.ellipse(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2)


    def draw_arc(self, x1, y1, x2, y2, start_angle, extent):
        self.canvas.arc(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2, start_angle, extent)


    def draw_back(self, box: Box):
        try:
            back = self.deck.info['Back']
            back_image = back['Image']
            back_image_filepath = os.path.join(self.deck.style.image_path, back_image)
            self.draw_image(back_image_filepath, box)
        except Exception:
            traceback.print_exc()


    def draw_front(self, box: Box):
        try:
            front = self.deck.info.get('Front', self.deck.info['Back'])
            front_image = front.get('Image', 'back1.png')
            front_image_filepath = os.path.join(self.deck.style.image_path, front_image)
            self.draw_image(front_image_filepath, box, 'Fit')
        except Exception:
            traceback.print_exc()


    def draw_image(self, image_filepath, box: Box, placement = 'None'):
        if os.path.isfile(image_filepath):
            if placement == 'Fit':
                box = fit_image(image_filepath, box)
            self.canvas.drawImage(image_filepath, self.x_offset + box.x_offset, self.y_offset + box.y_offset, box.width, box.height, mask='auto')


    def draw_rectangle(self, box: Box, corner_radius, fill):
        self.canvas.roundRect(self.x_offset + box.x_offset, self.y_offset + box.y_offset, box.width, box.height, corner_radius, stroke=1, fill=1)


    def draw_label(self, box: Box):
        try:
            top_text = self.deck.label
            header_filename = 'Centered Scroll Header.png'
            header_filepath = os.path.join(self.deck.style.style_path, header_filename)
            self.draw_image(header_filepath, box)
            self.draw_paragraph(top_text, box, self.deck.style.header_font_style)
        except Exception:
            traceback.print_exc()


    def draw_paragraph(self, msg, box: Box, font_style: FontStyle):
        self.register_font(font_style.name)
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
        message.drawOn(self.canvas, self.x_offset + box.x_offset, self.y_offset + effective_y)


    def register_font(self, font):
        detail_font_path = os.path.join(self.deck.style.style_path, font)
        pdfmetrics.registerFont(TTFont(font, detail_font_path))

