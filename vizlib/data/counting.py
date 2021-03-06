'''
'''
import numpy as np
from helpers import DataSet


def counting_2d(size=(32, 32), n_examples=10000, min_spots=0, max_spots=5, seed=42, standardization_type='individual'):
    if seed is not None:
        np.random.seed(seed)

    spot = np.array([[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]])
    X = []
    ys = []
    for i in range(n_examples):
        img = np.zeros(size)
        n_spots = np.random.randint(min_spots, max_spots + 1)

        spots_upper_left = generate_non_overlapping_points(
            size[0] - 3, size[1] - 3, n_spots
        )
        for y, x in spots_upper_left:
            for yo in range(spot.shape[0]):
                for xo in range(spot.shape[1]):
                    # the if ensures that already placed spots are not overwritten.
                    # because although their corners do not overlap, their values might.
                    if spot[yo, xo]:
                        img[y+yo, x+xo] = 1

        X.append(img)
        ys.append(n_spots - min_spots)

    return DataSet(X, ys)\
            .standardize(standardization_type=standardization_type)\
            .shuffle()


def generate_non_overlapping_points(w, h, n_points):
    points, i = set(), 0

    while len(points) < n_points:
        i += 1
        if i > n_points * 100:
            raise ValueError("Probably won't converge")
        points.add((np.random.randint(0, w), np.random.randint(0, h)))

    return points
