import numpy as np
import math


def get_co_occurrence_matrix(pix, d, angles, L):
    height, width = pix.shape
    p = np.zeros([L, L]).astype(np.uint)

    for x in range(0, width):
        for y in range(0, height):
            for angle in angles:
                dx, dy = d*round(math.cos(angle)), d*round(math.sin(angle))
                _x, _y = x + dx, y + dy
                if (0 <= _x < width) and (0 <= _y < height):
                    i, j = pix[y][x], pix[_y][_x]
                    p[i][j] = p[i][j] + 1

    return p


def grayscale_to_levels(pix, L):
    """

    :param pix:
    :param L:
    :return:
    """
    step = 256 / L
    height, width = pix.shape
    result = np.empty([height, width]).astype(np.uint8)

    for x in range(0, height):
        for y in range(0, width):
            result[x, y] = math.floor(pix[x][y] / step)

    return result


def spread_image(pix):
    height, width = pix.shape

    result = np.empty([height, width]).astype(np.uint8)
    max_value, min_value = np.max(pix), np.min(pix[np.nonzero(pix)])

    for x in range(0, height):
        for y in range(0, width):
            result[x, y] = round(pix[x][y] / max_value * 255)

    return result


def av(matrix, axis=0):
    result = 0
    size = matrix.shape[0]
    for i in range(0, size):
        # считаем PJ(i) или PI(j)
        p = 0
        for j in range(0, size):
            p += matrix[i][j] if axis == 0 else matrix[j][i]
        result += i * p

    return result / (size**2)


def sums(matrix):
    result = []
    size = matrix.shape[0]
    for i in range(0, size):
        p = 0
        for j in range(0, size):
            p += matrix[i][j]
        result.append(p)

    return result
