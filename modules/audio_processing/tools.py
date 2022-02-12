import numpy as np


def normalize_spectrogram(s):
    return 20. * np.log10(np.abs(s) / 10e+6)


def focused_spectrogram(s, bounds):
    """
    Фокусирует только определённый диапозон dBFS
    :param s: спекрограмма (исходная)
    :param bounds: кортеж из жвух чисел - левая и правая граница (включительно)
    :return: матрица со значениями True и False (True, если значение ячейке принадлежит диапозону dBFS, False иначе)
    """
    sn = normalize_spectrogram(s)
    left, right = bounds
    return ((sn <= right) * (sn >= left) * 255).astype(np.bool)


def get_timing(s, bin_size, sample_rate, x):
    samples_length = np.ceil(len(s) // 2) * bin_size
    time_bins, freq_bins = np.shape(s)
    return ((x * samples_length / time_bins) + (0.5 * bin_size)) / sample_rate


def get_timings(s, bin_size, sample_rate):
    samples_length = np.ceil(len(s) // 2) * bin_size
    time_bins, freq_bins = np.shape(s)
    x_locations = np.float32(np.linspace(0, time_bins - 1, 10))
    return ["%.02f" % l for l in ((x_locations * samples_length / time_bins) + (0.5 * bin_size)) / sample_rate]
