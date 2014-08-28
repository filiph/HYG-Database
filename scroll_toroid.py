from star import Star

def move_on_toroid(x, y, vx, vy, width, height):
    """

    :param x: Starting x.
    :param y: Starting y.
    :param vx: Move by in direction x (can be negative).
    :param vy: Move by in direction y (can be negative).
    :param width: Width of the toroidal grid.
    :param height: Height of the toroidal grid.
    :return: Tuple (x, y) of the moved position.
    """
    nx = x + vx
    ny = y + vy

    def normalize(pos, max):
        return abs(pos % max)
        # if 0 <= pos < max:
        #     return pos
        # elif pos < 0:
        #     while pos < 0:
        #         pos += max
        #     return pos
        # else:
        #     while pos >= max:
        #         pos -= max
        #     return pos

    return normalize(nx, width), normalize(ny, height)


def scroll_stars_by(vx, vy, stars, width, height):
    if vy % 2 != 0:
        print("Warning: moving by an odd number in vertical direction breaks the hex offset.")
    for star in stars:
        assert isinstance(star, Star)
        nx, ny = move_on_toroid(star.X2d, star.Y2d, vx, vy, width, height)
        star.X2d = nx
        star.Y2d = ny

def scroll_stars_to_center(star_in_center, stars, width, height):
    center_x = int(round(width / 2.0))
    center_y = int(round(height / 2.0))
    assert isinstance(star_in_center, Star)
    vx = center_x - star_in_center.X2d
    vy = center_y - star_in_center.Y2d
    scroll_stars_by(vx, vy, stars, width, height)


if __name__ == "__main__":
    print(move_on_toroid(5, 5, 14, 4, 10, 10))