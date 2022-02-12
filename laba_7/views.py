from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from laba_7.models import Laba7Result as Result
from io import BytesIO
from django.core.files.base import ContentFile
import modules.font_analysis as font_analysis
import modules.utils as utils
import modules.threshold as threshold
import numpy as np
import modules.contrast as contrast
import matplotlib.pyplot as plt
import os
import math

import modules.glcm as glcm

ANGLES = [
    0.25*math.pi,
    0.75*math.pi,
    1.25*math.pi,
    1.75*math.pi
]


def index(request):
	results = Result.objects.filter(user=request.user).order_by('-id')
	return render(request, 'laba_7/index.html', {'results': results})


def execute(request):
	original_img = request.FILES['img']
	pix_sample = utils.pix_from_img(original_img)

	if isinstance(pix_sample[0][0], np.ndarray):
		pix_grayscale = utils.grayscale_method(pix_sample)
	else:
		pix_grayscale = pix_sample

	levels_matrix = glcm.grayscale_to_levels(pix_grayscale, 255)
	co_occurrence_matrix = glcm.get_co_occurrence_matrix(levels_matrix, 2, ANGLES, 255)

	mui = glcm.av(co_occurrence_matrix, 0)
	muj = glcm.av(co_occurrence_matrix, 1)

	sums = glcm.sums(co_occurrence_matrix)

	title = 'Лабораторная работа №7 Текстурный анализ'
	result = Result.objects.create(title=title, user=request.user, img_before=original_img, evidence=[mui, muj, sums])
	path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_7/" + str(result.id)
	os.mkdir(path)

	# print(sums)
	font_analysis.visualize_profile(sums, "vertical", path + "/histogram.png", (20.0, 5.0))

	img_after = Image.fromarray(glcm.spread_image(co_occurrence_matrix))
	res_fp = BytesIO()
	img_after.save(res_fp, format='PNG')
	result.img_after.save('result.png', ContentFile(res_fp.getvalue()))
	result.save()

	return HttpResponseRedirect(reverse('laba_7:index'))
