from django.urls import path

from . import views

app_name = 'laba_8'
urlpatterns = [
	path('', views.index, name='index'),

	# path('roberts/index', views.roberts_index, name='execute'),
	path('execute', views.execute, name='execute'),

]
