
import math

import svgwrite
from svgwrite import cm, mm, rgb, deg

from star import Star
from check_variance import dist_3d, dist_2d


class Tile:
    def __init__(self, x, y):
        self.stars = []
        self.x = x
        self.y = y


def create_grid(width, height):
        return [[Tile(j, i) for i in range(height)] for j in range(width)]


def compute_screen_coords(x, y, hex=False, multiply=1, offset_y=0):
    hex_offset = 0
    if hex and (y + offset_y) % 2 != 0:
        hex_offset = multiply / 2
    return x * multiply + hex_offset, y * multiply * math.cos(2.0 * math.pi / 6.0 / 2.0)


def _same_string_except_last_char(names):
    assert isinstance(names, list)
    assert len(names) > 1
    stub = names[0][:-1]
    for name in names:
        if name[:-1] != stub:
            return False
    return True


def consolidate_star_names(stars):
    assert isinstance(stars, list)
    assert len(stars) > 0
    names = []
    for star in stars:
        if star.ProperName:
            star_name = star.ProperName
        else:
            star_name = star.get_best_human_ident()
        if not star_name in names:  # When there is two stars with duplicate names at one place.
            names.append(star_name)
    if len(names) == 1:
        return names[0]
    else:
        if _same_string_except_last_char(names):
            names.sort()
            name = names[0][:-1]
            appendixes = [n[-1:] for n in names]
            name += "/".join(appendixes)
            print("Same string except last! {}, {}, ... = {}".format(names[0], names[1], name))
            return name
        else:
            return "\n".join(names)


def create_beautiful_svg(stars, filename, width, height, offset_x=0, offset_y=0):
    multiply = 100
    dwg = svgwrite.Drawing(filename, debug=True)
    # dwg.defs.add(dwg.style("""
    #     circle {
    #
    #     }
    #
    #     text {
    #         fill: green;
    #         font-family: 'Comic Sans';
    #     }
    # """))
    viewbox_width, viewbox_height = int((width+1) * multiply), \
                                    int((height + 1) *
                                        multiply * math.cos(2.0 * math.pi / 6.0 / 2.0))
    dwg.viewbox(width=viewbox_width, height=viewbox_height)
    dwg.add(dwg.rect((0,0), (viewbox_width, viewbox_height), stroke="blue",
                     fill=svgwrite.rgb(255, 255, 255)))

    grid = create_grid(width, height)

    assert(isinstance(stars, list))
    for star in [s for s in stars
                 if offset_x <= s.X2d < offset_x + width and offset_y <= s.Y2d < offset_y + height]:
        assert(isinstance(star, Star))
        grid[star.X2d - offset_x][star.Y2d - offset_y].stars.append(star)

    def draw_star(star, sx, sy):
        assert isinstance(star, Star)
        diameter = (star.AbsMag + 12) / 30 * (multiply / 4)
        fill_color = "green" if star.habitable else "white"
        fill_opacity = "0.5" if star.habitable else "0.0"
        dwg.add(dwg.circle((sx, sy), diameter)
                .stroke(color="black", width=diameter / 10.0)
                .fill(color=fill_color, opacity=fill_opacity))

    def write_name(text, x, y):
        sx, sy = compute_screen_coords(x, y, multiply=multiply, hex=True, offset_y=offset_y)
        sy = sy + multiply / 2.0
        text_el = dwg.text(u"",
                           insert=(sx, sy + multiply / 2.0),
                           # size=(multiply, multiply / 2.0),
                           # fill="blue",
                           text_anchor="middle",
                           font_family="Input Sans Condensed",
                           font_size=multiply / 5)
        for i, t in enumerate(text.split("\n")):
            text_el.add(dwg.tspan(u"{}".format(t), x=[sx], y=[sy + i * multiply / 5.0]))

        dwg.add(text_el)

    for x in range(width):
        for y in range(height):
            tile = grid[x][y]
            assert(isinstance(tile, Tile))
            screen_x, screen_y = compute_screen_coords(x, y, multiply=multiply, hex=True,
                                                       offset_y=offset_y)
            # Draw the tile.
            dwg.add(dwg.circle((screen_x, screen_y), multiply / 2, stroke="#eeeeee")
                    .fill(opacity="0.0").dasharray([5, 5]))
            if len(tile.stars) == 1:
                draw_star(tile.stars[0], screen_x, screen_y)
                write_name(consolidate_star_names(tile.stars), x, y)
            elif len(tile.stars) > 1:
                print("multiple star")
                if len(tile.stars) > 2:
                    print("{}, {}".format(x, y))
                for i, star in enumerate(tile.stars):
                    rad = 2 * math.pi / len(tile.stars) * i + math.pi / 2
                    offset = multiply / 5
                    draw_star(star,
                              screen_x + math.sin(rad) * offset, screen_y + math.cos(rad) * offset)
                write_name(consolidate_star_names(tile.stars), x, y)

    dwg.save()
    print("SVG export done.")



