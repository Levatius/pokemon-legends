from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).parent

sinnoh_cube = pd.read_excel(ROOT_DIR / 'sinnoh_cube.xlsx', sheet_name='sinnoh')