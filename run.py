# Creating a SOM of stars autonomously

NUMBER_OF_STARS = 1000
WIDTH = 141
HEIGHT = 100
ITERS = 10
RATE = 0.0005

from import_from_hygxyz_csv import *
all_stars = import_from_csv()
stars = all_stars[:NUMBER_OF_STARS]

from create_som import *
kohonen = organize(stars, width=WIDTH, height=HEIGHT, iters=ITERS, learning_rate=RATE)

import check_variance
check_variance.show_map(stars, WIDTH / 2, HEIGHT / 2, zoom=2)