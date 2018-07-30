#-*- encoding: latin1-*-
"""Views, archivo para el backend del servidor"""
import json
from rest_framework_jwt.settings import api_settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt
from .utils import get_centroid, verify_favorite, five_favorites, remove_oldest_fav
from .models import Buildings, Users, Favorites
import numpy as np
import cv2

def obtain_buildings(request):
    """Service that returns the information of all the buildings (including geometry)"""
    dictionary = {}
    info_list = []
    buildings = Buildings.objects.all()
    for building in buildings:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(building.id)
        geometry = {}
        geometry["type"] = "Polygon"
        external_coords = []
        media_coords = []
        geom_long = len(building.geom[0][0])
        for i in range(geom_long):
            coords_tuple = building.geom[0][0][i]
            coordinates = []
            coordinates.append(coords_tuple[1])
            coordinates.append(coords_tuple[0])
            media_coords.append(coordinates)
        external_coords.append(media_coords)
        geometry["coordinates"] = external_coords
        feature_element["geometry"] = geometry
        info_list.append(feature_element)
    dictionary["features"] = info_list
    dictionary["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8"),
                        content_type="application/json")


def obtain_buildings_info(request):
    """Service that returns the information of all the buildings (excluding geometry)"""
    dictionary = {}
    info_list = []
    buildings = Buildings.objects.all()
    for building in buildings:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(building.id)
        information = {"codigo": building.code_infra,
                       "nombre": building.name, "unidad": building.unity_name}
        information["bloque"] = building.code_infra
        information["tipo"] = building.building_type
        information["descripcio"] = building.description
        feature_element["properties"] = information
        info_list.append(feature_element)
    dictionary["features"] = info_list
    dictionary["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
        , content_type="application/json")