# TODO: go hex by hex, paint twin-stars, try to
def create_svg(stars, filename, width, height, show_wormholes=False, show_closest=0, hex=False,
               multiply=10, border_ignore=0, all_names=False):
    assert(isinstance(stars, list))
    if border_ignore > 0:
        min_x = min([star.X2d for star in stars])
        min_y = min([star.Y2d for star in stars])
        max_x = max([star.X2d for star in stars])
        max_y = max([star.Y2d for star in stars])
        stars = [star for star in stars if
                 star.X2d >= min_x + border_ignore and
                 star.Y2d >= min_y + border_ignore and
                 star.X2d <= max_x - border_ignore and
                 star.Y2d <= max_y - border_ignore]

    dwg = svgwrite.Drawing(filename, debug=True)
    dwg.viewbox(width=width * multiply, height=height * multiply)  # A4 landscape
    dwg.add(dwg.rect((0,0), (width * multiply, height * multiply), stroke="blue",
                     fill=svgwrite.rgb(255, 255, 255)))
    for index, star in enumerate(stars):
        assert(isinstance(star, Star))
        x, y = star.coords_2d(multiply=multiply, hex=hex)
        # Lowest AbsMag is -11.06. Highest is 19.63.
        diameter = (star.AbsMag + 12) / 30 * 3
        fill_color = "green" if star.habitable else "white"
        dwg.add(dwg.circle((x, y), diameter, stroke="black").fill(color=fill_color, opacity=0))
        star_name = None
        if star.ProperName:
            star_name = star.ProperName
        elif all_names:
            star_name = star.get_best_human_ident()
        if star_name is not None:
            dwg.add(dwg.text(u"{}".format(star_name),
                             insert=(x, y), fill="blue", font_size=5))
        if show_wormholes:
            for other_star in stars[:index]:
                if star is other_star:
                    pass
                # DIST_3D_TO_2D_RATIO = 40
                # if dist_2d(star, other_star) > dist_3d(star, other_star) * DIST_3D_TO_2D_RATIO:
                if dist_2d(star, other_star) > 30 and dist_3d(star, other_star) < 2:
                    dwg.add(dwg.line((x, y), other_star.coords_2d(multiply=multiply, hex=hex),
                                     stroke="gray"))
                # Red lines for stars that are too close in 2D
                # if dist_2d(star, other_star) < 10 and dist_3d(star, other_star) > 10:
                #     dwg.add(dwg.line((x, y), other_star.coords_2d(multiply=multiply, hex=hex),
                #                      stroke="red"))

        if show_closest > 0:
            other_stars = sorted(stars, key=lambda other_star: dist_3d(star, other_star))
            for i in range(1, show_closest+1):
                other_star = other_stars[i]
                dwg.add(dwg.line((x, y), other_star.coords_2d(multiply=multiply, hex=hex),
                                 stroke="gray"))
    dwg.save()


if __name__ == "__main__":
    import pickle
    stars = None
    with open("starsom28_zoomed_283x200.pickle", "rb") as f:
        stars = pickle.load(f)

    height = 50
    width = int(math.sqrt(2) * height)
    center_x, center_y = stars[0].X2d, stars[0].Y2d
    create_beautiful_svg(stars, "test.svg", width, height,
                         offset_x=int(center_x-width/2.0), offset_y=int(center_y-height/2.0))
