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
    if nsamples is None:
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
    n = 0
    for v in variances:
        if abs(v) < threshold:
            n += 1
    return float(n) / float(len(variances))

def show_map(stars, width, height, zoom=1):
    assert(isinstance(stars, list))
    print_sol = stars[0].StarID == 0
    print_proxima = stars[1].ProperName == "Proxima Centauri"
    print("_" * width)
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