def alternative_names(request):
    """Service that returns the official and alternative names of all the buildings.
    Used to populate the search bar of the Android app """
    feature_element = {}
    buildings = Buildings.objects.all()
    count = 1
    for building in buildings:
        dictionary = {}
        dictionary["name"] = building.name
        info_list = []
        code_infra = building.code_infra
        if (code_infra is not None and code_infra != ""):
            info_list.append("Bloque "+building.code_infra)
        code_gtsi = building.code_gtsi
        if (code_gtsi is not None and code_gtsi != ""):
            info_list.append(building.code_gtsi)
        dictionary["code_gtsi"] = code_gtsi
        dictionary["alternative_names"] = info_list
        dictionary["type"] = building.building_type
        feature_element[count] = dictionary
        count += 1
    return HttpResponse(json.dumps(feature_element, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')


def token_user(request, name_user):
    '''Service that generates tokens of users'''
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = Users.objects.get(username=name_user, password=name_user)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = str(token)
    user.save()
    datos_retornar = {"access-token": user.token}
    return HttpResponse(json.dumps(datos_retornar, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')

@csrf_exempt
def login(request):
    """Service that creates a user that logged in for the first time"""
    datos = json.loads(str(request.body)[2:-1])
    usuario = Users.objects.filter(username=datos.get("data").get("username"))
    if len(usuario) > 0:
        user = Users.objects.get(username=datos.get("data").get("username"),\
         password=datos.get("data").get("username"))
        datos_retornar = {"access-token": user.token}
        return HttpResponse(json.dumps(datos_retornar, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')
    usuario = Users()
    usuario.username = datos.get("data").get("username")
    usuario.password = datos.get("data").get("username")
    usuario.token = "None"
    usuario.save()
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = Users.objects.get(username=datos.get("data").get("username"),\
     password=datos.get("data").get("username"))
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = str(token)
    user.save()
    datos_retornar = {"access-token": user.token}
    return HttpResponse(json.dumps(datos_retornar, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')



def show_photo(request, codigo):
    """Service that returns the photo of a building, given its gtsi code """
    if request.method == 'GET':
        building = Buildings.objects.filter(code_infra=codigo)
        if len(building) != 1:
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
            return HttpResponseRedirect(url)
        else:
            source = "/home/jonathan/software/repo/EG_RESTServer/espolguide_app/static/img/"+codigo+"/"+codigo+".JPG"
            full_path = finders.find("img/"+codigo+"/"+codigo+".JPG")
            if full_path == None:
                url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
                return HttpResponseRedirect(url)
            photo = cv2.imread(source)
            resized = cv2.resize(photo, (640,480), interpolation = cv2.INTER_AREA)
            photo = cv2.imencode('.jpg', resized)[1].tostring()
            return HttpResponse(photo,content_type="image/jpg")
    else:
        return HttpResponseNotFound('<h1>Invalid request</h1>')


@csrf_exempt
def favorites(request):
    """Service that returns the favorite POIs of a user"""
    if request.method == 'POST':
        token = request.META["HTTP_ACCESS_TOKEN"]
        user = Users.objects.filter(token=token)
        datos = json.loads(str(request.body)[2:-1])
        code = datos.get("code_gtsi")
        if len(user) > 0:
            if not verify_favorite(code, user[0].username):
                if five_favorites(code, user[0].username):
                    building = Buildings.objects.filter(code_gtsi=code)
                    favorites = Favorites()
                    favorites.id_buildings = building[0]
                    favorites.id_users = user[0]
                    favorites.save()
                else:
                    remove_oldest_fav(user[0].username)
                    building = Buildings.objects.filter(code_gtsi=code)
                    favorites = Favorites()
                    favorites.id_buildings = building[0]
                    favorites.id_users = user[0]
                    favorites.save()

    if request.method == 'GET':
        token = request.META["HTTP_ACCESS_TOKEN"]
        user = Users.objects.filter(token=token)
    code_pois_favorites = []
    if len(user) > 0:
        favorites = Favorites.objects.filter(id_users=user[0].id)
        for fav in favorites:
            building = Buildings.objects.filter(id=fav.id_buildings.id)
            code_pois_favorites.append(building[0].code_gtsi)
    feature = {"codes_gtsi": code_pois_favorites}
    return HttpResponse(json.dumps(feature, ensure_ascii=False).encode("utf-8")\
    , content_type='application/json')


def get_building_centroid(request, code_gtsi):
    """Service that returns the centroid of a building"""
    dictionary = {}
    building = Buildings.objects.filter(code_gtsi=code_gtsi)
    #If there are no buildings or more than one with that code
    #Return empty dictionary
    if len(building) != 1:
        return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
        , content_type="application/json")
    building = building[0]
    points = []
    geom_long = len(building.geom[0][0])
    for i in range(geom_long):
        coords_tuple = building.geom[0][0][i]
        coordinates = (coords_tuple[1], coords_tuple[0])
        points.append(coordinates)
    centroid = get_centroid(points)
    dictionary["lat"] = centroid[0]
    dictionary["long"] = centroid[1]
    return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
        , content_type="application/json")

@csrf_exempt
def delete_favorite(request):
    """Delete a favorite POIs from your list"""
    code_pois_favorites = []
    if request.method == 'POST':
        datos = json.loads(str(request.body)[2:-1])
        code_gtsi = datos.get("code_gtsi")
        token = request.META["HTTP_ACCESS_TOKEN"]
        user = Users.objects.filter(token=token)
        if len(user) > 0:
            favorites = Favorites.objects.filter(id_users=user[0].id)
            for fav in favorites:
                building = Buildings.objects.filter(id=fav.id_buildings.id)
                if building[0].code_gtsi == code_gtsi:
                    fav.delete()
                    break
        if len(user) > 0:
            favorites = Favorites.objects.filter(id_users=user[0].id)
            for fav in favorites:
                building = Buildings.objects.filter(id=fav.id_buildings.id)
                code_pois_favorites.append(building[0].code_gtsi)
        feature = {"codes_gtsi": code_pois_favorites}
        return HttpResponse(json.dumps(feature, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')
    else:
        return HttpResponseNotFound('<h1>Invalid request</h1>')
