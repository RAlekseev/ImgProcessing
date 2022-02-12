import numpy as np
import matplotlib.pyplot as plt


def calc_histogram(pix, level=256):
    """
    Рассчитывает гистограму для заданного изображения
    :param pix: матрица полутонового изображения
    :param level: уровень, в переделах которого нужно расчитывать гистограмму
    :return: массив размерности level, в котром индекс i отображает количесвто пикселей яркости i
    """
    hists = [0 for _ in range(level)]
    for row in pix:
        for p in row:
            hists[p] += 1
    return hists


def calc_histogram_cdf(hists, block_m, block_n, level=256):
    """
    Рассчёт функции распределения (CDF - Cumulative distribution function)
    :param hists: массив размерности level, в котром индекс i отображает количесвто пикселей яркости i
    :param block_m: ширина исходного изображения
    :param block_n: высота исходного изображения
    :param level: уровень, в переделах которого нужно расчитывать CDF (можно указывать значение больше 255)
    :return:
    """
    # Кумулятивная сумма (Скользящая средняя)
    # то есть для массива [a1, a2, a3] получаем [a1, a1+a2, a1+a2+z32]
    hists_cumsum = np.cumsum(np.array(hists))
    # из лекции средний уровень яркости, к которому следует стремиться
    n0 = (block_m * block_n) / (level - 1)
    hists_cdf = (hists_cumsum / n0)
    hists_cdf[hists_cdf > 255] = 255
    return hists_cdf.astype(np.uint8)


def histogram_equalization(pix, level=256, norm_level=255):
    hists = calc_histogram(pix, level)

    (m, n) = pix.shape
    hists_cdf = calc_histogram_cdf(hists, m, n, norm_level)

    arr = hists_cdf[pix]
    return arr


def visualize_histogram(values, path, figsize=(20.0, 5.0)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(values, bins=range(0, 255))

    fig.savefig(path)
    plt.close()
