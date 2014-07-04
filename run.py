# Creating a SOM of stars autonomously

REFRESH_STARS_FROM_CSV = False

NUMBER_OF_STARS = 500
MAGNITUDE = 20  # how big is the map (currently corresponds to the HEIGHT
WIDTH = int(1.41421356 * MAGNITUDE)  # square root of 2 (A4 paper)
HEIGHT = int(1 * MAGNITUDE)
TOROID = True
ITERS = 400
RATE = 0.001


import pickle

if REFRESH_STARS_FROM_CSV:
    from import_from_hygxyz_csv import *
    all_stars = import_from_csv()
else:
    print("Loading stars from pickle.")
    with open("all_stars.pickle", "rb") as f:
        all_stars = pickle.load(f)

stars = all_stars[:NUMBER_OF_STARS]

from create_som import *
# TODO: start many SOMs with same (or similar) parameters, then we can continue with the best one
kohonen = organize(stars, width=WIDTH, height=HEIGHT, iters=ITERS, learning_rate=RATE,
                   toroid=TOROID)

import check_variance
ZOOM = 2
check_variance.show_map(stars, int(WIDTH / ZOOM), int(HEIGHT / ZOOM), zoom=ZOOM)

print("Distance from Sol to Proxima Centauri is {0:.2f}."
      .format(check_variance.get_distance_to_proxima_centauri(stars)))

filename = "{0}stars-{1}x{2}-{3}iters-{4}rate".format(NUMBER_OF_STARS, WIDTH, HEIGHT, ITERS,
                                                      RATE)

print("Saving as {0}.pickle.".format(filename))
with open("{0}.pickle".format(filename), "wb") as f:
    pickle.dump(stars, f, pickle.HIGHEST_PROTOCOL)

import svg_export
print("Saving as {0}-control.svg.".format(filename))
svg_export.create_svg(stars, "{0}-control.svg".format(filename), WIDTH, HEIGHT, show_closest=2)
print("Saving as {0}-hex.svg.".format(filename))
svg_export.create_svg(stars, "{0}-hex.svg".format(filename), WIDTH, HEIGHT, hex=True,
                      border_ignore=int(WIDTH / 20))