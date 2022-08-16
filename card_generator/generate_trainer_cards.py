import json
from PIL import Image, ImageDraw

from config import *
from utils import xy, text_font, title_font, read_cube, get_img, wrapped_text

TRAINER_CARD_ASSETS = ROOT_DIR / 'assets' / '2_expansion_trainer_cards'

QUALITY_BRONZE = 'bronze'
QUALITY_SILVER = 'silver'
QUALITY_GOLD = 'gold'
QUALITIES = QUALITY_BRONZE, QUALITY_SILVER, QUALITY_GOLD


class TrainerCard:
    def __init__(self, data, quality):
        self.data = data
        self.quality = quality

    def _create_base(self):
        return get_img(TRAINER_CARD_ASSETS / self.quality / 'base.png', xy(28, 16))

    def _add_ability_texts(self, img):
        d = ImageDraw.Draw(img)
        # Ability 1
        wrapped_text(d, self.data.ability_1_name, title_font(24), boundaries=(8.5, 1), xy=xy(5.25, 4),
                     fill=WHITE_COLOUR, anchor='mm', align='center')
        wrapped_text(d, self.data.ability_1_description, text_font(24), boundaries=(8.5, 7.5), xy=xy(5.25, 5),
                     fill=WHITE_COLOUR, anchor='ma', align='center')
        # Ability 2
        wrapped_text(d, self.data.ability_2_name, title_font(24), boundaries=(8.5, 1), xy=xy(14.75, 4),
                     fill=WHITE_COLOUR, anchor='mm', align='center')
        wrapped_text(d, self.data.ability_2_description, text_font(24), boundaries=(8.5, 7.5), xy=xy(14.75, 5),
                     fill=WHITE_COLOUR, anchor='ma', align='center')

    def _add_locks(self, img):
        if self.quality == QUALITY_BRONZE:
            locked_blue_img = get_img(TRAINER_CARD_ASSETS / 'locked_blue.png', xy(9.5, 10))
            img.paste(locked_blue_img, xy(0.5, 3), locked_blue_img)
        if self.quality in (QUALITY_BRONZE, QUALITY_SILVER):
            locked_red_img = get_img(TRAINER_CARD_ASSETS / 'locked_red.png', xy(9.5, 10))
            img.paste(locked_red_img, xy(10, 3), locked_red_img)

    def _add_trainer(self, img):
        trainer_img = get_img(TRAINER_CARD_ASSETS / 'trainers' / f'{self.data.trainer_class}.png', xy(27, 13.5))
        img.paste(trainer_img, xy(10, 0.5), trainer_img)

    def _add_bottom_bar(self, img):
        bottom_bar_img = get_img(TRAINER_CARD_ASSETS / self.quality / 'bottom_bar.png', xy(28, 1.5))
        img.paste(bottom_bar_img, xy(0, 13.25), bottom_bar_img)

    def _add_trainer_class(self, img):
        d = ImageDraw.Draw(img)
        d.text(xy(25.75, 14), self.data.trainer_class, fill=WHITE_COLOUR, font=title_font(24), anchor='rm')

    def generate(self):
        img = self._create_base()
        self._add_ability_texts(img)
        self._add_locks(img)
        self._add_trainer(img)
        self._add_bottom_bar(img)
        self._add_trainer_class(img)
        return img

    @property
    def id(self):
        return (QUALITIES.index(self.quality) + 1) * 100 + self.data.name

    def get_json(self, deck_urls, back_urls):
        with open(TRAINER_CARD_ASSETS / 'object_templates' / 'card.json') as f:
            card_json = json.load(f)

        card_json['CardID'] = self.id
        card_json['Nickname'] = f'{self.data.trainer_class} ({self.quality.capitalize()})'
        card_json['Description'] = 'Trainer Card'
        card_json['CustomDeck'][QUALITIES.index(self.quality) + 1] = {
            'FaceURL': deck_urls[self.quality],
            'BackURL': back_urls[self.quality],
            'NumWidth': 10,
            'NumHeight': 7,
            'BackIsHidden': True,
            'UniqueBack': False,
            'Type': 0
        }
        return card_json


def generate_cards(overwrite=False):
    df = read_cube(sheet_name='trainer_cards')
    for quality in QUALITIES:
        output_dir = TRAINER_CARD_ASSETS / '_output' / 'card_fronts' / quality
        output_dir.mkdir(parents=True, exist_ok=True)

        for _, data in df.iterrows():
            output_path = output_dir / f'{data.trainer_class}.png'
            if output_path.is_file() and not overwrite:
                continue

            trainer_card = TrainerCard(data, quality)
            trainer_card_img = trainer_card.generate()
            trainer_card_img.save(output_path)


def generate_decks():
    def pos(x, y):
        return int(896 * x), int(512 * y)

    df = read_cube(sheet_name='trainer_cards')

    for quality in QUALITIES:
        deck_img = Image.new('RGBA', pos(10, 7))
        output_dir = TRAINER_CARD_ASSETS / '_output' / 'decks'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f'{quality}_deck.png'

        for i, data in df.iterrows():
            card_path = TRAINER_CARD_ASSETS / '_output' / 'card_fronts' / quality / f'{data.trainer_class}.png'
            img = get_img(card_path, xy(14, 8))
            deck_img.paste(img, pos(i % 10, (i // 10) % 7), img)

        deck_img.save(output_path)


#
# Generate Deck Object
#

def generate_deck_object():
    df = read_cube(sheet_name='trainer_cards')

    with open(TRAINER_CARD_ASSETS / 'object_templates' / 'deck.json') as f:
        deck_json = json.load(f)

    deck_urls = {}
    back_urls = {}
    for i, quality in enumerate(QUALITIES):
        deck_urls[quality] = input(f'Enter the Cloud URL for {quality}_deck:\n')
        back_urls[quality] = input(f'Enter the Cloud URL for {quality}_back:\n')

        deck_json['ObjectStates'][0]['CustomDeck'][str(i + 1)] = {
            'NumWidth': 10,
            'NumHeight': 7,
            'BackIsHidden': True,
            'UniqueBack': False,
            'Type': 0
        }
        deck_json['ObjectStates'][0]['CustomDeck'][str(i + 1)]['FaceURL'] = deck_urls[quality]
        deck_json['ObjectStates'][0]['CustomDeck'][str(i + 1)]['BackURL'] = back_urls[quality]

    for _, data in df.iterrows():
        for i, quality in enumerate(QUALITIES):
            trainer_card = TrainerCard(data, quality)
            trainer_card_json = trainer_card.get_json(deck_urls, back_urls)
            if quality == QUALITY_BRONZE:
                deck_json['ObjectStates'][0]['DeckIDs'].append(trainer_card.id)
                deck_json['ObjectStates'][0]['ContainedObjects'].append(trainer_card_json)
            else:
                deck_json['ObjectStates'][0]['ContainedObjects'][-1]['States'][i + 1] = trainer_card_json

    output_dir = TRAINER_CARD_ASSETS / '_output' / 'deck_object'
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / 'trainer_card_deck.json', 'w') as f:
        json.dump(deck_json, f)


if __name__ == '__main__':
    generate_cards(overwrite=False)
    generate_decks()
    generate_deck_object()
