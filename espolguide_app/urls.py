from django.conf.urls import include, url
from . import views
APP_NAME = 'espolguide_app'
urlpatterns = [
    url(r'^obtenerBloques/', views.obtener_bloques),
    url(r'^obtenerInformacionBloques/', views.obtener_informacion_bloques),
]
