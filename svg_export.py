#!/usr/bin/python
# -*- coding: utf-8 -*-

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


def compute_screen_coords(x, y, hex=False, multiply=1, offset_y=0,
                          screen_offset_x=1, screen_offset_y=1):
    """

    :param x: Horizontal coordinate in the viewport.
    :param y: Vertical coordinate in the viewport.
    :param hex: Whether or not this map is a hex map.
    :param multiply: Number of units per tile.
    :param offset_y: The vertical offset of the viewport (used to properly offset rows for hex maps).
    :param screen_offset_x: Number to be added to the resulting coords. Is multipled by `multiply`.
    :param screen_offset_y: Number to be added to the resulting coords. Is multipled by `multiply`.
    :return: None
    """
    hex_offset = 0
    if hex and (y + offset_y) % 2 != 0:
        hex_offset = multiply / 2
    return screen_offset_x * multiply + x * multiply + hex_offset, \
           screen_offset_y * multiply + y * multiply * math.cos(2.0 * math.pi / 6.0 / 2.0)


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


def get_rgb_from_spectrum(star):
    assert isinstance(star, Star)
    spectrum = star.Spectrum
    assert isinstance(spectrum, str)
    if spectrum == "":
        return "#CCCCCC"
    elif "M" in spectrum:
        return "#FF8585"  # red
    elif "K" in spectrum:
        return "#FFA600"  # orange
    elif "G" in spectrum:
        return "#FFEA00"  # yellow
    elif "F" in spectrum:
        return "#FFFF5C"  # yellow-white
    elif "A" in spectrum:
        return "#FFFFFF"  # white
    elif "B" in spectrum:
        return "#7ADEFF"  # blue-white
    elif "O" in spectrum:
        return "#00BFFF"  # blue
    else:
        return "#CCCCCC"

def get_viewport_coords(map_x, map_y, map_width, map_height, viewport_left, viewport_top,
                        viewport_width, viewport_height):
    """
    Gets the relative coordinates in a toroidal grid. (Coordinates wrap around the edges.)

    :param map_x:
    :param map_y:
    :param map_width:
    :param map_height:
    :param viewport_left:
    :param viewport_top:
    :param viewport_width:
    :param viewport_height:
    :return: None if map_x, map_y is not in viewport, a tuple of (x, y) when it is.
    """
    x = map_x - viewport_left
    if 0 <= x < viewport_width:
        pass  # Normal within bounds.
    elif viewport_left < 0 and 0 <= x - map_width < viewport_width:
        x = x - map_width
        pass  # Offset negative and star on the far side.
    elif viewport_left + viewport_width > map_width \
            and 0 <= map_x < viewport_left + viewport_width - map_width:
        x = x + map_width
        pass  # Viewport folding over the far side and star near axis.
    else:
        return None

    y = map_y - viewport_top
    if 0 <= y < viewport_height:
        pass  # Normal within bounds.
    elif viewport_top < 0 and 0 <= y - map_height < viewport_height:
        y = y - map_height
        pass  # Offset negative and star on the far side.
    elif viewport_top + viewport_height > map_height \
            and 0 <= map_y < viewport_top + viewport_height - map_height:
        y = y + map_height
        pass  # Viewport folding over the far side and star near axis.
    else:
        return None

    return x, y


