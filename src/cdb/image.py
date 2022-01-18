import traceback
from cdb.position import Position
from cdb.box import Box
import os
from cdb.fitting import fit_image

def draw_image(image_filepath, position: Position, box: Box, placement = 'None'):
    if not os.path.isfile(image_filepath):
        print(f'Image not found: {image_filepath}')
    if os.path.isfile(image_filepath):
        if placement == 'Fit':
            box = fit_image(image_filepath, box)
        position.canvas.drawImage(image_filepath, position.x_offset + box.x_offset, position.y_offset + box.y_offset, box.width, box.height, mask='auto')
