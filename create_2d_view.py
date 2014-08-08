from star import Star

NUMBER_OF_STARS = 5000
MAGNITUDE = 600  # how big is the map (currently corresponds to the HEIGHT
WIDTH = int(1.41421356 * MAGNITUDE)  # square root of 2 (A4 paper)
HEIGHT = int(1 * MAGNITUDE)
TOROID = True

import pickle
stars_input_filename = "10000_stars_with_simbad_names.pickle"
with open(stars_input_filename, "rb") as f:
    all_stars = pickle.load(f)

stars = all_stars[:NUMBER_OF_STARS]

xmin = min(stars, key=lambda s: s.X).X
ymin = min(stars, key=lambda s: s.Y).Y
zmin = min(stars, key=lambda s: s.Z).Z
xmax = max(stars, key=lambda s: s.X).X
ymax = max(stars, key=lambda s: s.Y).Y
zmax = max(stars, key=lambda s: s.Z).Z

for star in stars:
    assert(isinstance(star, Star))
    star.X2d = int(((star.X - xmin) / float(xmax - xmin)) * WIDTH)
    star.Y2d = int(((star.Y - ymin) / float(ymax - ymin)) * HEIGHT)

import check_variance