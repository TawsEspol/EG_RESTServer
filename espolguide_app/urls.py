from django.conf.urls import include,urls
from django.contrib import admin
admin.autodiscover()
from . import views

#from .viewsets import 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r')

urlpatterns = [
	url(r'^$',views.principal),
	url(r'^bloques/',views.obtenerBloques,name='obtenerBloques')
]

