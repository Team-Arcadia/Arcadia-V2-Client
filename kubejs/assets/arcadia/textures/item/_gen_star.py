"""
Generator for the Stellar Forge item textures at 64x64, in the style of _gen_all.py.
Author: vyrriox

Produces:
  - star_fragment + incomplete_nether_star
  - dragon_shard + incomplete_dragon_egg

Kept apart from _gen_all.py so the 58 existing textures are never rewritten.
"""
from PIL import ImageDraw
import math

from _gen_all import new_img, save, px, blend, draw_crystal, draw_sphere


def star_points(cx, cy, outer, inner, arms=4, rotation=-90.0):
    """Alternating outer/inner vertices of a pointed star."""
    pts = []
    for i in range(arms * 2):
        r = outer if i % 2 == 0 else inner
        a = math.radians(rotation + i * (360.0 / (arms * 2)))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_star_shard(palette, name, glow=True):
    """A broken piece of a nether star: four-pointed star with the east arm chipped off."""
    img = new_img()
    d = ImageDraw.Draw(img)
    base, lt, dk = palette

    pts = star_points(32, 32, 26, 9)
    d.polygon(pts, fill=base, outline=blend(base, (0, 0, 0, 255), 0.55))

    # facets: lit from the upper left, shaded to the lower right
    d.line([(32, 8), (24, 30)], fill=lt, width=2)
    d.line([(32, 8), (40, 30)], fill=blend(lt, base, 0.35), width=1)
    d.line([(10, 32), (30, 26)], fill=blend(lt, base, 0.2), width=1)
    d.line([(32, 56), (26, 38)], fill=dk, width=2)
    d.line([(32, 56), (38, 38)], fill=dk, width=1)

    if glow:
        d.ellipse([28, 28, 36, 36], fill=blend(lt, (255, 255, 255, 255), 0.75))
        for (x, y) in [(32, 12), (14, 32), (32, 52)]:
            px(img, x, y, (255, 255, 255, 255))

    # break: erase the east arm along a jagged edge, then re-darken the exposed rim
    d.polygon([(40, 20), (46, 26), (64, 24), (64, 42), (44, 40), (38, 46)], fill=(0, 0, 0, 0))
    for (x, y) in [(40, 21), (44, 26), (43, 33), (45, 39), (39, 45)]:
        px(img, x, y, dk)
        px(img, x - 1, y, blend(dk, base, 0.5))

    save(img, name)


if __name__ == '__main__':
    # Nether star line
    draw_star_shard(((225, 235, 250, 255), (255, 255, 255, 255), (110, 125, 170, 255)), 'star_fragment')
    draw_sphere(((115, 120, 138, 255), (180, 186, 205, 255), (50, 54, 68, 255)),
                'incomplete_nether_star', symbol='star', glow_inner=False)

    # Dragon egg line
    draw_crystal(((150, 60, 200, 255), (228, 165, 255, 255), (65, 18, 105, 255)),
                 'dragon_shard', tall=True, glow=True)
    draw_sphere(((62, 42, 78, 255), (112, 86, 132, 255), (24, 14, 34, 255)),
                'incomplete_dragon_egg', glow_inner=False)

    print('generated 4 stellar forge textures at 64x64')
