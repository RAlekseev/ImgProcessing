# import modules.fonts as fonts
import modules.fonts as fonts
import utils.image_utils as utils
import modules.grayscale as grayscale
import modules.threshold as threshold
import numpy as np
import modules.font_analysis as fa
import modules.csv_tools as csv_tools
from PIL import Image

RESULTS_PATH = "media/results/task4"
RESULTS_PATH_VERT_PROF = RESULTS_PATH + "/profiles/vertical/"
RESULTS_PATH_HOR_PROF = RESULTS_PATH + "/profiles/horizontal/"
SYMBOLS_STR = "AΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"  # символы для анализа


def dictionary_to_pixs(dictionary):
    result = {}
    for key in dictionary:
        result[key] = np.array(dictionary[key])
    return result


def pixs_map(dictionary, fn):
    result = {}
    for key in dictionary:
        result[key] = fn(dictionary[key], key)

    return result


def pix_to_path(pix, image_path):
    img = Image.fromarray(pix)
    img.save(image_path)


def pixs_to_path(dictionary, path):
    for key in dictionary:
        pix_to_path(dictionary[key], path + "/" + key + ".png")


# создаём словарь со всеми символами
symbols = dictionary_to_pixs(fonts.generate_symbols_dictionary(SYMBOLS_STR, "/Users/jewelieee/Desktop/Bopai/fonts/arial.ttf", 52))
# переводим все символы в ч/б
symbols_threshold = pixs_map(symbols, lambda pix, _s: utils.apply_threshold(grayscale.grayscale(pix)))
# сохраняем исходные изображения символов в директорию (один символ - один файл)
pixs_to_path(symbols_threshold, "/Users/jewelieee/Desktop/Bopai/media/images/laba_4")

