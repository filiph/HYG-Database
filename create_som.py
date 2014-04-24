

from mvpa2.suite import *
from star import Star

def create_xyz_array(stars):
    assert(isinstance(stars, list))
    coords = []
    for star in stars:
        try:
            assert(isinstance(star, Star))
        except:
            print(star)
            print(star.StarID)
            print(dir(star))
            raise
        coords.append([star.X, star.Y, star.Z])
    return np.array(coords)

def organize(stars, width=1000, height=1000, iters=1000):
    assert(isinstance(stars, list))
    np_coords = create_xyz_array(stars)
    som = SimpleSOMMapper((width, height), iters)
    print("Starting to train...")
    som.train(np_coords)
    print("... done.")
    mapped = som(np_coords)
    for i, m in enumerate(mapped):
        star = stars[i]
        assert(isinstance(star, Star))
        star.X2d = m[0]
        star.Y2d = m[1]
    print("... and written to the given list of stars.")