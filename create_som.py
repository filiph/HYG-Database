
import datetime
from mvpa2.suite import *
from math import sqrt
from star import Star

def create_xyz_array(stars):
    assert(isinstance(stars, list))
    min_x, min_y, min_z = 0, 0, 0
    max_x, max_y, max_z = 0, 0, 0
    for star in stars:
        if star.X < min_x: min_x = star.X
        if star.Y < min_y: min_y = star.Y
        if star.Z < min_z: min_z = star.Z
        if star.X > max_x: max_x = star.X
        if star.Y > max_y: max_y = star.Y
        if star.Z > max_z: max_z = star.Z
    coords = []
    for star in stars:
        assert(isinstance(star, Star))
        coords.append([
            (star.X - min_x) / (max_x - min_x),
            (star.Y - min_y) / (max_y - min_y),
            (star.Z - min_z) / (max_z - min_z)])
    return np.array(coords)

def organize(stars, width=1000, height=1000, iters=100, learning_rate=0.001, kohonen=None,
             iradius=None, toroid=False):
    assert(isinstance(stars, list))
    np_coords = create_xyz_array(stars)
    if kohonen is not None:
        initialization_func = lambda x: kohonen
    else:
        initialization_func = None

    if toroid:
        # formula stolen from http://stackoverflow.com/a/2123977
        def torus_distance(x, y):
            return sqrt(min(abs(x), width - abs(x))**2 + min(abs(y), height - abs(y))**2)
        distance_metric = torus_distance
    else:
        distance_metric = None
    som = SimpleSOMMapper((width, height), iters, learning_rate=learning_rate,
                          initialization_func=initialization_func, iradius=iradius,
                          distance_metric=distance_metric)
    print("Starting to train...")
    start_time = datetime.datetime.now()
    som.train(np_coords)
    print("... done.")
    mapped = som(np_coords)
    for i, m in enumerate(mapped):
        star = stars[i]
        assert(isinstance(star, Star))
        star.X2d = m[0]
        star.Y2d = m[1]
    print("... and written to the given list of stars.")
    duration = datetime.datetime.now()-start_time
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    print("Execution took {0:.0f}:{1:.0f}:{2:.0f} (hours:minutes:seconds)"
          .format(hours, minutes, seconds))
    return som.K