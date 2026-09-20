"""Generate the Arcadia Minecraft 1.21.1 hotbar skin.

Author: vyrriox

The vanilla sprites keep their original dimensions. Decorative gears are generated
as a separate overlay so they never cover the first or last item slot.
"""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "kubejs/assets/minecraft/textures/gui/sprites/hud"

TRANSPARENT = (0, 0, 0, 0)
BLACK_IRON = (13, 15, 16, 248)
DARK_IRON = (39, 39, 35, 245)
STEEL = (115, 116, 106, 255)
DARK_COPPER = (91, 43, 23, 255)
COPPER = (205, 91, 36, 255)
BRASS = (244, 174, 67, 255)
PALE_BRASS = (255, 224, 143, 255)
AGED_BRASS = (151, 102, 47, 255)
ARCANE_CYAN = (55, 218, 222, 255)


def save(image: Image.Image, name: str) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / name, optimize=True)


def draw_micro_gear(draw: ImageDraw.ImageDraw, center_x: int, center_y: int) -> None:
    """Draw a compact dark-iron cog with substantial copper teeth."""
    tooth_rectangles = (
        (center_x - 1, center_y - 6, center_x + 1, center_y - 4),
        (center_x - 1, center_y + 4, center_x + 1, center_y + 6),
        (center_x - 6, center_y - 1, center_x - 4, center_y + 1),
        (center_x + 4, center_y - 1, center_x + 6, center_y + 1),
        (center_x - 5, center_y - 5, center_x - 3, center_y - 3),
        (center_x + 3, center_y - 5, center_x + 5, center_y - 3),
        (center_x - 5, center_y + 3, center_x - 3, center_y + 5),
        (center_x + 3, center_y + 3, center_x + 5, center_y + 5),
    )
    for tooth in tooth_rectangles:
        draw.rectangle(tooth, fill=COPPER)

    body = (
        (center_x - 2, center_y - 5),
        (center_x + 2, center_y - 5),
        (center_x + 5, center_y - 2),
        (center_x + 5, center_y + 2),
        (center_x + 2, center_y + 5),
        (center_x - 2, center_y + 5),
        (center_x - 5, center_y + 2),
        (center_x - 5, center_y - 2),
    )
    draw.polygon(body, fill=BLACK_IRON)
    draw.line((*body, body[0]), fill=AGED_BRASS, width=1, joint="curve")
    draw.ellipse(
        (center_x - 3, center_y - 3, center_x + 3, center_y + 3),
        fill=DARK_IRON,
        outline=AGED_BRASS,
    )
    draw.rectangle(
        (center_x - 1, center_y - 1, center_x + 1, center_y + 1),
        fill=AGED_BRASS,
    )
    draw.point((center_x, center_y), fill=BLACK_IRON)
    draw.point((center_x - 3, center_y - 3), fill=PALE_BRASS)
    draw.point((center_x + 3, center_y + 2), fill=DARK_COPPER)


def build_hotbar_gear() -> Image.Image:
    image = Image.new("RGBA", (13, 13), TRANSPARENT)
    draw_micro_gear(ImageDraw.Draw(image), 6, 6)
    return image


