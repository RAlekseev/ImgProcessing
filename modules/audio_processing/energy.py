import numpy as np
import matplotlib.pyplot as plt

import modules.audio_processing.tools as tools
import modules.utils as utils


def visualize_noise(noise_stats, regs_to_focus, timings, path, figsize=(20.0, 5.0)):
    pts = np.arange(len(noise_stats))

    fig, ax = plt.subplots(figsize=figsize)
    for left, right in regs_to_focus:
        plt.axvspan(left, right, color='red', alpha=0.5)
    ax.plot(pts, noise_stats)
    ax.set_xticklabels(timings)
    ax.set_yticklabels([])
    plt.xlabel("Время(сек)")
    plt.ylabel("Энергия")

    fig.savefig(path)
    plt.close()


def get_energy_regions(energy_indexes, min_size=5):
    result = []
    length = energy_indexes.shape[0]

    start = None
    for i in range(0, length):
        if energy_indexes[i] == True:
            if start is None:
                start = i
        elif start is not None:
            if i - 1 - start >= min_size:
                result.append((start, i - 1))
            start = None

    return result


def save_energy_chart(s, bin_size, sample_rate, bounds, path):
    left, right = bounds
    sn = tools.normalize_spectrogram(s)
    sn[sn > right] = np.nan
    sn[sn < left] = np.nan
    timings = tools.get_timings(s, bin_size, sample_rate)
    avg = np.nanmean(sn, axis=1)
    max_in_avg = avg[np.argmax(avg)]
    min_accept_bound = max_in_avg * 1.05
    max_energy_regions = get_energy_regions(avg >= min_accept_bound)
    visualize_noise(avg, max_energy_regions, timings, path)
