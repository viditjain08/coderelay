"""relay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mainapp.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register$', register, name='register'),
    url(r'^ajax/register/$', ajaxregister, name='ajaxregister'),
    url(r'^login$', login, name='login'),
    url(r'^ajax/login/$', ajaxlogin, name='ajaxlogin'),
    url(r'^$', loginregister, name='loginregister'),
    url(r'^game$', compiler, name='game'),
    url(r'^game1$', abcd, name='game1'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^ajax/runcode/', runcode, name='runcode'),
    url(r'^ajax/savecode/', savecode, name='savecode'),
    url(r'^ajax/swapcode/', swapcode, name='swapcode'),
    url(r'^ajax/submitques/', submitques, name='submitques'),
    url(r'^ajax/finishrace/', finishrace, name='finishrace')
]
