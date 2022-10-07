import math


def get_distance_between_points(point_1: tuple[float, float], point_2: tuple[float, float]) -> float:
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    return math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
