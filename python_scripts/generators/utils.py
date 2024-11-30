import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from python_scripts.config import SCALE_FACTOR, Paths


def scaled_tuple(tuple_cm: tuple[float, float]) -> tuple[int, int]:
    return int(SCALE_FACTOR * tuple_cm[0]), int(SCALE_FACTOR * tuple_cm[1])


def _scaled_font(font: ImageFont):
    return font.font_variant(size=2.25 * font.size)


def _get_image(image_path: Path, size: tuple[int, int]) -> Image:
    return Image.open(image_path).convert("RGBA").resize(size)


def extract_colour_from_image(image_path: Path, position: tuple[int, int]):
    image = _get_image(image_path, size=(100, 100))
    return image.getpixel(position)


def init_apply_methods(base_size_cm: tuple[float, float]):
    base_image = Image.new("RGBA", size=scaled_tuple(base_size_cm), color=(0, 0, 0, 0))
    d = ImageDraw.Draw(base_image)

    def apply_image(
            image_path: Path,
            size_cm: tuple[float, float],
            position_cm: tuple[float, float],
    ) -> None:
        size = scaled_tuple(size_cm)
        position = scaled_tuple(position_cm)
        full_image_path = image_path.with_suffix(image_path.suffix + ".png")

        image = _get_image(full_image_path, size)
        base_image.alpha_composite(image, position)

    def apply_text(
            text,
            fill: tuple[int, int, int],
            font: ImageFont,
            size_cm: tuple[float, float],
            position_cm: tuple[float, float],
            anchor: str = "mm",
            align: str = "center",
    ) -> None:
        font = _scaled_font(font)
        width, height = scaled_tuple(size_cm)
        position = scaled_tuple(position_cm)

        keywords_in_text = []

        while True:
            multiline_text_list = [list()]
            for word in str(text).split():
                # Is word a keyword?
                if m := re.search("\[(.+)]", word):
                    keywords_in_text.append(m.group(1))
                    keyword_text = word.replace("_", " ").replace("[", "").replace("]", "").title()
                    word = f"{keyword_text} -·-"
                _, _, text_width, _ = d.textbbox((0, 0), " ".join(multiline_text_list[-1] + [word]), font)
                if text_width >= width:
                    multiline_text_list.append(list())
                multiline_text_list[-1].append(word)

            multiline_text = "\n".join([" ".join(text_list) for text_list in multiline_text_list]).strip()

            _, _, text_width, text_height = d.textbbox((0, 0), multiline_text, font)
            if text_width >= width or text_height >= height:
                font = font.font_variant(size=font.size - 2)
            else:
                break

        d.text(position, multiline_text, fill, font, anchor=anchor, align=align)

        keywords_data = zip(keywords_in_text, get_keyword_image_positions(d, position, multiline_text, font))
        for keyword, image_position in keywords_data:
            image_path = Paths.POKEMON_CARD_ASSETS / "keywords" / f"{keyword}.png"
            image_length = d.textbbox((0, 0), "-·-", font)[2]
            image_size = (image_length, image_length)
            adjusted_image_position = tuple(int(value - image_length / 2.0) for value in image_position)
            image = _get_image(image_path, image_size)
            base_image.alpha_composite(image, adjusted_image_position)

    return base_image, apply_image, apply_text


def get_keyword_image_positions(d, position, multiline_text, font):
    keyword_image_positions = []
    # For simplicity, assuming: anchor="mm", align="center", spacing=4, stroke_width=0
    line_spacing = d.textbbox((0, 0), "A", font)[3] + 4
    lines = multiline_text.split("\n")
    for i, line in enumerate(lines):
        left = d.textbbox(position, line, font, anchor="mm", align="center")[0]
        # Map i=0,1,2,3,4 -> j=-2,-1,0,1,2
        j = i - (len(lines) - 1) / 2.0
        top = position[1] + j * line_spacing

        interpunct_indexes = [index for index, char in enumerate(line) if char == "·"]
        for interpunct_index in interpunct_indexes:
            sub_line = line[:(interpunct_index - 1)]
            sub_line_length = int(d.textlength(sub_line, font) + d.textlength("-·-", font) / 2.0)
            keyword_image_positions.append((left + sub_line_length, top))

    return keyword_image_positions
