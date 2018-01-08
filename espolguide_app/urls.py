from django.conf.urls import include, url
from . import views
app_name = 'espolguide_app'
urlpatterns = [
        url(r'^obtenerBloques/', views.obtenerBloques),
        url(r'^obtenerInformacionBloques/', views.obtenerInformacionBloques),
    ]