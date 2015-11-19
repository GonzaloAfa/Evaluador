"""evaluacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'jurados.views.login_session', name ='login'),
    url(r'^logout/$','jurados.views.logout_session' , name ='logout'),

    url(r'^getdataxls$' , 'participantes.views.getDataXLS'  , name='dataxls'),
    url(r'^getphotos$'  , 'participantes.views.getPhotos'   , name='getphotos'),
    url(r'^participantes/(?P<page>\d+)$', 'votaciones.views.participantes' , name='participantes'),
    url(r'^fotografias/(?P<participante>\d+)/(?P<foto>\d+)$', 'votaciones.views.fotografias' , name='fotografias'),
    url(r'^hasvote/(?P<participante>\d+)$', 'votaciones.views.hasvote', name='hasvote'),
    url(r'^criterios/$', 'votaciones.views.criterios' , name='criterios'),



]
