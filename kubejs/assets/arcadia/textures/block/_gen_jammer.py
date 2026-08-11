"""
Generator for the Magnetic Jammer block texture at 64x64.
Author: vyrriox

Dark steel plate, riveted corners, a copper coil around a dead black core, and hazard
stripes on the top and bottom edges.
"""
from PIL import Image, ImageDraw
import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))
SIZE = 64

STEEL = (72, 76, 84, 255)
STEEL_LT = (118, 124, 134, 255)
STEEL_DK = (38, 40, 46, 255)
COPPER = (196, 118, 62, 255)
COPPER_LT = (238, 168, 104, 255)
COPPER_DK = (118, 66, 30, 255)
HAZARD = (214, 176, 54, 255)
CORE = (18, 18, 22, 255)


def main():
    img = Image.new("RGBA", (SIZE, SIZE), STEEL)
    d = ImageDraw.Draw(img)

    # plate bevel
    d.rectangle([0, 0, SIZE - 1, 1], fill=STEEL_LT)
    d.rectangle([0, 0, 1, SIZE - 1], fill=STEEL_LT)
    d.rectangle([0, SIZE - 2, SIZE - 1, SIZE - 1], fill=STEEL_DK)
    d.rectangle([SIZE - 2, 0, SIZE - 1, SIZE - 1], fill=STEEL_DK)

    # hazard stripes, top and bottom bands
    for band in (4, 54):
        d.rectangle([4, band, 59, band + 5], fill=STEEL_DK)
        for x in range(4, 60, 8):
            d.polygon([(x, band + 5), (x + 4, band), (x + 8, band), (x + 4, band + 5)], fill=HAZARD)
        d.rectangle([4, band, 59, band], fill=STEEL_DK)
        d.rectangle([4, band + 5, 59, band + 5], fill=STEEL_DK)

    # coil: three copper rings, lit from the upper left
    for r, w in ((21, 3), (16, 2), (11, 2)):
        d.ellipse([32 - r, 32 - r, 32 + r, 32 + r], outline=COPPER, width=w)
        d.arc([32 - r, 32 - r, 32 + r, 32 + r], 170, 320, fill=COPPER_LT, width=w)
        d.arc([32 - r, 32 - r, 32 + r, 32 + r], 20, 150, fill=COPPER_DK, width=w)

    # dead core
    d.ellipse([25, 25, 39, 39], fill=CORE, outline=STEEL_DK)
    d.line([(28, 28), (36, 36)], fill=COPPER_DK, width=2)
    d.line([(36, 28), (28, 36)], fill=COPPER_DK, width=2)

    # corner rivets
    for (rx, ry) in [(8, 14), (56, 14), (8, 50), (56, 50)]:
        d.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=STEEL_LT, outline=STEEL_DK)
        d.point((rx - 1, ry - 1), fill=(200, 206, 216, 255))

    # brushed metal noise
    for y in range(6, 58, 3):
        for x in range(6, 58, 11):
            if not (20 <= x <= 44 and 12 <= y <= 52):
                img.putpixel((x, y), STEEL_LT if (x + y) % 2 else STEEL_DK)

    img.save(os.path.join(OUT, "magnet_jammer.png"))
    print("generated magnet_jammer.png at 64x64")


if __name__ == '__main__':
    main()
