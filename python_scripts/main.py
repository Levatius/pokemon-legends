from pathlib import Path

import pandas as pd

from models import Pokemon

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent


def read_cube(cube_name='sinnoh_cube', sheet_name='pokemon'):
    df = pd.read_excel(ROOT_DIR / f'{cube_name}.xlsx', sheet_name)
    return df


def run():
    df = read_cube()

    Pokemon.validate(df, lazy=True)

    pass

    for i, stats in df.iterrows():
        pass


if __name__ == '__main__':
    run()
