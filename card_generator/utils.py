import pandas as pd

from config import *


def xy(width_cm, height_cm):
    return int(64 * width_cm), int(64 * height_cm)


def pos(x, y):
    return int(512 * x), int(896 * y)


def read_cube(cube_name='sinnoh_cube', sheet_name='sinnoh'):
    df = pd.read_excel(ROOT_DIR / f'{cube_name}.xlsx', sheet_name)
    return df


def get_shiny_name(shiny):
    return 'shiny' if shiny else 'normal'
