import numpy as np

import modules.audio_processing.frequency as frequency
import modules.audio_processing.tools as tools


def frequency_to_formant(f):
    if 0 < f <= 1000:
        return "F1"
    if 1000 < f <= 2000:
        return "F2"
    if 2000 < f <= 3000:
        return "F3"
    if 3000 < f <= 4000:
        return "F4"
    if 4000 < f <= 5000:
        return "F5"
    if 5000 < f <= 5000:
        return "F6"


def remove_formants(s, sample_rate, formant_to_remove, eps):
    global_min_bound = 300
    sr = np.copy(s)
    ssw, ssh = sr.shape

    min_formant, max_formant = formant_to_remove - eps, formant_to_remove + eps

    freq = frequency.get_frequencies(s, sample_rate)

    for ssy in range(0, ssh):
        if min_formant < freq[ssy] < max_formant or freq[ssy] < global_min_bound:
            for ssx in range(0, ssw):
                sr[ssx][ssy] = -np.infty

    return sr


def most_powerful_formant(s, sample_rate):
    """
    Получить самую сильную форманту для отрывка спектрограммы
    :param s: спектрограмма, исходная
    :param sample_rate
    :return: строка, самая сильная форманта на отрывке
    """

    ind = np.unravel_index(np.argmax(s, axis=None), s.shape)
    freq = frequency.get_frequencies(s, sample_rate)

    return freq[ind[1]]


def most_powerful_formants(s, bounds, sample_rate, x, eps):
    left, right = tuple(int(s.shape[0] * x) for x in bounds)
    right -= 1
    ss = s[left:right]

    sl = tools.normalize_spectrogram(ss)
    f1 = x_most_powerful_formant(sl, sample_rate, x)
    sl = remove_formants(sl, sample_rate, f1, eps)
    f2 = x_most_powerful_formant(sl, sample_rate, x)
    sl = remove_formants(sl, sample_rate, f2, eps)
    f3 = most_powerful_formant(sl, sample_rate)

    return str(int(f1)) + "Гц", str(int(f2)) + "Гц", str(int(f3)) + "Гц"


def x_most_powerful_formant(ss, sample_rate, x):
    ssw, ssh = ss.shape
    powerful_freqs = []
    freq = frequency.get_frequencies(ss, sample_rate)
    for ssx in range(0, ssw):
        ind = np.argpartition(ss[ssx], -x)[-x:]
        powerful_freq = ind[np.argmax(ind)]
        powerful_freqs.append(freq[powerful_freq])

    m = np.argmax(powerful_freqs)
    return powerful_freqs[m]
