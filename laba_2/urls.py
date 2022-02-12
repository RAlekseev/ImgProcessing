from django.urls import path

from . import views

app_name = 'laba_2'
urlpatterns = [
	path('', views.index, name='index'),

	path('opening/index', views.opening_index, name='opening-index'),
	path('opening', views.opening, name='opening'),

]
