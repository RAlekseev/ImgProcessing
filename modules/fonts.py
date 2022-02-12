from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import modules.utils as utils
import modules.font_analysis as font_analysis
import numpy as np
import modules.grayscale as grayscale
import modules.threshold as threshold


def create_image_from_text(text, font_path, font_size):
    test_img = Image.new("RGB", (font_size, font_size), (255, 255, 255))
    test_draw = ImageDraw.Draw(test_img)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = test_draw.textsize(text, font=font)

    # image_width, image_height = (font_size * len(text), font_size)
    img = Image.new("RGB", (text_width, text_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(font_path, font_size)
    # text_width, text_height = draw.textsize(text, font=font)
    draw.text((0, 0), text, (0, 0, 0), font=font)

    return img


def create_image_sample_text(text, font_path, font_size):
    # тестовое изображние, будем на нём смотреть реальный размер текста
    img = Image.new("RGB", (1000, font_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)    # как раз проверяем какой в итоге размер

    # а теперь, зная какие реальные размерф, можем чётко задать размеры изображения
    result_img = Image.new("RGB", (text_width, text_height), (255, 255, 255))
    result_draw = ImageDraw.Draw(result_img)
    result_draw.text((0, 0), text, (0, 0, 0), font=font)
    return result_img


def single_char_cropped(text, font_path, font_size):
    img = create_image_sample_text(text, font_path, font_size)
    pix = np.array(img)
    pix_processed = utils.pix_invert(threshold.apply_threshold(grayscale.grayscale(pix), 128, 1), 0)
    width = pix.shape[1]
    char_prof_x = font_analysis.calc_image_profile(pix_processed, 1, 0)
    char_prof_y = font_analysis.calc_image_profile(pix_processed, 0, 1)
    char_vert_bounds = font_analysis.detect_symbols_in_profile(char_prof_x)
    char_horiz_bounds = font_analysis.detect_symbols_in_profile(char_prof_y)
    (top, bottom) = (char_vert_bounds[0][0], char_vert_bounds[-1][1])
    (left, right) = (char_horiz_bounds[0][0], char_horiz_bounds[-1][1])

    return img.crop((left, top, right, bottom))


def generate_symbols_dictionary(symbols_set, font_path, font_size):
    result = {}
    for sym in symbols_set:
        result[sym] = single_char_cropped(sym, font_path, font_size)

    return result
