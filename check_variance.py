from math import sqrt
from star import Star
from random import Random

def dist_3d(a, b):
    assert(isinstance(a, Star))
    assert(isinstance(b, Star))
    return sqrt((a.X-b.X) ** 2 + (a.Y-b.Y) ** 2 + (a.Z-b.Z) ** 2)

def dist_2d(a, b):
    assert(isinstance(a, Star))
    assert(isinstance(b, Star))
    return sqrt((a.X2d-b.X2d) ** 2 + (a.Y2d-b.Y2d) ** 2)

def get_variances(stars, nsamples=None):
    if nsamples == None:
        nsamples = len(stars)
    random = Random()
    variances = []
    for i in range(nsamples):
        a = random.choice(stars)
        assert(isinstance(a, Star))
        b = random.choice(stars)
        assert(isinstance(b, Star))
        c = random.choice(stars)
        assert(isinstance(c, Star))

        a_b_distance_3d = dist_3d(a, b)
        b_c_distance_3d = dist_3d(b, c)

        a_b_distance_2d = dist_2d(a, b)
        b_c_distance_2d = dist_2d(b, c)

        try:
            variances.append((a_b_distance_3d/b_c_distance_3d) - (a_b_distance_2d/b_c_distance_2d))
        except ZeroDivisionError:
            pass  # TODO
    return variances

def compute_simple_variance(variances):
    abs_sum = 0
    for v in variances:
        abs_sum += abs(v)
    return abs_sum / len(variances)

def compute_percent_below_diff(variances, threshold=0.5):
    n = 0;
    for v in variances:
        if abs(v) < threshold:
            n += 1
    return float(n) / float(len(variances))

def show_map(stars, width, height):
    assert(isinstance(stars, list))
    print_sol = stars[0].StarID == 0
    print_proxima = stars[1].ProperName == "Proxima Centauri"
    print("_" * width)
    for j in range(height):
        line = ""
        for i in range(width):
            if print_sol and stars[0].X2d == i and stars[0].Y2d == j:
                line += "S"
                continue
            if print_proxima and stars[1].X2d == i and stars[1].Y2d == j:
                line += "P"
                continue
            star_present = False
            for s in stars:
                if s.X2d == i and s.Y2d == j:
                    star_present = True
                    break
            line += "*" if star_present else " "
        print(line)
