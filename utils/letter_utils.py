import numpy as np
import matplotlib.pyplot as plt

def calc_image_moment(pix, p=0, q=0):
    return image_moment_lambdas(pix, lambda x, y: (x ** p) * (y ** q))


def calc_image_central_moment(pix, _x, _y, p=0, q=0):
    return image_moment_lambdas(pix, lambda x, y: ((x - _x) ** p) * ((y - _y) ** q))


def image_moment_lambdas(pix, fn):
    pix_height = pix.shape[0]
    pix_width = pix.shape[1]

    result_sum = 0

    for x in range(0, pix_height):
        for y in range(0, pix_width):
            if pix[x][y] < 10:
                result_sum += fn(x, y)

    return result_sum

def pixs_map(dictionary, fn):
    result = {}
    for key in dictionary:
        result[key] = fn(dictionary[key], key)

    return result


def calc_image_profile(pix, p=0, q=0):
    pix_height = pix.shape[0]
    pix_width = pix.shape[1]

    profile = []

    if p == 1:
        for x in range(0, pix_height):
            current_sum = 0
            for y in range(0, pix_width):
                current_sum += 255 - pix[x][y]
            profile.append(current_sum)
    elif q == 1:
        for y in range(0, pix_width):
            current_sum = 0
            for x in range(0, pix_height):
                current_sum += 255 - pix[x][y]
            profile.append(current_sum)

    return profile


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