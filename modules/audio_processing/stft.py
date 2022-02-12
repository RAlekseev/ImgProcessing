import numpy as np

from numpy.lib import stride_tricks
from matplotlib import pyplot as plt


def stft(sig, frame_size, overlap_factor=0.5, window=np.hanning):
    """
    Функция, выполняющая оконное преобразование Фурье
    Превращает одномерный массив значений в двумерный
    :param sig: одномерный массив, содержащий информацию о сигнале
    :param frame_size: размер окна
    :param overlap_factor: так называемый период окна, указывает в процентом соотношении (длина FFT к перооду)
    :param window: оконная функция (подрузамеваются нотации как в numpy функциях)
    :return:
    """
    win = window(frame_size)
    # рассчитываем размер прыжка: при периоде окна 0.5 по сути просто делим пополам
    hop_size = int(frame_size - np.floor(overlap_factor * frame_size))

    # добавляем нули к началу (паддинг)
    samples = np.append(np.zeros(int(np.floor(frame_size / 2.0))), sig)
    # рассчитываем общее количество значений: делим длину сигнала на размер прыжка
    cols = np.ceil((len(samples) - frame_size) / float(hop_size)) + 1
    # добавляем нули к концу (паддинг)
    samples = np.append(samples, np.zeros(frame_size))

    # теперь нам нужно представить массив в виде нижеопределённой формы
    shape = (int(cols), frame_size)
    strides = (samples.strides[0] * hop_size, samples.strides[0])
    frames = stride_tricks.as_strided(samples, shape=shape, strides=strides).copy()
    frames *= win

    # теперь применяем быстрое преобразование Фурье
    return np.fft.rfft(frames)
