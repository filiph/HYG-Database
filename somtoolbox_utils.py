
_XDIM_STRING = r"$XDIM"
_YDIM_STRING = r"$YDIM"
_POSX_STRING = r"$POS_X"
_POSY_STRING = r"$POS_Y"
_MAPPED_VECS_STRING = r"$MAPPED_VECS"
_VAR_STRING = r"$"


def extract_int(line, prepend_string=""):
    assert(isinstance(line, str))
    line = line[len(prepend_string):]
    return int(line)


def read_unit_file(filename):
    xdim = None
    ydim = None
    x = None
    y = None
    grid = None

    def create_grid(width, height):
        return [[[] for i in range(height)] for i in range(width)]

    with open(filename, "r") as f:
        for line in f:
            if line.startswith(_XDIM_STRING):
                assert(xdim is None)
                xdim = extract_int(line, prepend_string=_XDIM_STRING)
                if ydim is not None: grid = create_grid(xdim, ydim)
            elif line.startswith(_YDIM_STRING):
                assert(ydim is None)
                ydim = extract_int(line, prepend_string=_YDIM_STRING)
                if xdim is not None: grid = create_grid(xdim, ydim)
            elif line.startswith(_POSX_STRING):
                assert(xdim is not None and ydim is not None and grid is not None)
                x = extract_int(line, prepend_string=_POSX_STRING)
            elif line.startswith(_POSY_STRING):
                assert(xdim is not None and ydim is not None and grid is not None)
                y = extract_int(line, prepend_string=_POSY_STRING)
            elif line and not line.startswith(_VAR_STRING):
                unit_repr = line.strip()
                print("{} at ({},{})".format(unit_repr, x, y))
                grid[x][y].append(unit_repr)

    return grid


def update_stars(stars, grid):
    """
    Very naive, but also extensible implementation of converting grid (from read_unit_file)
    into a list of [Star].
    :param stars: A list of Star instances.
    :param grid: A matrix.
    :return: None
    """
    for x in range(len(grid)):
        row = grid[x]
        for y in range(len(row)):
                cell = grid[x][y]
                for star_id_str in cell:
                        star_id = int(star_id_str)
                        for star in stars:
                                if star.StarID == star_id:
                                        star.X2d = x
                                        star.Y2d = y
                print("({},{})".format(x,y))


if __name__ == "__main__":
    grid = read_unit_file("SOMToolbox/output/starsom.unit")
    print grid