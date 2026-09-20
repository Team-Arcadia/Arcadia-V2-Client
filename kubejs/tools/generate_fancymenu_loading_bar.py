"""Generate the Arcadia FancyMenu/Drippy loading progress textures.

Author: vyrriox
"""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "config/fancymenu/assets/arcadia"


def build_track() -> Image.Image:
    image = Image.new("RGBA", (32, 14), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 0, 29, 13), fill=(15, 11, 8, 252))
    draw.rectangle((0, 2, 31, 11), fill=(15, 11, 8, 252))
    draw.line((3, 1, 28, 1), fill=(139, 91, 39, 255))
    draw.line((1, 3, 1, 10), fill=(101, 55, 26, 255))
    draw.line((30, 3, 30, 10), fill=(79, 38, 20, 255))
    draw.line((3, 12, 28, 12), fill=(62, 29, 18, 255))
    draw.rectangle((3, 3, 28, 10), fill=(25, 19, 14, 255))
    draw.line((4, 3, 27, 3), fill=(72, 47, 27, 255))
    draw.line((4, 10, 27, 10), fill=(7, 7, 6, 255))
    draw.point((2, 2), fill=(224, 151, 61, 255))
    draw.point((29, 2), fill=(170, 91, 35, 255))
    draw.point((2, 11), fill=(145, 69, 29, 255))
    draw.point((29, 11), fill=(80, 37, 20, 255))
    return image


def build_fill() -> Image.Image:
    image = Image.new("RGBA", (32, 14), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 3, 29, 10), fill=(101, 40, 20, 255))
    draw.line((3, 3, 28, 3), fill=(138, 65, 25, 255))
    draw.line((3, 4, 28, 4), fill=(255, 219, 128, 255))
    draw.line((3, 5, 28, 5), fill=(247, 174, 64, 255))
    draw.line((3, 6, 28, 6), fill=(229, 125, 39, 255))
    draw.line((3, 7, 28, 7), fill=(201, 83, 28, 255))
    draw.line((3, 8, 28, 8), fill=(157, 56, 24, 255))
    draw.line((3, 9, 28, 9), fill=(105, 39, 22, 255))
    draw.line((3, 10, 28, 10), fill=(57, 25, 17, 255))
    return image


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_track().save(OUTPUT / "loading_progress_track.png", optimize=True)
    build_fill().save(OUTPUT / "loading_progress_fill.png", optimize=True)
    print("Arcadia FancyMenu loading progress textures generated.")


if __name__ == "__main__":
    main()
