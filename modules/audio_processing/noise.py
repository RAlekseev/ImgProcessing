import numpy as np
import matplotlib.pyplot as plt

import modules.audio_processing.tools as tools
import modules.utils as utils


def visualize_noise(noise_stats, timings, path, figsize=(20.0, 5.0)):
    pts = np.arange(len(noise_stats))

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(pts, noise_stats)
    ax.set_xticklabels(timings)
    plt.xlabel("Время(сек)")
    plt.ylabel("Уровень шума")

    fig.savefig(path)
    plt.close()


def save_noise_map(s, path):
    """
    Создаёт карту шума, выделяя только области шума на спектрограмме
    :param s: спектрограмма аудиодорожки
    :param path: путь, по которому необходимо сохранить карту шума
    :return:
    """
    pix = tools.focused_spectrogram(s, (-300, -100))
    utils.pix_to_path(np.transpose(pix)[::-1], path)


def save_noise_level_chart(s, bin_size, sample_rate, path):
    timings = tools.get_timings(s, bin_size, sample_rate)
    pix = tools.focused_spectrogram(s, (-100, -80))
    sums = np.sum(pix, axis=1)
    sums = sums / s.shape[1]
    visualize_noise(sums, timings, path)
