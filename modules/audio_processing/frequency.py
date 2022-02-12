import numpy as np

import modules.audio_processing.tools as tools


def get_frequencies(s, sample_rate):
    return np.abs(np.fft.fftfreq(s.shape[1] * 2, 1.0 / sample_rate)[:s.shape[1] + 1])


def get_explicit_frequences(s, n):
    """
    Находит частоты, соответсвующие самому яркому значению dBFS
    Если делать точно, то для каждой единицы времени нужно:
     1) найти максимальное значение для dBFS
     2) получить индекс частоты, соотвествующий этому значению
     3) сопоставить индексу частоты реальную частоту

    Но мы можем делать небольшую погрешность и брать значение не самое максимальное, а близкое к максимальному
    :param s:
    :param n:
    :return:
    """

    s_norm = tools.normalize_spectrogram(s)
    result = []
    for i in range(0, s_norm.shape[0]):
        maximums = s_norm[i].argsort()[-n:][::-1]
        result.append(max(maximums))

    return result


def get_min_frequency(s, bin_size, sample_rate):
    exp_freq = get_explicit_frequences(s, 5)
    freq = get_frequencies(s, sample_rate)
    arg_min = np.argmin(exp_freq)
    timing = tools.get_timing(s, bin_size, sample_rate, arg_min)

    return freq[exp_freq[arg_min]], timing


def get_max_frequency(s, bin_size, sample_rate):
    exp_freq = get_explicit_frequences(s, 5)
    freq = get_frequencies(s, sample_rate)
    arg_max = np.argmax(exp_freq)
    timing = tools.get_timing(s, bin_size, sample_rate, arg_max)

    return freq[exp_freq[arg_max]], timing
