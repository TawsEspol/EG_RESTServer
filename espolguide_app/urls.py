'''Urls, archivo para  definir las urls con las que se accederan a los view'''
from django.conf.urls import  url
from rest_framework_jwt.views import obtain_jwt_token
from . import views
APP_NAME = 'espolguide_app'
urlpatterns = [
    url(r'^obtenerBloques/', views.obtener_bloques),
    url(r'^obtenerInformacionBloques/', views.obtener_informacion_bloques),
    url(r'^infoBloque/(?P<primary_key>[\w|\W]+)$', views.info_bloque),
    url(r'^nombresAlternativo/', views.nombres_bloques),
    url(r'^photoBlock/(?P<codigo>[\w|\W]*)$', views.show_photo),
    url(r'^apitokenauth/(?P<name_user>[\w|\W]+)$', views.token_user),
    url(r'^createUser/(?P<datos>[\w|\W]+)$', views.add_user),

]
