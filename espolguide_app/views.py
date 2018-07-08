#-*- encoding: latin1-*-
"""Views, archivo para el backend del servidor"""
import json
from rest_framework_jwt.settings import api_settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.staticfiles import finders
from .models import Buildings, Users, Favorites



def obtener_bloques(request):
    """Funcion para poder obtener la information de los Buildings incluido los shapefiles o
    poligonos para ubicarlos en la app"""
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
        # print("SE ACABO EL POLIGONO")
        external_coords.append(media_coords)
        geometry["coordinates"] = external_coords
        feature_element["geometry"] = geometry
        info_list.append(feature_element)
    dictionary["features"] = info_list
    dictionary["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8"),
                        content_type="application/json")


def obtener_informacion_bloques(request):
    """Funcion para obtener solo information de cloques sin incluir shapefiles"""
    dictionary = {}
    info_list = []
    buildings = Buildings.objects.all()
    for building in buildings:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(building.id)
        information = {"codigo": building.code_infra,
                       "nombre": building.name, "unidad": building.unity}
        information["bloque"] = building.code_infra
        information["tipo"] = building.building_type
        information["descripcio"] = building.description
        feature_element["properties"] = information
        info_list.append(feature_element)
    dictionary["features"] = info_list
    dictionary["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
        , content_type="application/json")


def info_bloque(request, primary_key, token):
    """Funcion que recibe un codigo y devuelve la informacion del bloque con ese codigo"""
    usuario = Users.objects.filter(token=token)
    if len(usuario) > 0:
        dictionary = {}
        info_list = []
        building = Buildings.objects.filter(pk=primary_key)
        #If there are no buildings or more than one with that pk
        #Return empty dictionary
        if len(building) != 1:
            return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
            , content_type="application/json")
        feature_element = {}
        feature_element["type"] = "Feature"
        information = {"codigo": building.code_infra,
                       "nombre": building.name, "unidad": building.unity}
        information["bloque"] = building.code_infra
        information["tipo"] = building.building_type
        information["descripcio"] = building.description
        feature_element["properties"] = information
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
            break
        # print("SE ACABO EL POLIGONO")
        external_coords.append(media_coords)
        geometry["coordinates"] = external_coords
        feature_element["geometry"] = geometry
        info_list.append(feature_element)
        dictionary["features"] = info_list
        dictionary["type"] = "FeatureCollection"
        return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
            , content_type="application/json")
    return HttpResponse("Token Invalido")



def nombres_bloques(request):
    """Returns the official and alternative names of a building """
    feature_element = {}
    buildings = Buildings.objects.all()
    for building in buildings:
        dictionary = {}
        dictionary["NombreOficial"] = building.name
        info_list = []
        if building.name != "":
            code_infra = building.code_infra
            if code_infra != "":
                info_list.append("Bloque "+building.code_infra)
            code_gtsi = building.code_gtsi
            if code_gtsi != "":
                info_list.append(building.code_gtsi)
        info_list.append(building.description)
        dictionary["NombresAlternativos"] = info_list
        dictionary["tipo"] = building.building_type
        feature_element["Bloque"+str(building.id)] = dictionary

    return HttpResponse(json.dumps(feature_element, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')


def token_user(request, name_user):
    '''Function that generates tokens of users'''
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = Users.objects.get(username=name_user, password=name_user)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = str(token)
    user.save()
    return HttpResponse(str(token))

def add_user(request, datos):
    """Service for create user for create tokens"""
    usuario = Users()
    usuario.username = datos
    usuario.password = datos
    usuario.save()
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = Users.objects.get(username=name_user, password=name_user)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token = str(token)
    return HttpResponse(str(True))

def get_token(request, name_user):
    """Service for get token"""
    user = Users.objects.filter(username=name_user)
    if len(user) > 0:
        return HttpResponse(user.token)
    return HttpResponse("User Invalido")


def show_photo(request, codigo, token):
    """Return the photo of a block """
    usuario = Users.objects.filter(token=token)
    if len(usuario) > 0:
        building = Buildings.objects.filter(code_infra=codigo)
        if len(building) != 1:
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
            return HttpResponseRedirect(url)
        full_path = finders.find("img/"+codigo+"/"+codigo+".JPG")
        if full_path == None:
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
        else:
            url = "http://www.espol-guide.espol.edu.ec/static/img/"+codigo+"/"+codigo+".JPG"
        return HttpResponseRedirect(url)
    return HttpResponse("Token Invalido")

def add_favorite(request):
    """Service for add favorite POIs for a user"""
    if request.method == 'POST':
        token = request.META["access_token"]
        user = Users.objects.filter(token=token)
        code = request["data"]["code_gtsi"]
        if len(user) > 0:
            building = Buildings.objects.filter(code_gtsi=code)
            favorites = Favorites()
            favorites.id_buildings = building.id
            favorites.id_users = user.id
            favorites.save()

def get_favorites(request)
"""Service for get favorites POIs for a user"""
if request.method == 'POST':
        token = request.META["access_token"]
        user = Users.objects.filter(token=token)
        code_pois_favorites = []
        if len(user) > 0:
            favorites = Favorites.objects.filter(id_users=user.id)
            for fav in favorites:
                building = Buildings.objects.filter(id=fav.id_buildings)
                code_pois_favorites.append(building.code_gtsi)
        feature = {"codes_gtsi": code_pois_favorites}
        return HttpResponse(json.dumps(feature, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')                
