"""Bopai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('laba_9/', include('laba_9.urls'), name='laba_9'),
    path('laba_8/', include('laba_8.urls'), name='laba_8'),
    path('laba_7/', include('laba_7.urls'), name='laba_7'),
    path('laba_6/', include('laba_6.urls'), name='laba_6'),
    path('laba_5/', include('laba_5.urls'), name='laba_5'),
    path('laba_4/', include('laba_4.urls'), name='laba_4'),
    path('laba_3/', include('laba_3.urls'), name='laba_3'),
    path('laba_2/', include('laba_2.urls'), name='laba_2'),
    path('laba_1/', include('laba_1.urls'), name='laba_1'),
    path('results/', include('results.urls'), name='results'),
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
