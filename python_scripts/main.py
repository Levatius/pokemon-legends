from pathlib import Path

import numpy as np
import pandas as pd

from python_scripts.config import Paths
from python_scripts.tts_images.deck import generate as generate_deck_images
from python_scripts.tts_images.move_box import generate as generate_move_box_images
from python_scripts.tts_images.move_card import generate as generate_move_card_images
from python_scripts.tts_images.pokemon_card import generate as generate_pokemon_card_images
from python_scripts.tts_objects.pokemon_card import generate as generate_pokemon_card_objects
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

    _ = list(generate_move_box_images(moves_list, outputs_path, overwrite=False))
    move_card_images = list(generate_move_card_images(moves_list, outputs_path, overwrite=False))
    move_card_images_indexed = {image.move.name: image for image in move_card_images}
    pokemon_card_images = list(generate_pokemon_card_images(pokemon_list, outputs_path, overwrite=False))
    pokemon_card_deck_images = list(generate_deck_images(pokemon_card_images, outputs_path / "decks" / "faces", overwrite=False))
    back_images = [move_card_images_indexed[pokemon_card.pokemon.signature_move.name] for pokemon_card in pokemon_card_images]
    back_deck_images = list(generate_deck_images(back_images, outputs_path / "decks" / "backs", overwrite=False))
    deck_images = zip(pokemon_card_deck_images, back_deck_images)

    pokemon_cards = list(generate_pokemon_card_objects(pokemon_list))


if __name__ == "__main__":
    run(outputs_path=Paths.ROOT / "outputs")
