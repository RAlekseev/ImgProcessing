from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from results.models import Result
from io import BytesIO
from django.core.files.base import ContentFile

# import modules.oversample as oversample
import numpy as np
import math


def index(request):
    results = Result.objects.filter(user=request.user).order_by('-id')
    return render(request, 'laba_1/index.html', {'results': results})


def resampling_index(request):

    return render(request, 'laba_1/resampling.html')


def resampling(request):
    original_img = request.FILES['img']
    pix_sample = pix_from_img(original_img)
    if request.POST['k']:
        pix_oversampled = oversample(pix_sample, float(request.POST['k']))
    else:
        m = float(request.POST['m']) if request.POST['m'] else 1
        n = float(request.POST['n']) if request.POST['n'] else 1
        pix_oversampled = oversample(pix_sample, m/n)

    img_after = Image.fromarray(pix_oversampled)
    fp = BytesIO()
    img_after.save(fp, format='PNG')

    result = Result.objects.create(title='test', user=request.user, img_before=original_img)

    result.img_after.save('result.png', ContentFile(fp.getvalue()))
    result.save()

    return HttpResponseRedirect(reverse('laba_1:resampling-index'))


def grayscale_index(request):
    return render(request, 'laba_1/grayscale.html')


def grayscale(request):
    original_img = request.FILES['img']
    pix_sample = pix_from_img(original_img)

    pix_result = grayscale_method(pix_sample)

    img_after = Image.fromarray(pix_result)

    fp = BytesIO()
    img_after.save(fp, format='PNG')

    title = 'Лабораторная работа №1.2 Приведение полноцветного изображения к полутоновому.'

    result = Result.objects.create(title=title, user=request.user, img_before=original_img)

    result.img_after.save('result.png', ContentFile(fp.getvalue()))
    result.save()

    return HttpResponseRedirect(reverse('laba_1:grayscale-index'))


def threshold_index(request):
    return render(request, 'laba_1/threshold.html')

def threshold(request):
    original_img = request.FILES['img']
    pix_sample = pix_from_img(original_img)
    pix_grayscale = grayscale_method(pix_sample)

    pix_result = apply_threshold(pix_grayscale, christian_threshold(pix_grayscale, k=float(request.POST['k'])))

    img_after = Image.fromarray(pix_result)

    fp = BytesIO()
    img_after.save(fp, format='PNG')

    title = 'Лабораторная работа №1.3 Алгоритм адаптивной бинаризации Ниблэка. K=' + request.POST['k']

    result = Result.objects.create(title=title, user=request.user, img_before=original_img)

    result.img_after.save('result.png', ContentFile(fp.getvalue()))
    result.save()

    return HttpResponseRedirect(reverse('laba_1:threshold-index'))


def pix_from_img(img):
    img = Image.open(img)
    img.load()
    return np.array(img)

def pix_to_img(pix):
    img = Image.fromarray(pix)
    return img


def oversample(pix, ratio):
    original_height, original_width, _ = pix.shape
    resized_height, resized_width = (round(original_height * ratio), round(original_width * ratio))
    pix_resized = np.empty([resized_height, resized_width, 4]).astype(np.uint8)

    for x in range(0, resized_height):
        for y in range(0, resized_width):
            pix_resized[x, y] = pix[math.floor(x / ratio), math.floor(y / ratio)]

    return pix_resized


def grayscale_method(pix):
    original_height, original_width, _ = pix.shape
    pix_grayscale = np.empty([original_height, original_width]).astype(np.uint8)

    for x in range(0, original_height):
        for y in range(0, original_width):
            pix_grayscale[x, y] = round(np.mean(pix[x, y]))

    return pix_grayscale


def christian_threshold(pix, w_size=15, k=-0.2):
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

    # находим минимальное серое значение всего изображения M
    max_std = np.max(stds)
    # находим максимальное среднеквадратичное значение всего изображение R
    min_v = np.min(pix)

    # составляем матрицу локальных пороговых значений (формула Кристиана)
    thresholds = means + k * stds

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