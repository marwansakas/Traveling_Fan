from math import sqrt
from random import randint, uniform
from data.constants import *
import numpy as np


def distance(a, b):
    return sqrt((b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y))


def sum_distance(points):
    s = 0
    for i in range(len(points)):
        dist = distance(points[i], points[(i + 1) % len(points)])
        s += dist
    return s


def sum_real_distances(distance_values):
    first_gen = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    s = sum([distance_values[first_gen[i - 1]][first_gen[i]] for i in range(len(first_gen))])
    return s


def euclidean_distance(point1, point2):
    return np.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)


def create_distance_matrix(points):
    num_points = len(points)
    distance_matrix = np.zeros((num_points, num_points))

    for i in range(num_points):
        for j in range(num_points):
            distance_matrix[i, j] = euclidean_distance(points[i], points[j])

    return distance_matrix


def find_offset(screen_width, screen_height):

    scale_x = screen_width / manual_width
    scale_y = screen_height / manual_height

    x_min_scaled = int(x_min * scale_x)
    x_max_scaled = int(x_max * scale_x)
    y_min_scaled = int(y_min * scale_y)
    y_max_scaled = int(y_max * scale_y)

    return x_min_scaled, x_max_scaled, y_min_scaled, y_max_scaled


def scale_coordinates(coordinates, screen_width, screen_height):
    # Scale factors
    width_scale = screen_width / manual_width
    height_scale = screen_height / manual_height

    # Scale the coordinates
    scaled_coordinates = []
    for coord in coordinates:
        scaled_x = int(coord[0] * width_scale)
        scaled_y = int(coord[1] * height_scale)
        scaled_coordinates.append((scaled_x, scaled_y))

    return np.array(scaled_coordinates)



