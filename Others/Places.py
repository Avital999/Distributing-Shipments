import numpy as np
import random
import math


def get_places_matrix(locations_num: int, max_distance):
    """

    :param locations_num: The number of locations includes the place from which the packages depart.
    :param max_distance: The matrix simulates a two-dimensional map
     of locations with the central place as its central point.
     The size of the map will be max_distance*2 by max_distance*2.
     central point location will be (max_distance, max_distance).
    :return: A graph represented by a neighborhood matrix where:
        1. The first vertex is the location from which the packages depart
        2. The other vertices are the locations where the couriers bring the packages
        3. The weights of the edge [i,j] represents the time it takes to get from location i to location j.
    """

    mat = np.zeros(shape=(locations_num+1, locations_num+1))

    # The location of the first vertex is the middle point
    locations = [(max_distance, max_distance)]

    # Add all the other location, every location is a tuple (x,y)
    for i in range(locations_num+1):
        locations.append((random.randint(0, max_distance*2), (random.randint(0, max_distance*2))))


    for i in range(locations_num+1):
        for j in range(locations_num+1):
            d = math.dist(locations[i], locations[j])
            mat[i][j] = mat[j][i] = round(d, 2)

    return mat

