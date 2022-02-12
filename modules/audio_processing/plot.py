import numpy as np
from matplotlib import pyplot as plt

import modules.audio_processing.tools as tools
import modules.audio_processing.frequency as frequency


def audio_spectrogram(sample_rate, s, plot_path=None, bin_size=2**10):
    # получаем массив частот
    freq = frequency.get_frequencies(s, sample_rate)
    data = tools.normalize_spectrogram(s)  # шкала dBFS

    time_bins, freq_bins = np.shape(data)

    plt.figure(figsize=(time_bins/100, freq_bins/100))
    plt.imshow(np.transpose(data), origin="lower", aspect="auto", cmap="jet", interpolation="none")

    plt.xlabel("Время(сек)")
    plt.ylabel("Частота(Гц)")
    plt.xlim([0, time_bins-1])
    plt.ylim([0, freq_bins])

    plt.colorbar().ax.set_xlabel('dBFS')

    x_locations = np.float32(np.linspace(0, time_bins-1, 10))
    plt.xticks(x_locations, tools.get_timings(s, bin_size, sample_rate))
    y_locations = np.int16(np.round(np.linspace(0, freq_bins-1, 20)))
    plt.yticks(y_locations, ["%.02f" % freq[i] for i in y_locations])

    plt.savefig(plot_path)
    plt.clf()

    return data
