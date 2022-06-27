import pandas as pd
from PIL import Image, ImageFont

from config import *


def xy(width_cm, height_cm):
    return int(64 * width_cm), int(64 * height_cm)


def pos(x, y):
    return int(512 * x), int(896 * y)


def _adjusted_font_size(font_size):
    return int(2.25 * font_size)


def text_font(size):
    return ImageFont.truetype(BARLOW_PATH, size=_adjusted_font_size(size))


def title_font(size):
    return ImageFont.truetype(ORIENTAL_PATH, size=_adjusted_font_size(size))


def read_cube(cube_name='sinnoh_cube', sheet_name='pokemon'):
    df = pd.read_excel(ROOT_DIR / f'{cube_name}.xlsx', sheet_name)
    return df


def get_img(file_path, size):
    return Image.open(file_path).convert('RGBA').resize(size)


# TODO: Deprecate these next two methods in favour of wrapped_text

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


def wrap_text(text, draw, starting_font, max_width, max_lines):
    multiline_text_list, font_used = get_multiline_text_list_and_font(text, draw, starting_font, max_width, max_lines)
    return '\n'.join(multiline_text_list).strip(), font_used


def wrapped_text(d, text, font, boundaries, *args, **kwargs):
    words = text.split(' ')
    multiline_text_list = []
    for word in words:
        if not multiline_text_list or d.textsize(f'{multiline_text_list[-1]} {word}', font)[0] >= xy(*boundaries)[0]:
            multiline_text_list.append('')
        multiline_text_list[-1] += word + ' '

    multiline_text = '\n'.join(multiline_text_list).strip()
    if d.textsize(multiline_text, font)[0] >= xy(*boundaries)[0] or d.textsize(multiline_text, font)[1] >= xy(*boundaries)[1]:
        smaller_font = ImageFont.truetype(font.path, size=font.size - 2)
        wrapped_text(d, text, smaller_font, boundaries, *args, **kwargs)
    else:
        d.multiline_text(text=multiline_text, font=font, *args, **kwargs)
