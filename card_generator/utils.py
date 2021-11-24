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


def wrap_text(text, draw, font, max_width):
    text_list = text.split(' ')
    multiline_text_list = []
    for text in text_list:
        if not multiline_text_list or draw.textsize(f'{multiline_text_list[-1]} {text}', font)[0] >= 64 * max_width:
            multiline_text_list.append(str())
        multiline_text_list[-1] += text + ' '
    return '\n'.join(multiline_text_list)
