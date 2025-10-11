import json

from python_scripts.config import Paths
from python_scripts.models import TTSObject, Pokemon
from python_scripts.tts_objects.deck import Deck


class PokemonCard(TTSObject):
    def __init__(self, pokemon: Pokemon, is_evolution: bool = False):
        self.pokemon = pokemon
        self.is_evolution = is_evolution
        self.states = [] # Populated after init

    @property
    def nickname(self):
        bracket_text = f" ({self.pokemon.description})" if self.description else ""
        return self.pokemon.pokedex_name + bracket_text

    @property
    def description(self):
        if not self.pokemon.trainer:
            return f"The {self.pokemon.classification}"
        return self.pokemon.description

    @property
    def encounter_tier_tag(self):
        tag_map = {
            "starter": "Starter Card",
            "weak": "Weak Encounter Card",
            "moderate": "Moderate Encounter Card",
            "strong": "Strong Encounter Card",
            "legendary": "Legendary Encounter Card",
            "ultra_beast": "Ultra Beast Encounter Card",
            "ultra_burst": "Ultra Burst Encounter Card",
        }
        if self.pokemon.trainer:
            tag_map = {
                "grunt": "Galactic Grunt",
                "commander": f"Galactic {self.pokemon.trainer.title()}",
                "boss": "Galactic Boss"
            }
        return tag_map.get(self.pokemon.encounter_tier)

    @property
    def tags(self):
        return [
            tag for tag in [
                "Pokemon Card",
                self.pokemon.biome,
                self.pokemon.climate,
                self.encounter_tier_tag if not self.is_evolution else "Evolution Card",
            ] if tag
        ]

    @property
    def lua_script(self):
        local_vars = {
            "pokedex_name": self.pokemon.pokedex_name,
            "internal_name": self.pokemon.internal_name,
            "health": self.pokemon.health,
            "initiative": self.pokemon.initiative,
            "types": [type_.title() for type_ in self.pokemon.types],
            "moves": [type_.title() for type_ in self.pokemon.learnable_types],
            "evolve_into": self.pokemon.evolve_into,
            "evolve_cost": self.pokemon.evolve_cost,
            "encounter_tier": self.encounter_tier_tag,
            "move_name": self.pokemon.signature_move.name,
            "move_type": self.pokemon.signature_move.type_.title(),
            "move_attack_strength": self.pokemon.signature_move.attack_strength,
            "move_effect": self.pokemon.signature_move.effect,
        }

        def convert_to_lua_format(py_value):
            """
            Only covering cases needed by the generator, add in more for other types.
            """
            match py_value:
                case int():
                    # No changes
                    return py_value
                case str():
                    # Encase in double quotes
                    return f'"{py_value}"'
                case list():
                    # Lua table syntax
                    return "{" + ",".join([convert_to_lua_format(value) for value in py_value]) + "}"
                case None:
                    return "nil"
                case _:
                    return py_value

        lua_script_lines = [f"{variable} = {convert_to_lua_format(value)}" for variable, value in local_vars.items()]
        return "\n".join(lua_script_lines)

    def get_card_json(self, card_id: int, deck: Deck):
        with open(Paths.POKEMON_CARD_ASSETS / "object_templates" / "card.json") as f:
            card_json = json.load(f)

        card_json["CardID"] = card_id
        card_json["Nickname"] = self.nickname
        card_json["Description"] = self.description
        card_json["Tags"] = self.tags
        card_json["LuaScript"] = self.lua_script
        card_json["CustomDeck"][str(deck.id)] = {
            "FaceURL": deck.face_url,
            "BackURL": deck.back_url,
            "NumWidth": 10,
            "NumHeight": 7,
            "BackIsHidden": True,
            "UniqueBack": True,
            "Type": 0,
        }
        return card_json

def generate(pokemon_list: list[Pokemon]):
    pokemon_cards: list[PokemonCard] = []
    for pokemon in pokemon_list:
        # State is None means the Pokémon has no other states
        # State == 1 means the Pokémon has other states
        if pokemon.state is None or pokemon.state == 1:
            pokemon_cards.append(PokemonCard(pokemon))
        elif pokemon.state >= 1:
            # Add additional states to last Pokémon
            pokemon_cards[-1].states.append(PokemonCard(pokemon))

    pass
