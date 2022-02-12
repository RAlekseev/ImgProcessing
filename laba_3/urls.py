from django.urls import path

from . import views

app_name = 'laba_3'
urlpatterns = [
	path('', views.index, name='index'),

	path('roberts/index', views.roberts_index, name='roberts-index'),
	path('roberts', views.roberts, name='roberts'),

]
