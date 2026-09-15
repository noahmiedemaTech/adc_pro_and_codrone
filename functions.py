import math

def inches_to_cm(inches):
    return inches * 2.54


def cm_to_inches(cm):
    return cm / 2.54


def distance_2d(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