def create_beautiful_svg(stars, filename, width, height, offset_x=0, offset_y=0,
                         map_width=848, map_height=600, header=u"Header"):
    """

    :param stars: A list of Star instances with X2d and Y2d properties set.
    :param filename: Filename of the output SVG file.
    :param width: Width of the viewport.
    :param height: Height of the viewport.
    :param offset_x: X offset of the viewport.
    :param offset_y: Y offset of the viewport.
    :param map_width: The absolute map width (from which we are seeing only width x height viewport).
    :param map_height: The absolute map width (from which we are seeing only width x height viewport).
    :return: None
    """
    multiply = 100
    dwg = svgwrite.Drawing(filename, debug=True)
    dwg.defs.add(dwg.style("""
        circle {

        }

        text {
            fill: black;
            font-family: 'Input Sans Condensed';
            font-size: 150%;
        }

        .header {
            fill: black;
            font-size: 200%;
        }

        .note {
            fill: #cccccc;
        }
    """))
    s_viewbox_width, s_viewbox_height = int((width+1.5) * multiply), \
        int((height + 1.5) *
            multiply * math.cos(2.0 * math.pi / 6.0 / 2.0))
    dwg.viewbox(width=s_viewbox_width, height=s_viewbox_height)
    dwg.add(dwg.rect((0,0), (s_viewbox_width, s_viewbox_height), stroke="blue",
                     fill=svgwrite.rgb(255, 255, 255)))

    grid = create_grid(width, height)

    assert(isinstance(stars, list))
    for star in stars:
        assert(isinstance(star, Star))
        coords = get_viewport_coords(star.X2d, star.Y2d, map_width, map_height, offset_x, offset_y,
                                     width, height)
        if coords:
            x, y, = coords
            grid[x][y].stars.append(star)

    def draw_star(star, sx, sy):
        assert isinstance(star, Star)
        diameter = (star.AbsMag + 12) / 30 * (multiply / 4)
        # TODO: habitable = some other graphic - fill_color = "green" if star.habitable else "white"
        #fill_opacity = "0.5" if star.habitable else "0.0"
        fill_color = get_rgb_from_spectrum(star)
        fill_opacity = "0.5"
        dwg.add(dwg.circle((sx, sy), diameter)
                .stroke(color="black", width=diameter / 10.0)
                .fill(color=fill_color, opacity=fill_opacity))
        if star.habitable:
            # Draw planet.
            dwg.add(dwg.circle((sx + diameter * 1.4, sy), diameter / 5.0)
                .stroke(color="green", width=diameter / 10.0)
                .fill(color="green"))

    def write_name(text, x, y):
        sx, sy = compute_screen_coords(x, y, multiply=multiply, hex=True, offset_y=offset_y)
        sy = sy + multiply / 2.0
        text_el = dwg.text(u"",
                           insert=(sx, sy + multiply / 2.0),
                           text_anchor="middle")
                           #font_size=multiply / 5)
        for i, t in enumerate(text.split("\n")):
            text_el.add(dwg.tspan(u"{}".format(t), x=[sx], y=[sy + i * multiply / 5.0]))

        dwg.add(text_el)

    # Draw the tiles in the background first.
    for x in range(width):
        for y in range(height):
            screen_x, screen_y = compute_screen_coords(x, y, multiply=multiply, hex=True,
                                                       offset_y=offset_y)
            # Draw the tile.
            dwg.add(dwg.circle((screen_x, screen_y), multiply / 2, stroke="#eeeeee")
                    .fill(opacity="0.0").dasharray([31.4/2, 31.4/2]))

    for x in range(width):
        for y in range(height):
            tile = grid[x][y]
            assert(isinstance(tile, Tile))
            screen_x, screen_y = compute_screen_coords(x, y, multiply=multiply, hex=True,
                                                       offset_y=offset_y)
            if len(tile.stars) == 1:
                draw_star(tile.stars[0], screen_x, screen_y)
                write_name(consolidate_star_names(tile.stars), x, y)
            elif len(tile.stars) > 1:
                print("multiple star")
                if len(tile.stars) > 2:
                    print("{}, {}".format(x, y))
                for i, star in enumerate(tile.stars):
                    rad = 2 * math.pi / len(tile.stars) * i - math.pi / 2
                    offset = multiply / 5
                    draw_star(star,
                              screen_x + math.sin(rad) * offset, screen_y + math.cos(rad) * offset)
                write_name(consolidate_star_names(tile.stars), x, y)

    # Create header
    footer_el = dwg.text(u"",
                         insert=(s_viewbox_width - multiply / 2, s_viewbox_height - multiply / 4),
                         text_anchor="end")
    note_el = dwg.tspan(u"A self-organizing map of 5000 known stars closest to Sol. "
                        u"License: Creative Commons Attribution 4.0. "
                        u"Filip Hracek, 2014.")
    note_el['class'] = "note"
    footer_el.add(note_el)
    header_el = dwg.tspan(header, dx=[multiply / 2])
    header_el['class'] = "header"
    footer_el.add(header_el)
    dwg.add(footer_el)

    dwg.save()
    print("SVG export done.")


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


GREEK_ALPHABET = [
    "Alpha",
    "Beta",
    "Gamma",
    "Delta",
    "Epsilon",
    "Zeta",
    "Eta",
    "Theta",
    "Iota",
    "Kappa",
    "Lambda",
    "Mu",
    "Nu",
    "Xi",
    "Omicron",
    "Pi",
    "Rho",
    "Sigma",
    "Tau",
    "Upsilon",
    "Phi",
    "Chi",
    "Psi",
    "Omega"
]

ROMAN_NUMERALS = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
]


if __name__ == "__main__":
    # map_width = 6
    # map_height = 7
    #
    # x, y = get_viewport_coords(5, 1, map_width, map_height, -1, 1, 4, 3)
    # assert(x == 0)
    # assert(y == 0)
    # x, y = get_viewport_coords(1, 5, map_width, map_height, 4, 3, 4, 3)
    # assert(x == 3)
    # assert(y == 2)

    import pickle
    stars = None
    with open("starsom28.pickle", "rb") as f:
        stars = pickle.load(f)
    #
    # height = 50
    # width = int(math.sqrt(2) * height)
    # center_x, center_y = 0, 0  # stars[0].X2d, stars[0].Y2d
    # create_beautiful_svg(stars, "test.svg", width, height,
    #                      offset_x=int(center_x-width/2.0), offset_y=int(center_y-height/2.0))
    map_width = 848
    map_height = 600
    height = 25
    width = int(math.ceil(height * math.sqrt(2)))
    overlap_tile_count = 1
    divisions_count = int(map_height / height)
    for row in range(0, divisions_count):
        for column in range(0, divisions_count):
            name = "{}-{}".format(GREEK_ALPHABET[column], ROMAN_NUMERALS[row])
            print(name)
            viewport_left = column * width - overlap_tile_count
            viewport_top = row * height - overlap_tile_count
            viewport_width = width + 2 * overlap_tile_count
            viewport_height = height + 2 * overlap_tile_count
            print(viewport_left, viewport_left + viewport_width)
            print(viewport_top, viewport_top + viewport_height)
            if not (viewport_left <= stars[0].X2d <= viewport_left + width and
                    viewport_top <= stars[0].Y2d <= viewport_top + height):
                continue
            create_beautiful_svg(stars, "test.svg".format(name), viewport_width, viewport_height,
                                 viewport_left, viewport_top,
                                 header=u"Star Map 2D Sector {}".format(name))
            exit()

