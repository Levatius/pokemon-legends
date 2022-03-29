import pandas as pd
from PIL import Image

from config import *


def xy(width_cm, height_cm):
    return int(64 * width_cm), int(64 * height_cm)


def pos(x, y):
    return int(512 * x), int(896 * y)


def read_cube(cube_name='sinnoh_cube', sheet_name='pokemon'):
    df = pd.read_excel(ROOT_DIR / f'{cube_name}.xlsx', sheet_name)
    return df


def get_img(file_path, size):
    return Image.open(file_path).convert('RGBA').resize(size)


def get_multiline_text_list_and_font(text, draw, font, max_width, max_lines):
    text_list = text.split(' ')
    multiline_text_list = []
    for text_ in text_list:
        if not multiline_text_list or draw.textsize(f'{multiline_text_list[-1]} {text_}', font)[0] >= 64 * max_width:
            multiline_text_list.append('')
        multiline_text_list[-1] += text_ + ' '

    # If there are too many lines, decrease the font size and try again:
    if len(multiline_text_list) > max_lines:
        smaller_font = ImageFont.truetype(font.path, size=font.size - 2)
        multiline_text_list, font = get_multiline_text_list_and_font(text, draw, smaller_font, max_width, max_lines)

    return multiline_text_list, font


def wrap_text(text, draw, font, max_width, max_lines):
    multiline_text_list, font_used = get_multiline_text_list_and_font(text, draw, font, max_width, max_lines)
    return '\n'.join(multiline_text_list), font_used
