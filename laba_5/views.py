from django.shortcuts import render, HttpResponseRedirect
from PIL import Image
# import utils.letter_utils as utils
import utils.image_utils as img_utils
import os
from io import BytesIO
from laba_5.models import Laba5Result as Result
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

	return render(request, 'laba_5/index.html', {'fonts': fonts, 'results': results})


def execute(request):
	text = request.POST['text']
	font = request.POST['font']

	img_before = fonts.create_image_from_text(text, "/Users/jewelieee/Desktop/Bopai/fonts/" + font, 52)
	img_pix = fa.get_normalized_image(utils.pix_from_img(img_before))

	#
	# img_before = Image.fromarray(img_pix)

	before_fp = BytesIO()
	img_before.save(before_fp, format='PNG')

	title = 'Лабораторная работа №5 Сегментация текста.'



	result = Result.objects.create(title=title, text=text, font=font, user=request.user)
	path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_5/" + str(result.id)
	os.mkdir(path)

	prof_x = fa.calc_image_profile(img_pix, 1, 0)[::-1]
	prof_y = fa.calc_image_profile(img_pix, 0, 1)

	fa.visualize_profile(prof_x, "horizontal", path + "/horizontal.png")
	fa.visualize_profile(prof_y, "vertical", path + "/vertical.png", (25, 5))

	result.img_before.save('before.png', ContentFile(before_fp.getvalue()))
	result.save()

	rects_img_1 = fa.get_rects(img_pix)
	fa.draw_bounds(result.img_before.path, path + "/bounds.png", rects_img_1)

	os.mkdir(path + "/char_profiles")
	os.mkdir(path + "/char_profiles/original/")
	os.mkdir(path + "/char_profiles/horizontal/")
	os.mkdir(path + "/char_profiles/vertical/")
	save_char_profiles(img_pix, rects_img_1, path)

	return HttpResponseRedirect(reverse('laba_5:index'))


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