import numpy as np


def xor(pix1, pix2):
    """
    Находит попиксельный xor двух матриц пикселей
    :param pix1: монохромная матрица пикселей
    :param pix2: монохромная матрица пикселей
    :return: попиксельный xor матриц pix1 и pix2
    """
    pix_height, pix_width = pix1.shape
    pix_xor = np.empty([pix_height, pix_width]).astype(np.uint8)

    for x in range(0, pix_height):
        for y in range(0, pix_width):
            pix_xor[x, y] = pix1[x, y] ^ pix2[x, y]

    return pix_xor


def apply_filter(pix, filter_fn, mask):
    """
    Применит фильтр, заданный функцией filter_fn
    :param pix: монохромная матрица пикселей
    :param filter_fn: функция, для каждого набора (pix, x, y, mask_size) возвращает новое значений пикселя (x,y)
    :param mask: матрица макси (подразумевается, что маска квадратная)
    :return:
    """
    result = np.copy(pix).astype(np.uint8)
    for x in range(0, pix.shape[0]):
        for y in range(0, pix.shape[1]):
            # применяем фильтр для каждого пикселя матрицы
            result[x][y] = filter_fn(pix, x, y, mask)

    return result


def spatial_smoothing_filter(pix, x, y, mask):
    """
    Алгоритм пространственного сглаживания
    :param pix: монохромная матрица пикселей
    :param x: текущая координата x обрабатываемого пикселя
    :param y: текущая координата y обрабатываемого пикселя
    :param mask: матрица макси (подразумевается, что маска квадратная)
    :return:
    """

    # определяем размер макси
    wmask = mask.shape[0] // 2
    pixels_sum = 0
    mask_sum = 0
    # "прикладываем" максу так, чтобы текущий пиксель (x,y) был в центре
    for i in range(-wmask, wmask + 1):
        for j in range(-wmask, wmask + 1):
            if (pix.shape[0] - 1) >= (x + i) >= 0 and (pix.shape[1] - 1) >= (y + j) >= 0:
                pixels_sum += pix[x + i, y + j] * mask[i + wmask][j + wmask]
                mask_sum += mask[i + wmask][j + wmask]

    return pixels_sum // mask_sum
