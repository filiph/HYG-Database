# Creating a SOM of stars autonomously

NUMBER_OF_STARS = 5000
WIDTH = int(1.41421356 * 100 * 2)  # square root of 2 (A4 paper)
HEIGHT = int(1 * 100 * 2)
ITERS = 1000
RATE = 0.00005

from import_from_hygxyz_csv import *
all_stars = import_from_csv()
stars = all_stars[:NUMBER_OF_STARS]

from create_som import *

kohonen = organize(stars, width=WIDTH, height=HEIGHT, iters=ITERS, learning_rate=RATE)

import check_variance
ZOOM = 2
check_variance.show_map(stars, int(WIDTH / ZOOM), int(HEIGHT / ZOOM), zoom=ZOOM)

print("Distance from Sol to Proxima Centauri is {0:.2f}."
      .format(check_variance.get_distance_to_proxima_centauri(stars)))