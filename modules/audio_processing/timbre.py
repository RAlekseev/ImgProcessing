import itertools
import operator
import numpy as np

import modules.audio_processing.tools as tools


def accumulate(l):
    it = itertools.groupby(l, operator.itemgetter(0))
    for key, subiter in it:
        yield key, sum(item[1] for item in subiter)


def detect_areas(s, min_gap, min_area):
    """
    Определяет, сколько уникальных отдельных зон в каждой отдельно взятой вертикале
    :param s:
    :param min_gap:
    :param min_area:
    :return:
    """
    w, h = s.shape
    result = []

    for i in range(0, w):
        a = [(x, len(list(y))) for x, y in itertools.groupby(s[i])]
        # убираем первый и последний, если они False
        if not a[0][0]:
            a = a[1:]
        # if not a[len(a)-1][0]:
        #     a = a[:-1]

        a = [(x, y) for x, y in a if x is True or y >= min_gap]
        b = list(accumulate(a))
        c = [(x, y) for x, y in b if x and y >= min_area]
        result.append(len(c))

    return result


def most_powerful_timbre(s, bin_size, sample_rate):
    pix = tools.focused_spectrogram(s, (-60, 0))
    detected_areas = detect_areas(pix, 3, 4)
    max_fragment = np.argmax(detected_areas)
    timing = tools.get_timing(s, bin_size, sample_rate, max_fragment)

    return timing
