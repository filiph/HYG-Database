from math import sqrt
from star import Star
from random import Random
import numpy as np

import toroidsom

def dist_3d(a, b):
    assert(isinstance(a, Star))
    assert(isinstance(b, Star))
    return sqrt((a.X-b.X) ** 2 + (a.Y-b.Y) ** 2 + (a.Z-b.Z) ** 2)


def dist_2d(a, b):
    assert(isinstance(a, Star))
    assert(isinstance(b, Star))
    return sqrt((a.X2d-b.X2d) ** 2 + (a.Y2d-b.Y2d) ** 2)


def get_differences(stars, nsamples=None, toroid=False):
    """
    Takes 3 stars A, B and C, and computes 1) the relative distance of A-B to B-C in 3D space, and
    2) the relative distance of A-B to B-C in 2D space.

    Does this [nsamples] times for random 3 stars.

    Returns an array of differences.
    """
    if nsamples is None:
        nsamples = len(stars)
    random = Random()

    if toroid:
        width = 0
        height = 0
        for star in stars:
            assert(isinstance(star, Star))
            width = max(width, star.X2d)
            height = max(height, star.Y2d)

    differences = []
    for i in range(nsamples):
        a = random.choice(stars)
        assert(isinstance(a, Star))
        b = random.choice(stars)
        assert(isinstance(b, Star))
        c = random.choice(stars)
        assert(isinstance(c, Star))

        a_b_distance_3d = dist_3d(a, b)
        b_c_distance_3d = dist_3d(b, c)

        if not toroid:
            a_b_distance_2d = dist_2d(a, b)
            b_c_distance_2d = dist_2d(b, c)
        else:
            a_b_distance_2d = toroidsom.ToroidSOMMapper.get_toroid_distance(
                a.X2d, a.Y2d, b.X2d, b.Y2d, width, height)
            b_c_distance_2d = toroidsom.ToroidSOMMapper.get_toroid_distance(
                b.X2d, b.Y2d, c.X2d, c.Y2d, width, height)

        if b_c_distance_2d == 0 or b_c_distance_3d == 0:
            continue

        differences.append((a_b_distance_3d/b_c_distance_3d) - (a_b_distance_2d/b_c_distance_2d))
    return differences


def compute_average_difference(differences):
    abs_sum = 0
    for v in differences:
        abs_sum += abs(v)
    return abs_sum / len(differences)


def get_percent_below_diff(differences, threshold=0.5):
    n = 0
    for v in differences:
        if abs(v) < threshold:
            n += 1
    return float(n) / float(len(differences))


def compute_stats(stars, nsamples=None, toroid=False):
    differences = get_differences(stars, nsamples=nsamples, toroid=toroid)
    narray = np.absolute(np.array(differences))
    mean = np.mean(narray)
    median = np.median(narray)
    std = np.std(narray)
    histogram = np.histogram(narray, range=(0, 1), density=True)
    return mean, median, std, histogram


def print_stats(stars, nsamples=None, toroid=False):
    mean, median, std, histogram = compute_stats(stars, nsamples=nsamples, toroid=toroid)
    print("Mean:\t{}\nMedian:\t{}\nStdDev:\t{}\n".format(mean, median, std))
    print("Histogram:\n")
    hist, bin_edges = histogram
    for i, bar in enumerate(hist):
        print("{:>16} : {}".format(bin_edges[i], "*" * int(bar*20)))


def show_map(stars, width, height, zoom=1):
    assert(isinstance(stars, list))
    print_sol = stars[0].StarID == 0
    print_proxima = stars[1].ProperName == "Proxima Centauri"
    print("_" * int(width/zoom))
    for j in range(height):
        y_min = j * zoom
        y_max = (j + 1) * zoom - 1
        line = ""
        for i in range(width):
            x_min = i * zoom
            x_max = (i + 1) * zoom - 1
            if print_sol and x_min <= stars[0].X2d <= x_max and y_min <= stars[0].Y2d <= y_max:
                line += "*"
                continue
            if print_proxima and x_min <= stars[1].X2d <= x_max and y_min <= stars[1].Y2d <= y_max:
                line += "P"
                continue
            stars_present = 0
            for s in stars:
                if x_min <= s.X2d <= x_max and y_min <= s.Y2d <= y_max:
                    stars_present += 1
                if stars_present >= 9:
                    break
            line += str(stars_present) if stars_present > 0 else " "
        print(line)


def get_distance_to_proxima_centauri(stars):
    assert(isinstance(stars, list))
    sol = stars[0]
    proxima = stars[1]
    assert(isinstance(sol, Star))
    assert(isinstance(proxima, Star))
    return sqrt((sol.X2d - proxima.X2d)**2 + (sol.Y2d - proxima.Y2d)**2)