import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageDraw

import modules.utils as utils
import modules.threshold as threshold
import modules.grayscale as grayscale
import os
import utils.image_utils as img_utils


def calc_weight_black(pix_threshold):
    unique, counts = np.unique(pix_threshold, return_counts=True)
    return dict(zip(unique, counts))[0]


def calc_black_ratio(pix_threshold):
    unique, counts = np.unique(pix_threshold, return_counts=True)
    weights = dict(zip(unique, counts))
    return weights[1] / (weights[0] + weights[1])


def image_moment_lambdas(pix, fn):
    pix_height = pix.shape[0]
    pix_width = pix.shape[1]

    result_sum = 0

    for x in range(0, pix_height):
        for y in range(0, pix_width):
            result_sum += fn(x, y) * pix[x][y]

    return result_sum


def calc_image_moment(pix, p=0, q=0):
    return image_moment_lambdas(pix, lambda x, y: (x ** p) * (y ** q))


def calc_image_central_moment(pix, _x, _y, p=0, q=0):
    return image_moment_lambdas(pix, lambda x, y: ((x - _x) ** p) * ((y - _y) ** q))


def get_icm45(pix, _x, _y):
    return 0.5 * image_moment_lambdas(pix, lambda x, y: (y - _y - x + _x)**2)


def get_icm135(pix, _x, _y):
    return 0.5 * image_moment_lambdas(pix, lambda x, y: (y - _y + x - _x)**2)


def calc_image_profile(pix, p=0, q=0):
    pix_height = pix.shape[0]
    pix_width = pix.shape[1]

    profile = []

    if p == 1:
        for x in range(0, pix_height):
            current_sum = 0
            for y in range(0, pix_width):
                current_sum += pix[x][y]
            profile.append(current_sum)
    elif q == 1:
        for y in range(0, pix_width):
            current_sum = 0
            for x in range(0, pix_height):
                current_sum += pix[x][y]
            profile.append(current_sum)

    return profile


def detect_symbols_in_profile(p):
    bounds = []

    bound_start = None
    for i in range(0, len(p)):
        if (p[i - 1] == 0 and p[i] != 0) or i == 0:
            bound_start = i
        elif (p[i - 1] != 0 and p[i] == 0) or (i == len(p) - 1 and bound_start is not None):
            bounds.append((bound_start, i))
            bound_start = None

    return bounds


def visualize_profile(profiles, profile_type, path, figsize=(5.0, 5.0)):
    pts = np.arange(len(profiles))

    fig, ax = plt.subplots(figsize=figsize)
    if profile_type == "horizontal":
        ax.plot(profiles, pts)
        #ax.set_yticklabels([])
    else:
        ax.plot(pts, profiles)
        #ax.set_xticklabels([])

    fig.savefig(path)
    plt.close()


def draw_bounds(source_path, result_path, rects):
    """
    :param source_path:
    :param result_path:
    :param rects: [x0, y0, x1, y1]
    :return:
    """
    img = Image.open(source_path)
    img.load()
    draw = ImageDraw.Draw(img)
    for i in range(0, len(rects)):
        draw.rectangle(rects[i], outline="red")

    img.save(result_path)


def get_rects(pix):
    result = []

    prof_x = calc_image_profile(pix, 1, 0)
    horizontal_bounds = detect_symbols_in_profile(prof_x)
    for i in range(0, len(horizontal_bounds)):
        (y0, y1) = horizontal_bounds[i]
        line_pix = pix[y0:y1]
        prof_y = calc_image_profile(line_pix, 0, 1)
        vertical_bounds = detect_symbols_in_profile(prof_y)
        for j in range(0, len(vertical_bounds)):
            (x0, x1) = vertical_bounds[j]
            char_pix = line_pix[:, x0:x1]
            char_prof_x = calc_image_profile(char_pix, 1, 0)
            char_bounds = detect_symbols_in_profile(char_prof_x)
            (fy0, fy1) = (char_bounds[0][0], char_bounds[-1][1])
            result.append([x0, y0 + fy0, x1, y0 + fy1])

    return result


