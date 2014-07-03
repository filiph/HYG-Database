
import svgwrite
from svgwrite import cm, mm, rgb, deg

from star import Star
from check_variance import dist_3d, dist_2d


# TODO: go hex by hex, paint twin-stars, try to
def create_svg(stars, filename, width, height, show_wormholes=False, show_closest=0, hex=False,
               multiply=10, border_ignore=0):
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
        if star.ProperName:
            dwg.add(dwg.text("{} ({:.1f})".format(star.ProperName, star.Distance),
                             insert=(x, y), fill="blue", font_size=10))
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
    with open("stars1000.pickle", "rb") as f:
        stars = pickle.load(f)
    create_svg(stars, "test.svg", 100, 100)
