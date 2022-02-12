from django.shortcuts import render
from PIL import Image
import utils.letter_utils as utils
import utils.image_utils as img_utils
import os
import modules.threshold as threshold


def index(request):
	path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_4/"  # insert the path to your directory
	img_list = os.listdir(path)

	prof_path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_4_prof/"
	profs_x = os.listdir(prof_path + 'prof_x')
	profs_y = os.listdir(prof_path + 'prof_y')

	images = {}

	for img in img_list:
		pix = img_utils.pix_from_img(path + img)
		# pix = utils.pixs_map(pix, lambda pix, _s: threshold.apply_threshold(pix, 128, 1))
		weight_black = utils.calc_image_moment(pix, 0, 0)
		x_coords = utils.calc_image_moment(pix, 1, 0) / weight_black
		y_coords = utils.calc_image_moment(pix, 0, 1) / weight_black
		x_axis_moment = utils.calc_image_central_moment(pix, x_coords, y_coords, 2, 0)
		y_axis_moment = utils.calc_image_central_moment(pix, x_coords, y_coords, 0, 2)

		if img not in profs_x:
			prof_x = utils.calc_image_profile(pix, 1, 0)[::-1]
			prof_y = utils.calc_image_profile(pix, 0, 1)

			utils.visualize_profile(prof_x, "horizontal", prof_path + 'prof_x/' + img)
			utils.visualize_profile(prof_y, "vertical", prof_path + 'prof_y/' + img)

		images[img] = {
			'image': open(path + img),
			'weight_black': weight_black,
			'weight_black_norm': round(weight_black / (pix.shape[0] * pix.shape[1]), 3),
			'x_coords': round(x_coords),
			'y_coords': round(y_coords),
			'x_coords_norm': round((x_coords - 1) / (pix.shape[0]),2),
			'y_coords_norm': round((y_coords - 1) / (pix.shape[1]),2),
			'x_axis_moment': round(x_axis_moment),
			'y_axis_moment': round(y_axis_moment),
			'x_axis_moment_norm': round(x_axis_moment / (weight_black ** 2), 2),
			'y_axis_moment_norm': round(y_axis_moment / (weight_black ** 2), 2),
		}

	print(images)

	return render(request, 'laba_4/index.html', {'images': images})
