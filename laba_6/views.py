from django.shortcuts import render, HttpResponseRedirect
from PIL import Image
import modules.csv_tools as csv_tools

import os
from io import BytesIO
from laba_6.models import Laba6Result as Result
from django.core.files.base import ContentFile
from django.urls import reverse
import modules.fonts as fonts
import modules.utils as utils
import modules.font_analysis as fa
import numpy as np


def index(request):
	fonts_path = "/Users/jewelieee/Desktop/Bopai/fonts/"
	fonts = os.listdir(fonts_path)

	results = Result.objects.all()

	path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_4/"  # insert the path to your directory
	letters = os.listdir(path)

	return render(request, 'laba_6/index.html', {'fonts': fonts, 'results': results, 'letters': letters})


def execute(request):
	text = request.POST['text']
	font = request.POST['font']

	img_before = fonts.create_image_from_text(text, "/Users/jewelieee/Desktop/Bopai/fonts/" + font, int(request.POST['font_size']))
	img_pix = fa.get_normalized_image(utils.pix_from_img(img_before))

	# model_dict = csv_tools.load_model('media/results/task4/analysis_file.csv')
	hypothesis = fa.get_pix_hypothesis(img_pix)
	print(hypothesis)

	before_fp = BytesIO()
	img_before.save(before_fp, format='PNG')

	title = 'Лабораторная работа №6 Классификация на основе признаков, анализ профилей. Font_size:' + request.POST['font_size']

	result = Result.objects.create(title=title, text=text, font=font, user=request.user, letters=hypothesis)

	result.img_before.save('before.png', ContentFile(before_fp.getvalue()))
	result.save()



	return HttpResponseRedirect(reverse('laba_6:index'))


def save_char_profiles(_img, _rects_img, path):
	for (x0, y0, x1, y1) in _rects_img:
		subpix = _img[y0:y1, x0:x1]
		name = "[%.0f, %.0f, %.0f, %.0f]" % (x0, y0, x1, y1)
		_prof_x = fa.calc_image_profile(subpix, 1, 0)[::-1]
		_prof_y = fa.calc_image_profile(subpix, 0, 1)

		Image.fromarray(pix_back(subpix)).save(path + "/char_profiles/original/" + name + ".png")
		fa.visualize_profile(_prof_x, "horizontal", path + "/char_profiles/horizontal/" + name + ".png")
		fa.visualize_profile(_prof_y, "vertical", path + "/char_profiles/vertical/" + name + ".png")


def pix_back(pix_normalized):
	pix_height = pix_normalized.shape[0]
	pix_width = pix_normalized.shape[1]

	pix_inverted = np.empty([pix_height, pix_width]).astype(np.uint8)

	for x in range(0, pix_height):
		for y in range(0, pix_width):
			pix_inverted[x][y] = 255 if (pix_normalized[x][y] == 0) else 0

	return pix_inverted