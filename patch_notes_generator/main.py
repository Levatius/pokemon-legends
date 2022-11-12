import pandas as pd
from pathlib import Path

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent

# def get_pokemon_name(df):
#     return df[]


def run():
    old_df_pokemon = pd.read_excel(ROOT_DIR / f'old_sinnoh_cube.xlsx', sheet_name='pokemon')
    new_df_pokemon = pd.read_excel(ROOT_DIR / f'sinnoh_cube.xlsx', sheet_name='pokemon')

    old_df_moves = pd.read_excel(ROOT_DIR / f'old_sinnoh_cube.xlsx', sheet_name='moves')
    new_df_moves = pd.read_excel(ROOT_DIR / f'sinnoh_cube.xlsx', sheet_name='moves')

    old_df_trainer_cards = pd.read_excel(ROOT_DIR / f'old_sinnoh_cube.xlsx', sheet_name='trainer_cards')
    new_df_trainer_cards = pd.read_excel(ROOT_DIR / f'sinnoh_cube.xlsx', sheet_name='trainer_cards')

    print('**New Pokémon**')
    for _, new_row in new_df_pokemon.iterrows():
        if not pd.isnull(new_row.trainer):
            continue

        old_row_df = old_df_pokemon.loc[old_df_pokemon.internal_name == new_row.internal_name]
        if not old_row_df.empty:
            continue

        health_text = f':attr_health:: {new_row.health}'
        initiative_text = f':attr_initiative:: {new_row.initiative}'
        move_text = f':crossed_swords:: {new_row.move_name}'

        texts = ', '.join([text for text in [health_text, initiative_text, move_text] if text])
        print(f':small_blue_diamond: **{new_row.internal_name}**: {texts}')

    print('\n**Modified Pokémon**')
    for _, new_row in new_df_pokemon.iterrows():
        if not pd.isnull(new_row.trainer):
            continue

        old_row_match_condition = (old_df_pokemon.internal_name == new_row.internal_name) & \
                                  (old_df_pokemon.pokedex_number == new_row.pokedex_number)
        old_row_df = old_df_pokemon.loc[old_row_match_condition]
        if old_row_df.empty:
            continue

        old_row = old_row_df.iloc[0]

        texts = []
        if new_row.health != old_row.health:
            health_text = f':attr_health:: {old_row.health} → {new_row.health}'
            texts.append(health_text)
        if new_row.initiative != old_row.initiative:
            initiative_text = f':attr_initiative:: {old_row.initiative} → {new_row.initiative}'
            texts.append(initiative_text)
        if new_row.move_name != old_row.move_name:
            move_text = f':crossed_swords:: {old_row.move_name} → {new_row.move_name}'
            texts.append(move_text)

        if not texts:
            continue
        texts = ', '.join(texts)
        pokemon_description = '' if pd.isnull(new_row.description) else f' ({new_row.description})'
        print(f':small_orange_diamond: **{new_row.pokedex_name}{pokemon_description}**: {texts}')

    print('\n**New Moves**')
    for _, new_row in new_df_moves.iterrows():
        old_row_df = old_df_moves.loc[old_df_moves['move_name'] == new_row.move_name]
        if old_row_df.empty:
            print(
                f':small_blue_diamond: **{new_row.move_name}**: ({str(new_row.move_type).capitalize()}) [{new_row.move_attack_strength}] {new_row.move_effect}')

    print('\n**Modified Moves**')
    for _, new_row in new_df_moves.iterrows():
        old_row_df = old_df_moves.loc[old_df_moves['move_name'] == new_row.move_name]
        if not old_row_df.empty:
            old_row = old_row_df.iloc[0]

            damage_text = f'{old_row.move_attack_strength} → {new_row.move_attack_strength}' if new_row.move_attack_strength != old_row.move_attack_strength else f'{new_row.move_attack_strength}'
            description_text = new_row.move_effect if new_row.move_effect != old_row.move_effect else ''

            # v1.4a Language Adjustments
            if '1 or more' in old_row.move_effect and 'any' in new_row.move_effect:
                continue
            elif 'Use a second' in old_row.move_effect and 'The user may use a second' in new_row.move_effect:
                continue

            if new_row.move_attack_strength != old_row.move_attack_strength or new_row.move_effect != old_row.move_effect:
                print(
                    f':small_orange_diamond: **{new_row.move_name}**: ({str(new_row.move_type).capitalize()}) [{damage_text}] {description_text}')

    print('\n**Removed Moves**')
    for _, old_row in old_df_moves.iterrows():
        new_row_df = new_df_moves.loc[new_df_moves['move_name'] == old_row.move_name]
        if new_row_df.empty:
            print(
                f':small_red_triangle_down: **{old_row.move_name}**: ({str(old_row.move_type).capitalize()}) [{old_row.move_attack_strength}] {old_row.move_effect}')


    print('\n**Modified Trainer Cards**')
    for _, new_row in new_df_trainer_cards.iterrows():
        old_row_df = old_df_trainer_cards.loc[old_df_trainer_cards['trainer_class'] == new_row.trainer_class]
        if not old_row_df.empty:
            old_row = old_row_df.iloc[0]

            if new_row.ability_1_description != old_row.ability_1_description or new_row.ability_2_description != old_row.ability_2_description:
                print(f':small_orange_diamond: **{new_row.trainer_class}**')



if __name__ == '__main__':
    run()
