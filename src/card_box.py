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
from paragraph import draw_paragraph

TOP = 'top'
BOTTOM = 'bottom'
MIDDLE = 'middle'

from font_style import FontStyle, LEFT, CENTER, RIGHT, TOP, MIDDLE, BOTTOM
from deck import Deck
from card import Card
from fitting import fit_image
from box import Box
from point import Point
from position import Position
from image import draw_image

class CardBox:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.cover_card = deck.cover_card

    def draw_box(self):
        try:
            print(f'printing box for {self.deck.name}')
            self.style = self.deck.style
            filepath =  os.path.join(self.style.output_folder, self.deck.name + ' Box.pdf')
            self.canvas = Canvas(filepath, pagesize=landscape(A4))
            self.position = Position(self.style, self.canvas, 0, self.style.rows - 1)
            card_thickness = self.style.card_thickness
            extra_box_space = self.style.extra_box_space
            thickness = max(self.style.min_box_thickness, len(self.deck.cards) * card_thickness + extra_box_space)
            width = self.style.card_width + self.style.extra_box_width
            height = self.style.card_height
            tab_length = self.style.tab_length
            tab_cutout_width = self.style.tab_cutout_width
            tab_cutout_length = self.style.tab_cutout_length
            tongue_length = self.style.tongue_length
            tongue_curve_height = self.style.tongue_curve_height
            border_width = self.style.border_width
            pull_depth = self.style.pull_depth
            pull_width = self.style.pull_width
            self.x_offset = self.style.page_left_margin
            self.y_offset = self.style.page_bottom_margin + thickness
            self.position.x_offset = self.x_offset
            self.position.y_offset = self.y_offset
            self.front_position = Position(self.position.style, self.position.canvas, 0, self.style.rows - 1)
            self.front_position.x_offset = self.x_offset + thickness + self.style.extra_box_width / 2
            self.front_position.y_offset = self.y_offset
            
            self.back_position = Position(self.position.style, self.position.canvas, 0, self.style.rows - 1)
            self.back_position.x_offset = self.x_offset + thickness + width + thickness
            self.back_position.y_offset = self.y_offset

            self.full_box = Box(0, -thickness, thickness + width + thickness + width + thickness, height + thickness)
            self.top_left_tab_box = Box(0, height, thickness, tab_length)
            self.top_right_tab_box = Box(thickness + width, height, thickness, tab_length)
            self.tongue_box = Box(thickness + width + thickness, height, width, thickness + tongue_length)
            self.front_box = Box(thickness, 0, width, height)
            self.back_box = Box(thickness + width + thickness, 0, width, height)
            self.label_height = self.style.header_height
            self.top_box = Box(thickness + width + thickness + border_width, height + (thickness - self.label_height) / 2 , width - border_width * 2, self.label_height)
            self.bottom_box = Box(thickness + width + thickness + border_width, -thickness + (thickness - self.label_height) / 2, width - border_width * 2, self.label_height)
            self.front_label_box = Box(thickness + border_width, border_width, width - border_width * 2, self.label_height)
            self.front_image_box = Box(thickness + border_width, border_width + self.label_height + 2, width - border_width * 2, height - self.label_height - border_width * 2 - pull_depth)

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

            self.draw_label(self.position, self.top_box)
            self.draw_label(self.position, self.bottom_box)



    def reverse_box(self, box: Box):
        return Box(box.x_offset, self.style.page_width - self.y_offset - box.y_offset - box.height - self.y_offset, box.width, box.height)


    def reverse_point(self, point: Point):
        return Point(point.x, self.style.page_width - self.y_offset - point.y - self.y_offset)


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
            if self.cover_card is not None:
                self.cover_card.draw_back(self.back_position)
            else:
                back = self.style.info['Back']
                back_image = back['Image']
                back_image_filepath = os.path.join(self.style.image_path, back_image)
                back_position = Position(self.position.style, self.position.canvas, 0, 0)
                draw_image(back_image_filepath, self.position, box)
        except Exception:
            traceback.print_exc()


    def draw_front(self, box: Box):
        try:
            if self.cover_card is not None:
                self.cover_card.draw_front(self.front_position)
            else:
                front = self.deck.info.get('Front', None)
                if front is not None:
                    self.draw_label(self.position, self.front_label_box)
                    front_image = front.get('Image')
                    front_image_filepath = os.path.join(self.style.image_path, front_image)
                    draw_image(front_image_filepath, self.position, self.front_image_box, 'Fit')

                if front is None:
                    self.draw_back(box)

        except Exception:
            traceback.print_exc()


    # def draw_image(self, image_filepath, box: Box, placement = 'None'):
    #     if not os.path.isfile(image_filepath):
    #         print(f'Image not found: {image_filepath}')
    #     if os.path.isfile(image_filepath):
    #         if placement == 'Fit':
    #             box = fit_image(image_filepath, box)
    #         self.canvas.drawImage(image_filepath, self.x_offset + box.x_offset, self.y_offset + box.y_offset, box.width, box.height, mask='auto')


    def draw_rectangle(self, box: Box, corner_radius, fill):
        self.canvas.roundRect(self.x_offset + box.x_offset, self.y_offset + box.y_offset, box.width, box.height, corner_radius, stroke=1, fill=1)


    def draw_label(self, position: Position, box: Box):
        try:
            top_text = self.deck.label
            header_filepath = self.style.header_filepath
            draw_image(header_filepath, self.position, box)
            draw_paragraph(top_text, position, box, self.style.header_font_style)
        except Exception:
            traceback.print_exc()
