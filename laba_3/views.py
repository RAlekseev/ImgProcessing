from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from laba_3.models import Laba3Result as Result
from io import BytesIO
from django.core.files.base import ContentFile
from utils.image_utils import *
import modules.threshold as threshold
import numpy as np
import math


def index(request):
	laba_3 = Result.objects.filter(user=request.user).order_by('-id')
	return render(request, 'laba_3/index.html', {'laba_3': laba_3})


def roberts_index(request):
	laba_3 = Result.objects.filter(user=request.user).order_by('-id')
	return render(request, 'laba_3/roberts.html', {'laba_3': laba_3})


def roberts(request):
	original_img = request.FILES['img']
	pix_sample = pix_from_img(original_img)
	# print(type(pix_sample[0][0]))
	# print(isinstance(pix_sample[0][0], np.ndarray))
	if isinstance(pix_sample[0][0], np.ndarray):
		pix_grayscale = grayscale_method(pix_sample)
	else:
		pix_grayscale = pix_sample

	[G, Gx, Gy] = roberts_operator(pix_grayscale)

	pix_threshold = threshold.apply_threshold(G, threshold.christian_threshold(G))

	img_after = Image.fromarray(pix_threshold)
	res_fp = BytesIO()
	img_after.save(res_fp, format='PNG')

	G = Image.fromarray(G)
	g_fp = BytesIO()
	G.save(g_fp, format='PNG')

	Gx = Image.fromarray(Gx)
	gx_fp = BytesIO()
	Gx.save(gx_fp, format='PNG')

	Gy = Image.fromarray(Gy)
	gy_fp = BytesIO()
	Gy.save(gy_fp, format='PNG')



	title = 'Лабораторная работа №3 Выделение контуров на изображении Оператор Робертса'

	result = Result.objects.create(title=title, user=request.user, img_before=original_img)

	result.Gx.save('gx.png', ContentFile(gx_fp.getvalue()))
	result.Gy.save('gy.png', ContentFile(gy_fp.getvalue()))
	result.G.save('g.png', ContentFile(g_fp.getvalue()))
	result.img_after.save('result.png', ContentFile(res_fp.getvalue()))
	result.save()

	return HttpResponseRedirect(reverse('laba_3:roberts-index'))

