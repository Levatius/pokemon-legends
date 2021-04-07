NORMAL = 'normal'
FIRE = 'fire'
WATER = 'water'
ELECTRIC = 'electric'
GRASS = 'grass'
ICE = 'ice'
FIGHTING = 'fighting'
POISON = 'poison'
GROUND = 'ground'
FLYING = 'flying'
PSYCHIC = 'psychic'
BUG = 'bug'
ROCK = 'rock'
GHOST = 'ghost'
DRAGON = 'dragon'
DARK = 'dark'
STEEL = 'steel'
FAIRY = 'fairy'

WEAK = 2
RESIST = -2
IMMUNE = -4

TYPE_CHART = {
    NORMAL: {ROCK: RESIST, GHOST: IMMUNE, STEEL: RESIST},
    FIRE: {FIRE: RESIST, WATER: RESIST, GRASS: WEAK, ICE: WEAK, BUG: WEAK, ROCK: RESIST, DRAGON: RESIST, STEEL: WEAK},
    WATER: {FIRE: WEAK, WATER: RESIST, GRASS: RESIST, GROUND: WEAK, ROCK: WEAK, DRAGON: RESIST},
    ELECTRIC: {WATER: WEAK, ELECTRIC: RESIST, GRASS: RESIST, GROUND: IMMUNE, FLYING: WEAK, DRAGON: RESIST},
    GRASS: {FIRE: RESIST, WATER: WEAK, GRASS: RESIST, POISON: RESIST, GROUND: WEAK, FLYING: RESIST, BUG: RESIST,
            ROCK: WEAK, DRAGON: RESIST, STEEL: RESIST},
    ICE: {FIRE: RESIST, WATER: RESIST, GRASS: WEAK, ICE: RESIST, GROUND: WEAK, FLYING: WEAK, DRAGON: WEAK,
          STEEL: RESIST},
    FIGHTING: {NORMAL: WEAK, ICE: WEAK, POISON: RESIST, FLYING: RESIST, PSYCHIC: RESIST, BUG: RESIST, ROCK: WEAK,
               GHOST: IMMUNE, DARK: WEAK, STEEL: WEAK, FAIRY: RESIST},
    POISON: {GRASS: WEAK, POISON: RESIST, GROUND: RESIST, ROCK: RESIST},
    GROUND: {FIRE: WEAK, ELECTRIC: WEAK, GRASS: RESIST, POISON: WEAK, FLYING: IMMUNE, BUG: RESIST, ROCK: WEAK,
             STEEL: WEAK},
    FLYING: {ELECTRIC: RESIST, GRASS: WEAK, FIGHTING: WEAK, BUG: WEAK, ROCK: RESIST, STEEL: RESIST},
    PSYCHIC: {FIGHTING: WEAK, POISON: WEAK, PSYCHIC: RESIST, DARK: IMMUNE, STEEL: RESIST},
    BUG: {FIRE: RESIST, GRASS: WEAK, FIGHTING: RESIST, POISON: RESIST, FLYING: RESIST, PSYCHIC: WEAK, GHOST: RESIST,
          DARK: WEAK, STEEL: RESIST, FAIRY: RESIST},
    ROCK: {FIRE: WEAK, ICE: WEAK, FIGHTING: RESIST, GROUND: RESIST, FLYING: WEAK, BUG: WEAK, STEEL: RESIST},
    GHOST: {NORMAL: IMMUNE, PSYCHIC: WEAK, GHOST: WEAK, DARK: RESIST},
    DRAGON: {DRAGON: WEAK, STEEL: RESIST, FAIRY: IMMUNE},
    DARK: {FIGHTING: RESIST, PSYCHIC: WEAK, DARK: RESIST, FAIRY: RESIST},
    STEEL: {FIRE: RESIST, WATER: RESIST, GRASS: RESIST, ICE: WEAK, ROCK: WEAK, STEEL: RESIST, FAIRY: WEAK},
    FAIRY: {FIRE: RESIST, FIGHTING: WEAK, POISON: RESIST, DRAGON: WEAK, DARK: WEAK, STEEL: RESIST}
}