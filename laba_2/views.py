from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from results.models import Result
from io import BytesIO
from django.core.files.base import ContentFile
from utils.image_utils import *

# import modules.oversample as oversample
import numpy as np
import math


def index(request):
	results = Result.objects.filter(user=request.user).order_by('-id')
	return render(request, 'laba_2/index.html', {'results': results})


def opening_index(request):
	results = Result.objects.filter(user=request.user).order_by('-id')
	return render(request, 'laba_2/opening.html', {'results': results})


def opening(request):
	original_img = request.FILES['img']
	pix_sample = pix_from_img(original_img)

	pix_result = dilation(erosion(pix_sample))

	img_after = Image.fromarray(pix_result)

	fp = BytesIO()
	img_after.save(fp, format='PNG')

	title = 'Лабораторная работа №2 Открытие (сжатие + расширение).'

	result = Result.objects.create(title=title, user=request.user, img_before=original_img)

	result.img_after.save('result.png', ContentFile(fp.getvalue()))
	result.save()

	return HttpResponseRedirect(reverse('laba_2:opening-index'))


def erosion(pix):

	result = np.copy(pix).astype(np.uint8)


	for x in range(3, pix.shape[0]-4):
		for y in range(3, pix.shape[1]-4):

			apperture_sum = pix[x-3:x+4, y-3:y+4].sum()
	# for x in range(1, pix.shape[0]-2):
	# 	for y in range(1, pix.shape[1]-2):
	#
	# 		apperture_sum = pix[x-1:x+2, y-1:y+2].sum()

			if (apperture_sum < 49*255):
				result[x][y] = 0
			else:
				result[x][y] = 255

	return result


def dilation(pix):


	result = np.copy(pix).astype(np.uint8)


	for x in range(2, pix.shape[0]-3):
		for y in range(2, pix.shape[1]-3):

			apperture_sum = pix[x-2:x+3, y-2:y+3].sum()

			if (apperture_sum > 254):
				result[x][y] = 255
			else:
				result[x][y] = 0

	return result


