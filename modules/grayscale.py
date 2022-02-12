"""
Модуль содержит функции, связанные с приведением изображений к полутоновым
"""
import numpy as np


def grayscale(pix):
    """
    Приводит изображние к полутоновому
    :param pix: матрица, содержащая пиксели исходного изображения
    :return: матрица, содержащая пиксели нового, полутонового изображения
    """
    pix_height = pix.shape[0]
    pix_width = pix.shape[1]

    pix_grayscale = np.empty([pix_height, pix_width]).astype(np.uint8)

    for x in range(0, pix_height):
        for y in range(0, pix_width):
            pix_grayscale[x, y] = round(np.mean(pix[x, y]))

    return pix_grayscale
