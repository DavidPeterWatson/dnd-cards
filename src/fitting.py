from reportlab.lib import utils
from box import Box

def fit_image(image_filepath, box: Box):
    iw, ih = utils.ImageReader(image_filepath).getSize()
    image_aspect_ratio = ih / float(iw)
    image_height = box.height
    image_width = image_height / image_aspect_ratio
    if image_width > box.width:
        image_width = box.width
        image_height = box.width * image_aspect_ratio
    return Box(box.x_offset + (box.width - image_width) / 2, box.y_offset + (box.height - image_height) / 2, image_width, image_height)