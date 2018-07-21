'''Urls, archivo para  definir las urls con las que se accederan a los view'''
from django.conf.urls import  url
from rest_framework_jwt.views import obtain_jwt_token
from . import views
APP_NAME = 'espolguide_app'
urlpatterns = [
    url(r'^obtainBuildings/', views.obtain_buildings),
    url(r'^obtainBuildingsInfo/', views.obtain_buildings_info),
    url(r'^buildingInfo/(?P<code_gtsi>[\w|\W]+)', views.building_info),
    url(r'^alternativeNames/', views.alternative_names),
    url(r'^photoBlock/(?P<codigo>[\w|\W]*)', views.show_photo),
    url(r'^apitokenauth/(?P<name_user>[\w|\W]+)$', views.token_user),
    url(r'^login/', views.login),
    url(r'^favorites/', views.favorites),
    url(r'^coordinates/(?P<code_gtsi>[\w |\W ]+)/$', views.get_building_centroid),
    url(r'^deleteFavorite/', views.delete_favorite),
]

