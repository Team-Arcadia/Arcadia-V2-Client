"""Build the Arcadia skin for FTB Library and FTB Quests.

Author: vyrriox

The script preserves upstream texture dimensions and icon silhouettes while
applying Arcadia's restrained iron, brass, copper, walnut and arcane-cyan
palette. Run it from the instance root after extracting the matching FTB GUI
textures into ``work/ftb_gui_originals``.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "work" / "ftb_gui_originals" / "assets"
ASSETS = ROOT / "kubejs" / "assets"

IRON_DARK = (18, 24, 29, 255)
IRON = (36, 47, 55, 255)
IRON_LIGHT = (68, 82, 88, 255)
STEEL = (115, 119, 113, 255)
BRASS_DARK = (91, 58, 27, 255)
BRASS = (177, 119, 48, 255)
BRASS_LIGHT = (235, 183, 91, 255)
COPPER = (165, 74, 43, 255)
CYAN_DARK = (15, 91, 101, 255)
CYAN = (48, 210, 220, 255)
WOOD_DARK = (52, 31, 22, 255)
WOOD = (91, 53, 31, 255)


def save(image: Image.Image, namespace: str, name: str) -> None:
    destination = ASSETS / namespace / "textures" / "gui" / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, optimize=True)


def build_background() -> Image.Image:
    image = Image.new("RGBA", (16, 16), IRON_DARK)
    draw = ImageDraw.Draw(image)
    for y in range(16):
        for x in range(16):
            noise = ((x * 11 + y * 7 + x * y) % 5) - 2
            draw.point((x, y), fill=(22 + noise, 29 + noise, 34 + noise, 255))
    draw.line((0, 0, 15, 0), fill=(45, 56, 61, 255))
    draw.line((0, 0, 0, 15), fill=(39, 49, 55, 255))
    draw.line((0, 15, 15, 15), fill=(12, 17, 21, 255))
    draw.line((15, 0, 15, 15), fill=(12, 17, 21, 255))
    draw.point((1, 1), fill=(68, 72, 69, 255))
    draw.point((14, 14), fill=(9, 13, 16, 255))
    return image


def build_background_squares() -> Image.Image:
    tile = build_background()
    image = Image.new("RGBA", (256, 256))
    for y in range(0, 256, 16):
        for x in range(0, 256, 16):
            image.alpha_composite(tile, (x, y))
    draw = ImageDraw.Draw(image)
    for value in range(0, 256, 64):
        draw.line((value, 0, value, 255), fill=(115, 76, 34, 90))
        draw.line((0, value, 255, value), fill=(115, 76, 34, 90))
    return image


def build_button(state: str) -> Image.Image:
    image = Image.new("RGBA", (200, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    disabled = state == "disabled"
    hovered = state == "hovered"

    outer = (38, 27, 19, 255) if not disabled else (31, 34, 35, 255)
    rim = CYAN if hovered else ((116, 75, 31, 255) if not disabled else (62, 67, 66, 255))
    fill = (63, 42, 29, 255) if not disabled else (40, 45, 46, 255)
    fill_alt = (76, 48, 30, 255) if not disabled else (45, 49, 49, 255)

    draw.rectangle((2, 0, 197, 19), fill=outer)
    draw.rectangle((0, 2, 199, 17), fill=outer)
    draw.rectangle((2, 2, 197, 17), fill=rim)
    draw.rectangle((3, 3, 196, 16), fill=IRON_DARK)
    draw.rectangle((5, 4, 194, 15), fill=fill)
    draw.line((6, 5, 193, 5), fill=fill_alt)
    draw.line((6, 14, 193, 14), fill=WOOD_DARK if not disabled else (29, 33, 34, 255))

    for x in (4, 195):
        draw.point((x, 4), fill=BRASS_LIGHT if not disabled else STEEL)
        draw.point((x, 15), fill=BRASS_DARK if not disabled else IRON_LIGHT)
    if hovered:
        draw.line((8, 16, 191, 16), fill=CYAN_DARK)
        draw.point((1, 9), fill=CYAN)
        draw.point((198, 9), fill=CYAN)
    return image


def recolor_icon(source: Path, accent: bool) -> Image.Image:
    image = Image.open(source).convert("RGBA")
    output = Image.new("RGBA", image.size, (0, 0, 0, 0))
    source_pixels = image.load()
    output_pixels = output.load()

    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = source_pixels[x, y]
            luminance = (red * 54 + green * 183 + blue * 19) // 256
            if alpha == 0:
                continue
            if luminance < 8 and source.suffix.lower() == ".png":
                output_pixels[x, y] = (8, 12, 15, alpha)
            elif accent:
                if luminance < 80:
                    output_pixels[x, y] = (*CYAN_DARK[:3], alpha)
                elif luminance < 180:
                    output_pixels[x, y] = (31, 143, 153, alpha)
                else:
                    output_pixels[x, y] = (*CYAN[:3], alpha)
            else:
                if luminance < 70:
                    output_pixels[x, y] = (*BRASS_DARK[:3], alpha)
                elif luminance < 170:
                    output_pixels[x, y] = (*BRASS[:3], alpha)
                else:
                    output_pixels[x, y] = (*BRASS_LIGHT[:3], alpha)
    return output


def main() -> None:
    save(build_background(), "ftblibrary", "background.png")
    save(build_background_squares(), "ftblibrary", "background_squares.png")
    save(build_button("normal"), "ftblibrary", "nord_button.png")
    save(build_button("hovered"), "ftblibrary", "nord_button_hovered.png")
    save(build_button("disabled"), "ftblibrary", "nord_button_disabled.png")

    quest_source = SOURCE / "ftbquests" / "textures" / "gui"
    accent_icons = {
        "arrow_collapsed.png",
        "arrow_expanded.png",
        "arrow_left.png",
        "arrow_right.png",
        "chain_link.png",
        "collect_rewards.png",
        "dependency.png",
        "link.png",
        "pin.png",
        "search.png",
    }
    for source in sorted(quest_source.rglob("*.png")):
        relative = source.relative_to(quest_source)
        save(recolor_icon(source, source.name in accent_icons), "ftbquests", relative.as_posix())

    print("Arcadia FTB GUI skin generated: 5 library textures and 27 quest textures.")


if __name__ == "__main__":
    main()
