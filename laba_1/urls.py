from django.urls import path

from . import views

app_name = 'laba_1'
urlpatterns = [
	path('', views.index, name='index'),

	path('resampling/index', views.resampling_index, name='resampling-index'),
	path('resampling', views.resampling, name='resampling'),

	path('grayscale/index', views.grayscale_index, name='grayscale-index'),
	path('grayscale', views.grayscale, name='grayscale'),

	path('threshold/index', views.threshold_index, name='threshold-index'),
	path('threshold', views.threshold, name='threshold'),
]
