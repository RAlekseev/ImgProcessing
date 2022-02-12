"""
Модуль содержит все функции, относящиеся к передискретизации изображений
"""

from fractions import Fraction
import numpy as np
import math


def interpolation(pix, m):
    """
    Растяжение (интерполяция) изображения в m раз
    :param pix: матрица, содержащая пиксели исходного изображения
    :param m: во сколько раз будет растянуто изображение

    :return: матрица, содержащая пиксели нового, растянутого изображения
    """
    return oversample(pix, m)


def decimation(pix, n):
    """
    Сжатие (децимация) изображения в n раз
    :param pix: матрица, содержащая пиксели исходного изображения
    :param n: во сколько раз будет уменьшено изображение

    :return: матрица, содержащая пиксели нового, сжатого изображения
    """
    return oversample(pix, 1 / n)


def oversample(pix, ratio):
    """
    Производит передескритизацию изображения
    :param pix: матрица, содержащая пиксели исходного изображения
    :param ratio: отношение размера нового изображения к старому (ratio > 1 - растяжение, ratio < 1 - сжатие)

    :return: матрица, содержащая пиксели нового, передескритизованного изображения
    """
    original_height, original_width, _ = pix.shape
    resized_height, resized_width = (round(original_height * ratio), round(original_width * ratio))

    pix_resized = np.empty([resized_height, resized_width, 3]).astype(np.uint8)

    for x in range(0, resized_height):
        for y in range(0, resized_width):
            pix_resized[x, y] = pix[math.floor(x / ratio), math.floor(y / ratio)]

    return pix_resized


def oversample_as_fraction(pix, ratio):
    """
    Производит передескритизацию изображения в два этапа, представляя ratio как дробь m/n
    :param pix: матрица, содержащая пиксели исходного изображения
    :param ratio: отношение размера нового изображения к старому (ratio > 1 - растяжение, ratio < 1 - сжатие)

    :return: матрица, содержащая пиксели нового, передескритизованного изображения
    """
    res = Fraction(ratio).limit_denominator()
    return decimation(interpolation(pix, res.numerator), res.denominator)
