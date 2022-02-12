import numpy as np


def sobel_operator(pix):
    """
    Оператор Собеля
    :param pix: полутоновая матрица пикселей исходного изображения
    :return: массив из трёх матриц: G, Gx, Gy
    """
    [result, result_gx, result_gy] = [np.copy(pix), np.copy(pix), np.copy(pix)]
    size = result.shape
    for i in range(1, size[0] - 1):
        for j in range(1, size[1] - 1):
            gx = (pix[i - 1][j - 1] + 2 * pix[i][j - 1] + pix[i + 1][j - 1]) - (
                        pix[i - 1][j + 1] + 2 * pix[i][j + 1] + pix[i + 1][j + 1])
            gy = (pix[i - 1][j - 1] + 2 * pix[i - 1][j] + pix[i - 1][j + 1]) - (
                        pix[i + 1][j - 1] + 2 * pix[i + 1][j] + pix[i + 1][j + 1])
            result[i][j] = min(255, np.sqrt(gx ** 2 + gy ** 2))
            result_gx[i][j] = min(255, np.sqrt(gx ** 2 + 128 ** 2))
            result_gy[i][j] = min(255, np.sqrt(128 ** 2 + gy ** 2))
    return [result, result_gx, result_gy]
