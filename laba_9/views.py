from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from PIL import Image
from laba_9.models import Laba9Result as Result
from io import BytesIO
from django.core.files.base import ContentFile
import modules.utils as utils
import modules.threshold as threshold
import numpy as np
import modules.contrast as contrast
import matplotlib.pyplot as plt
import os
from scipy.io import wavfile

import modules.audio_processing.formant as formant
import modules.audio_processing.noise as noise
import modules.audio_processing.frequency as frequency
import modules.audio_processing.stft as stft
import modules.audio_processing.plot as plot
import modules.audio_processing.timbre as timbre
import modules.audio_processing.energy as energy

def index(request):
	results = Result.objects.filter(user=request.user).order_by('-id')
	return render(request, 'laba_9/index.html', {'results': results})

def execute(request):
	original_voice = request.FILES['img']

	title = 'Лабораторная работа №9 Обработка звуковой информации'
	result = Result.objects.create(title=title, user=request.user, voice=original_voice)
	path = "/Users/jewelieee/Desktop/Bopai/media/images/laba_9/" + str(result.id)
	os.mkdir(path)

	bin_size = 2 ** 11
	sample_rate, samples = wavfile.read(result.voice)

	s = stft.stft(samples, bin_size)

	result.freq_min = frequency.get_min_frequency(s[10::], bin_size, sample_rate)[0]
	result.freq_max = frequency.get_max_frequency(s, bin_size, sample_rate)[0]

	result.pow_timbre = timbre.most_powerful_timbre(s, bin_size, sample_rate)

	factor = 3
	audio_len = 11
	result.formants = [
		formant.most_powerful_formants(s, (3 / audio_len, 4 / audio_len), sample_rate, factor, 150),
		formant.most_powerful_formants(s, (5 / audio_len, 6 / audio_len), sample_rate, factor, 300),
		formant.most_powerful_formants(s, (9 / audio_len, 10 / audio_len), sample_rate, factor, 300)
	]

	result.save()

	plot.audio_spectrogram(sample_rate, s,  path + "/spectrogram.png", bin_size)

	noise.save_noise_map(s, path + "/noise-map.bmp")
	noise.save_noise_level_chart(s, bin_size, sample_rate, path + "/noise-level.png")

	energy.save_energy_chart(s, bin_size, sample_rate, (-60, 0), path + "/energy.png")

	# plot.audio_spectrogram(sample_rate, s, path + "/spectrogram2.png", bin_size)

	return HttpResponseRedirect(reverse('laba_9:index'))