def build_hotbar() -> Image.Image:
    image = Image.new("RGBA", (182, 22), TRANSPARENT)
    draw = ImageDraw.Draw(image)

    draw.rectangle((1, 0, 180, 21), fill=BLACK_IRON)
    draw.rectangle((0, 1, 181, 20), fill=BLACK_IRON)
    draw.line((2, 1, 179, 1), fill=(154, 145, 119, 255))
    draw.line((2, 2, 179, 2), fill=COPPER)
    draw.line((2, 19, 179, 19), fill=DARK_COPPER)
    draw.line((2, 20, 179, 20), fill=(8, 10, 11, 255))

    for slot in range(9):
        left = 1 + slot * 20
        right = left + 19
        draw.rectangle((left + 2, 3, right - 1, 18), fill=DARK_IRON)
        draw.line((left + 2, 3, right - 1, 3), fill=(75, 70, 58, 255))
        draw.line((left + 2, 4, left + 2, 17), fill=(58, 56, 49, 255))
        draw.line((left + 2, 18, right - 1, 18), fill=(10, 12, 13, 255))
        draw.line((right - 1, 4, right - 1, 17), fill=(20, 21, 20, 255))
        if slot < 8:
            draw.line((right, 3, right, 18), fill=COPPER)
            draw.line((right + 1, 3, right + 1, 18), fill=(54, 35, 24, 255))

    # Symmetrical mechanical end caps keep the bar from looking cut off.
    draw.line((0, 5, 0, 16), fill=(45, 43, 38, 255))
    draw.line((1, 3, 1, 18), fill=STEEL)
    draw.line((2, 2, 2, 19), fill=COPPER)
    draw.line((2, 2, 5, 2), fill=BRASS)
    draw.line((2, 19, 5, 19), fill=DARK_COPPER)
    draw.point((1, 4), fill=PALE_BRASS)
    draw.point((2, 10), fill=(113, 63, 34, 255))

    draw.line((181, 5, 181, 16), fill=(45, 43, 38, 255))
    draw.line((180, 3, 180, 18), fill=STEEL)
    draw.line((179, 2, 179, 19), fill=COPPER)
    draw.line((176, 2, 179, 2), fill=BRASS)
    draw.line((176, 19, 179, 19), fill=DARK_COPPER)
    draw.point((180, 4), fill=PALE_BRASS)
    draw.point((179, 10), fill=(113, 63, 34, 255))

    return image


def build_selection() -> Image.Image:
    image = Image.new("RGBA", (24, 23), TRANSPARENT)
    draw = ImageDraw.Draw(image)

    draw.line((3, 0, 20, 0), fill=STEEL)
    draw.line((3, 22, 20, 22), fill=(30, 27, 23, 255))
    draw.line((0, 3, 0, 19), fill=STEEL)
    draw.line((23, 3, 23, 19), fill=(30, 27, 23, 255))
    draw.line((1, 2, 2, 1), fill=STEEL)
    draw.line((21, 1, 22, 2), fill=(76, 67, 51, 255))
    draw.line((1, 20, 2, 21), fill=(76, 67, 51, 255))
    draw.line((21, 21, 22, 20), fill=(30, 27, 23, 255))

    draw.rectangle((2, 2, 21, 20), outline=DARK_COPPER)
    draw.line((3, 2, 20, 2), fill=BRASS)
    draw.line((2, 3, 2, 19), fill=BRASS)
    draw.line((3, 20, 20, 20), fill=COPPER)
    draw.line((21, 3, 21, 19), fill=COPPER)
    draw.line((8, 21, 15, 21), fill=ARCANE_CYAN)
    return image


def build_offhand(side: str) -> Image.Image:
    image = Image.new("RGBA", (29, 24), TRANSPARENT)
    draw = ImageDraw.Draw(image)
    left = 0 if side == "left" else 7
    right = 21 if side == "left" else 28

    draw.rectangle((left + 1, 1, right - 1, 22), fill=BLACK_IRON)
    draw.rectangle((left, 3, right, 20), fill=BLACK_IRON)
    draw.rectangle((left + 2, 3, right - 2, 20), outline=DARK_COPPER)
    draw.rectangle((left + 3, 4, right - 3, 19), fill=DARK_IRON)
    draw.line((left + 3, 4, right - 3, 4), fill=STEEL)
    draw.line((left + 3, 19, right - 3, 19), fill=(11, 13, 13, 255))
    draw.point((left + 2, 2), fill=BRASS)
    draw.point((right - 2, 21), fill=DARK_COPPER)
    return image


def main() -> None:
    save(build_hotbar(), "hotbar.png")
    save(build_selection(), "hotbar_selection.png")
    save(build_offhand("left"), "hotbar_offhand_left.png")
    save(build_offhand("right"), "hotbar_offhand_right.png")
    save(build_hotbar_gear(), "hotbar_gear.png")
    print("Arcadia HUD generated: hotbar, selection, offhand frames and external gear.")


if __name__ == "__main__":
    main()
