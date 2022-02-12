from django.urls import path

from . import views

app_name = 'laba_4'
urlpatterns = [
	path('', views.index, name='index'),

]
