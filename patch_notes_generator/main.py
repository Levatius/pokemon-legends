import pandas as pd
from pathlib import Path

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent


def run():
    old_df_pokemon = pd.read_excel(ROOT_DIR / f'old_sinnoh_cube.xlsx', sheet_name='sinnoh')
    new_df_pokemon = pd.read_excel(ROOT_DIR / f'sinnoh_cube.xlsx', sheet_name='pokemon')

    old_df_moves = pd.read_excel(ROOT_DIR / f'old_sinnoh_cube.xlsx', sheet_name='moves')
    new_df_moves = pd.read_excel(ROOT_DIR / f'sinnoh_cube.xlsx', sheet_name='moves')

    print('**Modified Pokémon**')
    for _, new_row in new_df_pokemon.iterrows():
        if not pd.isnull(new_row.trainer):
            continue

        old_row_df = old_df_pokemon.loc[old_df_pokemon['internal_name'] == new_row.internal_name]
        if not old_row_df.empty:
            old_row = old_row_df.iloc[0]
            if not ((new_row.initiative != old_row.initiative) or (new_row.health != old_row.health) or (new_row.move_name != old_row.move_name)):
                continue

            initiative_text = f'Initiative: {old_row.initiative} → {new_row.initiative} ' if new_row.initiative != old_row.initiative else f''
            health_text = f'Health: {old_row.health} → {new_row.health} ' if new_row.health != old_row.health else f''
            move_text = f'Move: {old_row.move_name} → {new_row.move_name} ' if new_row.move_name != old_row.move_name else f''

            print(f':small_orange_diamond: **{new_row.internal_name}**: {initiative_text}{health_text}{move_text}')
        else:
            initiative_text = f'Initiative: {new_row.initiative} '
            health_text = f'Health: {new_row.health} '
            move_text = f'Move: {new_row.move_name} '
            print(f':small_blue_diamond: **{new_row.internal_name}**: {initiative_text}{health_text}{move_text}')

    print('\n**New Moves**')
    for _, new_row in new_df_moves.iterrows():
        old_row_df = old_df_moves.loc[old_df_moves['move_name'] == new_row.move_name]
        if old_row_df.empty:
            print(f':small_blue_diamond: **{new_row.move_name}**: ({str(new_row.type).capitalize()}) [{new_row.damage}] {new_row.description}')

    print('\n**Modified Moves**')
    for _, new_row in new_df_moves.iterrows():
        old_row_df = old_df_moves.loc[old_df_moves['move_name'] == new_row.move_name]
        if not old_row_df.empty:
            old_row = old_row_df.iloc[0]

            damage_text = f'{old_row.damage} → {new_row.damage}' if new_row.damage != old_row.damage else f'{new_row.damage}'

            if new_row.description != old_row.description:
                print(f':small_orange_diamond: **{new_row.move_name}**: ({str(new_row.type).capitalize()}) [{damage_text}] {new_row.description}')

    print('\n**Removed Moves**')
    for _, old_row in old_df_moves.iterrows():
        new_row_df = new_df_moves.loc[new_df_moves['move_name'] == old_row.move_name]
        if new_row_df.empty:
            print(f':small_red_triangle_down: **{old_row.move_name}**: ({str(old_row.type).capitalize()}) [{old_row.damage}] {old_row.description}')


if __name__ == '__main__':
    run()
