'''Urls, archivo para  definir las urls con las que se accederan a los view'''
from django.conf.urls import  url
from . import views
APP_NAME = 'espolguide_app'
urlpatterns = [
    url(r'^obtenerBloques/', views.obtener_bloques),
    url(r'^obtenerInformacionBloques/', views.obtener_informacion_bloques),
    url(r'^infoBloque/(?P<pk>[\w|\W]+)$', views.info_bloque),
    url(r'^nombresAlternativo/', views.nombres_bloques),
    url(r'^fotoBloque/(?P<codigo>[\w|\W]+)$', views.imagen_bloque),
]
