from PIL import Image
import numpy as np


def pix_from_img(img):
    img = Image.open(img)
    img.load()
    return np.array(img)


def grayscale_method(pix):
    original_height, original_width, _ = pix.shape
    pix_grayscale = np.empty([original_height, original_width]).astype(np.uint8)

    for x in range(0, original_height):
        for y in range(0, original_width):
            pix_grayscale[x, y] = round(np.mean(pix[x, y]))

    return pix_grayscale

def roberts_operator(pix):
    """
    Оператор Собеля
    :param pix: полутоновая матрица пикселей исходного изображения
    :return: массив из трёх матриц: G, Gx, Gy
    """
    [result, result_gx, result_gy] = [np.copy(pix), np.copy(pix), np.copy(pix)]
    size = result.shape
    for i in range(1, size[0] - 1):
        for j in range(1, size[1] - 1):
            # gx = pix[i + 1][j + 1] - pix[i][j]
            # gy = pix[i + 1][j] - pix[i][j + 1]
            gx = (pix[i - 1][j - 1] + 2 * pix[i][j - 1] + pix[i + 1][j - 1]) - (
                        pix[i - 1][j + 1] + 2 * pix[i][j + 1] + pix[i + 1][j + 1])
            gy = (pix[i - 1][j - 1] + 2 * pix[i - 1][j] + pix[i - 1][j + 1]) - (
                        pix[i + 1][j - 1] + 2 * pix[i + 1][j] + pix[i + 1][j + 1])
            result[i][j] = min(255, np.sqrt(gx ** 2 + gy ** 2))
            result_gx[i][j] = min(255, np.sqrt(gx ** 2 + 128 ** 2))
            result_gy[i][j] = min(255, np.sqrt(128 ** 2 + gy ** 2))
    return [result, result_gx, result_gy]


def christian_threshold(pix, w_size=15, k=0.5):
    """
    Алгоритм адаптивной бинаризации Кристиана
    :param pix: матрица, содержащая пиксели исходного (но уже полутонового) изображения
    :param w_size: размер окна
    :param k: коэффициент из формулы Кристиана

    :return: матрица локальных пороговых значений
    """
    # получаем ширину и высоту исходного изображения
    rows, cols = pix.shape
    i_rows, i_cols = rows + 1, cols + 1

    # создаём две пустые матрицы аналогичного размера
    integ = np.zeros((i_rows, i_cols), np.float)
    sqr_integral = np.zeros((i_rows, i_cols), np.float)

    # здесь мы получаем матрицу интегральных изображний (сумма всех элементов матрицы от (0,0) до (i, j) включительно)
    # суммируем в два подхода - сначала по столцам, потом по строкам
    integ[1:, 1:] = np.cumsum(np.cumsum(pix.astype(np.float), axis=0), axis=1)
    # матрица квадратов пикселей исходного изображения
    sqr_img = np.square(pix.astype(np.float))
    # матрица интегральных изображений для квадратов пикселей
    sqr_integral[1:, 1:] = np.cumsum(np.cumsum(sqr_img, axis=0), axis=1)

    # создаём две сетки (аналогичные размеру исходного изображения)
    # сетка-x в каждом ряду содержит 1...i_cols
    # сетка-y d каждом столбце модержит 1...i_rows
    x, y = np.meshgrid(np.arange(1, i_cols), np.arange(1, i_rows))

    # половина размера окна
    hw_size = w_size // 2
    # далее получаем четыре матрицы, где к каждому элемента прибавили/отняли полвину окна (+ ограничение)
    x1 = (x - hw_size).clip(1, cols)
    x2 = (x + hw_size).clip(1, cols)
    y1 = (y - hw_size).clip(1, rows)
    y2 = (y + hw_size).clip(1, rows)

    # считаем размеры соотвестующих окрестностей
    l_size = (y2 - y1 + 1) * (x2 - x1 + 1)

    # сумма яркостей (рекурретная формула)
    sums = (integ[y2, x2] - integ[y2, x1 - 1] - integ[y1 - 1, x2] + integ[y1 - 1, x1 - 1])
    # аналогично для квадратов пикселей (рекурретная формула)
    sqr_sums = (sqr_integral[y2, x2] - sqr_integral[y2, x1 - 1] - sqr_integral[y1 - 1, x2] + sqr_integral[y1 - 1, x1 - 1])

    # считаем средние значения выборки для окрестности точки (x, y)
    means = sums / l_size

    # считаем среднеквадратичное отклонение для той же окрестности
    stds = np.sqrt(sqr_sums / l_size - np.square(means))

    # находим минимальное серое значение всего изображения
    max_std = np.max(stds)
    # находим максимальное среднеквадратичное значение всего изображение
    min_v = np.min(pix)

    # составляем матрицу локальных пороговых значений (формула Кристиана)
    thresholds = ((1.0 - k) * means + k * min_v + k * stds / max_std * (means - min_v))

    return thresholds


def apply_threshold(pix, threshold=128, wp_val=255):
    """
    Бинаризация изображения либо по глобальному пороговому значению, либо по матрица локальных пороговых значений
    :param pix: матрица, содержащая пиксели исходного (но уже полутонового) изображения
    :param threshold: матрица локальных пороговых значений (или одно глобальное пороговое значение)
    :param wp_val: значение, которое будет присвоено пикселях выше порога

    :return: матрица пикселей бинаризованного изображения
    """
    return ((pix >= threshold) * wp_val).astype(np.uint8)