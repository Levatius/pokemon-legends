# Pokémon: Legends of Sinnoh

- `assests/`: Contains all the assets I have created for the game. You can add new assets here if you want to change how your custom cards look.

- `requirements.txt`: You need a Python environment with these packages installed to use the card generator.
- `sinnoh_cube.xlsx`: Contains the full database of Pokémon and moves.
- `card_generator/main.py`: Generates the Pokémon cards. After it finishes running, you will get some JSON files in `card_generator/output/deck_objects/` that you can add to your TTS saved objects folder to import directly into TTS.

- `patch_notes_generator/`: Ignore this, used for creating the changelog.
- `tabletop_model_bootstrap/`: Ignore this, used for preloading the Pokémon models to avoid certain TTS bugs.

- `tabletop_src/`: Contains all the scripts for the game, forgive the untidiness, Lua is not my first choice of language.
