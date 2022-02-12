from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from laba_8.models import Laba8Result as Result
from io import BytesIO
from django.core.files.base import ContentFile
import modules.utils as utils
import modules.threshold as threshold
import numpy as np
import modules.contrast as contrast
import matplotlib.pyplot as plt
import os


def index(request):
	results = Result.objects.filter(user=request.user).order_by('-id')
	return render(request, 'laba_8/index.html', {'results': results})


def visualize_histogram(values, path, figsize=(20.0, 5.0)):
	fig, ax = plt.subplots(figsize=figsize)
	ax.hist(values, bins=range(0, 255))

	fig.savefig(path)
	plt.close()


def execute(request):
	original_img = request.FILES['img']
	level = int(request.POST['level'])
	pix_sample = utils.pix_from_img(original_img)

	if isinstance(pix_sample[0][0], np.ndarray):
		pix_sample = utils.grayscale_method(pix_sample)


	title = 'Лабораторная работа №8 Улучшение изображений. Контрастирование'

	result = Result.objects.create(title=title, user=request.user, img_before=original_img)

	path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_8/" + str(result.id)
	os.mkdir(path)

	# stats = contrast.calc_histogram(pix_sample)
	visualize_histogram(pix_sample.flatten(), path + "/histogram_original.png")

	# улучшенное изображение
	pix_processed = contrast.histogram_equalization(pix_sample, 256, level)
	img_after = Image.fromarray(pix_processed)
	res_fp = BytesIO()
	img_after.save(res_fp, format='PNG')
	result.img_after.save('result.png', ContentFile(res_fp.getvalue()))
	result.save()

	# stats_processed = contrast.calc_histogram(pix_processed)
	visualize_histogram(pix_processed.flatten(), path + "/histogram_processed.png")

	return HttpResponseRedirect(reverse('laba_8:index'))
