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

            self.full_box = Box(0, -thickness, thickness + width + thickness + width + thickness, height + thickness)
            self.top_left_tab_box = Box(0, height, thickness, tab_length)
            self.top_right_tab_box = Box(thickness + width, height, thickness, tab_length)
            self.tongue_box = Box(thickness + width + thickness, height, width, thickness + tongue_length)
            self.front_box = Box(thickness, 0, width, height)
            self.back_box = Box(thickness + width + thickness, 0, width, height)
            self.label_height = 12*mm
            self.top_box = Box(thickness + width + thickness + border_width, height + (thickness - self.label_height) / 2 , width - border_width * 2, self.label_height)
            self.bottom_box = Box(thickness + width + thickness + border_width, -thickness + (thickness - self.label_height) / 2, width - border_width * 2, self.label_height)
            self.front_label_box = Box(thickness + border_width, border_width, width - border_width * 2, self.label_height)
            self.front_image_box = Box(thickness + border_width, border_width + self.label_height + 2, width - border_width * 2, height - self.label_height - border_width * 2 - pull_depth )

            self.draw_outside()
            self.canvas.showPage()
            
            self.canvas.setLineWidth(0.5)
            self.canvas.setStrokeColor(lightsteelblue)
            left_side_top_left = Point(0, height)
            back_top_right = Point(thickness + width + thickness + width, height)
            lid_top_left = Point(thickness + width + thickness, height + thickness)
            lid_top_right = Point(thickness + width + thickness + width, height + thickness)
            self.draw_reverse_line(left_side_top_left, back_top_right)
            self.draw_reverse_line(lid_top_left, lid_top_right)

            left_bottom_left = Point(0, 0)
            back_bottom_right = Point(thickness + width + thickness + width, 0)
            front_bottom_left = Point(thickness, 0)
            front_top_left = Point(thickness, height)
            front_bottom_right = Point(thickness + width, 0)
            front_top_right = Point(thickness + width, height)
            back_bottom_left = Point(thickness + width + thickness, 0)
            back_top_left = Point(thickness + width + thickness, height)
            self.draw_reverse_line(left_bottom_left, back_bottom_right)
            self.draw_reverse_line(front_bottom_left, front_top_left)
            self.draw_reverse_line(front_bottom_right, front_top_right)
            self.draw_reverse_line(back_bottom_left, back_top_left)
            self.draw_reverse_line(back_bottom_right, back_top_right)

            self.canvas.setLineWidth(0.5)
            self.canvas.setStrokeColor(black)

            top_left_tab_top_left = Point(0, height + tab_length)
            top_left_tab_top_right = Point(thickness - tab_cutout_width, height + tab_length)
            top_left_tab_middle_right = Point(thickness, height + tab_length - tab_cutout_length)
            self.draw_reverse_line(left_bottom_left, top_left_tab_top_left)
            self.draw_reverse_line(top_left_tab_top_left, top_left_tab_top_right)
            self.draw_reverse_line(top_left_tab_top_right, top_left_tab_middle_right)
            self.draw_reverse_line(top_left_tab_middle_right, front_top_left)
            
            # front top line
            front_top_thumb_left = Point(thickness + (width - pull_width) / 2, height)
            front_top_thumb_right = Point(thickness + (width - pull_width) / 2 + pull_width, height)
            front_top_thumb_bottom_left = Point(thickness + (width - pull_width) / 2, height - pull_depth)
            front_top_thumb_top_right = Point(thickness + (width - pull_width) / 2 + pull_width, height + pull_depth)
            self.draw_reverse_line(front_top_left, front_top_thumb_left)
            self.draw_reverse_line(front_top_thumb_right, front_top_right)
            self.draw_reverse_arc(front_top_thumb_bottom_left, front_top_thumb_top_right, 180, 180)

            # tab lines
            right_top_tab_middle_left = Point(thickness + width, height + tab_length - tab_cutout_length)
            right_top_tab_top_left = Point(thickness + width + tab_cutout_width, height + tab_length)
            right_top_tab_top_right = Point(thickness + width + thickness, height + tab_length)
            self.draw_reverse_line(front_top_right, right_top_tab_middle_left)
            self.draw_reverse_line(right_top_tab_middle_left, right_top_tab_top_left)
            self.draw_reverse_line(right_top_tab_top_left, right_top_tab_top_right)
            self.draw_reverse_line(right_top_tab_top_right, back_top_left)

            # tongue lines
            tongue_bottom_left = Point(thickness + width + thickness, height + thickness + tongue_length - tongue_curve_height)
            tongue_top_right = Point(thickness + width + thickness + width, height + thickness + tongue_length)
            tongue_left = Point(thickness + width + thickness, height + thickness + tongue_length - tongue_curve_height / 2)
            tongue_right = Point(thickness + width + thickness + width, height + thickness + tongue_length - tongue_curve_height / 2)
            self.draw_reverse_arc(tongue_bottom_left, tongue_top_right, 0, 180)
            self.draw_reverse_line(back_top_left, tongue_left)
            self.draw_reverse_line(tongue_right, back_top_right)

            # pull cuts
            pull_cut_left_top = Point(thickness + width + thickness + (width - pull_width) / 2, height + pull_depth)
            pull_cut_left_bottom = Point(thickness + width + thickness + (width - pull_width) / 2, height - pull_depth)
            pull_cut_right_top = Point(thickness + width + thickness + (width - pull_width) / 2 + pull_width, height + pull_depth)
            pull_cut_right_bottom = Point(thickness + width + thickness + (width - pull_width) / 2 + pull_width, height - pull_depth)
            self.draw_reverse_line(pull_cut_left_top, pull_cut_left_bottom)
            self.draw_reverse_line(pull_cut_right_top, pull_cut_right_bottom)

            # glue tab lines
            side_tab_top_right = Point(thickness + width + thickness + width + thickness, height)
            side_tab_bottom_right = Point(thickness + width + thickness + width + thickness, 0)
            self.draw_reverse_line(back_top_right, side_tab_top_right)
            self.draw_reverse_line(side_tab_top_right, side_tab_bottom_right)
            self.draw_reverse_line(side_tab_bottom_right, back_bottom_right)

            # bottom back
            outer_base_bottom_right = Point(thickness + width + thickness + width, -thickness)
            outer_base_bottom_left = Point(thickness + width + thickness, -thickness)
            self.draw_reverse_line(back_bottom_right, outer_base_bottom_right)
            self.draw_reverse_line(outer_base_bottom_right, outer_base_bottom_left)
            self.draw_reverse_line(outer_base_bottom_left, back_bottom_left)
            
            # tab bottom left 
            self.draw_reverse_line(back_bottom_left, outer_base_bottom_left)
            inner_base_bottom_right = Point(thickness + width, -thickness)
            self.draw_reverse_line(outer_base_bottom_left, inner_base_bottom_right)
            self.draw_reverse_line(inner_base_bottom_right, front_bottom_right)

            # # front bottom line
            # self.draw_line(inner_base_bottom_right, front_bottom_right)

            # front bottom base
            inner_base_bottom_left_corner = Point(thickness, -thickness)
            self.draw_reverse_line(inner_base_bottom_right, inner_base_bottom_left_corner)
            self.draw_reverse_line(inner_base_bottom_left_corner, front_bottom_left)

            bottom_left_tab_bottom_left_corner = Point(0, -thickness)
            self.draw_reverse_line(front_bottom_left, inner_base_bottom_left_corner)
            self.draw_reverse_line(inner_base_bottom_left_corner, bottom_left_tab_bottom_left_corner)
            self.draw_reverse_line(bottom_left_tab_bottom_left_corner, left_bottom_left)

            self.canvas.showPage()

            self.canvas.save()

        except Exception:
            traceback.print_exc()

    def draw_outside(self):
            self.canvas.setFillColor(black)
            self.canvas.setLineWidth(10)
            self.canvas.setStrokeColor(black)

            self.draw_rectangle(self.full_box, 0, black)
            self.draw_rectangle(self.top_left_tab_box, 0, black)
            self.draw_rectangle(self.top_right_tab_box, 0, black)
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

    def draw_line(self, point1: Point, point2: Point):
        self.canvas.line(self.x_offset + point1.x, self.y_offset + point1.y, self.x_offset + point2.x, self.y_offset + point2.y)

    def draw_reverse_line(self, point1: Point, point2: Point):
        self.draw_line(self.reverse_point(point1), self.reverse_point(point2))
    # def draw_line(self, x1, y1, x2, y2):
    #     self.canvas.line(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2)


    def draw_ellipse(self, x1, y1, x2, y2):
        self.canvas.ellipse(self.x_offset + x1, self.y_offset + y1, self.x_offset + x2, self.y_offset + y2)

    def draw_reverse_arc(self, point1: Point, point2: Point, start_angle, extent):
        self.draw_arc(self.reverse_point(point1), self.reverse_point(point2), start_angle, extent)


    def draw_arc(self, point1: Point, point2: Point, start_angle, extent):
        self.canvas.arc(self.x_offset + point1.x, self.y_offset + point1.y, self.x_offset + point2.x, self.y_offset + point2.y, start_angle + 180, extent)



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
            front = self.deck.info.get('Front', None)
            if front is not None:
                self.draw_label(self.front_label_box)

            if front is None:
                front = self.deck.info.get('Back')
            front_image = front.get('Image')
            front_image_filepath = os.path.join(self.deck.style.image_path, front_image)
            self.draw_image(front_image_filepath, self.front_image_box, 'Fit')
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