def get_pix_font_metrics(pix):
    # далее рассчитываем сами признаки
    # a) Вес (масса чёрного)
    weight_black = calc_image_moment(pix, 0, 0)
    # b) Удельный вес (вес, нормированный к площади)
    weight_black_norm = weight_black / (pix.shape[0] * pix.shape[1])
    # c) Координаты центра тяжести
    x_coords = calc_image_moment(pix, 1, 0) / weight_black
    y_coords = calc_image_moment(pix, 0, 1) / weight_black
    # d) Нормированные координаты центра тяжести
    x_coords_norm = (x_coords - 1) / (pix.shape[0] - 1)
    y_coords_norm = (y_coords - 1) / (pix.shape[1] - 1)
    # e) Осевые моменты инерции по горизонтали и вертикали
    x_axis_moment = calc_image_central_moment(pix, x_coords, y_coords, 2, 0)
    y_axis_moment = calc_image_central_moment(pix, x_coords, y_coords, 0, 2)
    # f) Нормированные осевые моменты инерции
    x_axis_moment_norm = x_axis_moment / (weight_black ** 2)
    y_axis_moment_norm = y_axis_moment / (weight_black ** 2)

    icm45 = get_icm45(pix, x_coords, y_coords)
    icm135 = get_icm135(pix, x_coords, y_coords)

    icm45_norm = icm45 / (weight_black ** 2)
    icm135_norm = icm135 / (weight_black ** 2)

    return [
        weight_black,       weight_black_norm,
        x_coords,           y_coords,
        x_coords_norm,      y_coords_norm,
        x_axis_moment,      y_axis_moment,
        x_axis_moment_norm, y_axis_moment_norm,
        icm45,              icm135,
        icm45_norm,         icm135_norm
    ]


def get_normalized_image(pix):
    img_grayscale = threshold.apply_threshold(grayscale.grayscale(pix), 128, 1)
    return utils.pix_invert(img_grayscale, 0)


def get_pix_hypothesis(pix):

    path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_4/"  # insert the path to your directory
    letters_list = os.listdir(path)

    pix_rects = get_rects(pix)
    res = []
    for (x0, y0, x1, y1) in pix_rects:
        [
            _,                  weight_black_norm,
            _,                  _,
            x_coords_norm,      y_coords_norm,
            _,                  _,
            x_axis_moment_norm, y_axis_moment_norm,
            _,                  _,
            icm45_norm,         icm135_norm
        ] = get_pix_font_metrics(pix[y0:y1, x0:x1])

        diff_dict = {}
        for letter in letters_list:
            let_pix = img_utils.pix_from_img(path + letter)

            [
                _, let_weight_black_norm,
                _, _,
                let_x_coords_norm, let_y_coords_norm,
                _, _,
                let_x_axis_moment_norm, let_y_axis_moment_norm,
                _, _,
                let_icm45_norm, let_icm135_norm
            ] = get_pix_font_metrics(get_normalized_image(let_pix))

            black_diff = (weight_black_norm - let_weight_black_norm)
            x_center_diff = (x_coords_norm - let_x_coords_norm)
            y_center_diff = (y_coords_norm - let_y_coords_norm)
            x_axis_diff = (x_axis_moment_norm - let_x_axis_moment_norm)
            y_axis_diff = (y_axis_moment_norm - let_y_axis_moment_norm)
            icm45_diff = (icm45_norm - let_icm45_norm)
            icm135_diff = (icm135_norm - let_icm135_norm)
            diff_dict[letter[0]] = round(1 - (
                        black_diff ** 2 +
                        x_center_diff ** 2 +
                        y_center_diff ** 2 +
                        x_axis_diff ** 2 +
                        y_axis_diff ** 2 +
                        icm45_diff ** 2 +
                        icm135_diff ** 2
            ) ** (
                                         1 / 2), 2)

        res.append(diff_dict)

    return res
