from pathlib import Path

import numpy as np
import pandas as pd

from python_scripts.config import Paths
from python_scripts.generators.moves import generate_move_boxes, generate_move_cards
from python_scripts.generators.pokemon_cards import generate_pokemon_cards
from python_scripts.models import PokemonDataModel, Pokemon, MovesDataModel, Move


def read_cube(cube_name, sheet_name, data_model=None):
    df = pd.read_excel(Paths.ROOT / f"{cube_name}.xlsx", sheet_name)
    # Validates the data in the sheet against a provided data model (optional)
    if data_model:
        data_model.validate(df, lazy=True, inplace=True)
    # Convert NaN values to None values
    df.replace({np.nan: None}, inplace=True)
    return df


def run(outputs_path: Path):
    pokemon_df = read_cube("sinnoh_cube", "pokemon", data_model=PokemonDataModel)
    pokemon_list = [Pokemon.from_df_row(row) for _, row in pokemon_df.iterrows()]

    moves_df = read_cube("sinnoh_cube", "moves", data_model=MovesDataModel)
    moves_list = [Move.from_df_row(row) for _, row in moves_df.iterrows()]

    generate_move_boxes(moves_list, outputs_path, overwrite=False)
    generate_move_cards(moves_list, outputs_path, overwrite=False)
    generate_pokemon_cards(pokemon_list, outputs_path, overwrite=False)


if __name__ == "__main__":
    run(outputs_path=Paths.ROOT / "outputs")
