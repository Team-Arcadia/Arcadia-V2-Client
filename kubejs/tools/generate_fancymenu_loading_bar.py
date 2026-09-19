"""Generate the Arcadia FancyMenu/Drippy loading progress textures.

Author: vyrriox
"""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "config/fancymenu/assets/arcadia"


def build_track() -> Image.Image:
    image = Image.new("RGBA", (32, 12), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 0, 29, 11), fill=(13, 15, 16, 246))
    draw.rectangle((0, 2, 31, 9), fill=(13, 15, 16, 246))
    draw.line((3, 1, 28, 1), fill=(126, 123, 108, 255))
    draw.line((1, 3, 1, 8), fill=(91, 88, 78, 255))
    draw.line((3, 10, 28, 10), fill=(70, 33, 20, 255))
    draw.line((30, 3, 30, 8), fill=(70, 33, 20, 255))
    draw.rectangle((3, 3, 28, 8), fill=(20, 22, 21, 255))
    draw.line((4, 3, 27, 3), fill=(47, 45, 38, 255))
    draw.line((4, 8, 27, 8), fill=(8, 10, 11, 255))
    draw.point((2, 2), fill=(239, 169, 65, 255))
    draw.point((29, 2), fill=(180, 76, 29, 255))
    draw.point((2, 9), fill=(180, 76, 29, 255))
    draw.point((29, 9), fill=(91, 43, 23, 255))
    return image


def build_fill() -> Image.Image:
    image = Image.new("RGBA", (32, 12), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((2, 3, 29, 8), fill=(211, 84, 27, 255))
    draw.line((3, 3, 28, 3), fill=(255, 226, 133, 255))
    draw.line((3, 4, 28, 4), fill=(245, 163, 48, 255))
    draw.line((3, 5, 28, 5), fill=(69, 224, 225, 255))
    draw.line((3, 6, 28, 6), fill=(25, 139, 146, 255))
    draw.line((3, 7, 28, 7), fill=(150, 57, 24, 255))
    draw.line((3, 8, 28, 8), fill=(79, 36, 23, 255))
    return image


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    build_track().save(OUTPUT / "loading_progress_track.png", optimize=True)
    build_fill().save(OUTPUT / "loading_progress_fill.png", optimize=True)
    print("Arcadia FancyMenu loading progress textures generated.")


if __name__ == "__main__":
    main()
