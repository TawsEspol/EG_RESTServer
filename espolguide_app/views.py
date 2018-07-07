#-*- encoding: latin1-*-
"""Views, archivo para el backend del servidor"""
import json
<<<<<<< HEAD
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import HttpResponse
from .models import Buildings, Users
from django.http import HttpResponse, HttpResponseRedirect 
from django.templatetags.static import static
from django.shortcuts import redirect
=======
#from osgeo import osr
from django.http import HttpResponse, HttpResponseRedirect
>>>>>>> master
from django.contrib.staticfiles import finders
from .models import Bloques




def obtener_bloques(request):
    """Funcion para poder obtener la information de los Buildings incluido los shapefiles o
    poligonos para ubicarlos en la app"""
    dictionary = {}
    info_list = []
    buildings = Buildings.objects.all()
    for building in buildings:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(building.id) #Cómo almacenan y usan estos ids
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
<<<<<<< HEAD
        feature_element["identificador"] = "Bloque"+str(building.id)
        information = {"codigo": building.code_infra,
                       "nombre": building.name, "unidad": building.unity}
        information["bloque"] = building.code_infra #CUÁL ES LA DIFERENCIA ENTRE LAS CLAVES bloque y código
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
    """RETORNAR SOLO PRIMERA COORDENADA"""
    usuario = Users.objects.filter(token = token)
    a=1
    if len(usuario) > 0:
        dictionary = {}
        info_list = []
        building = Buildings.objects.filter(pk=primary_key)
        #If there are no buildings or more than one with that pk
        #Return empty dictionary
        if (len(building) != 1 ):
            return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
            , content_type="application/json")
        building = building[0]
        feature_element = {}
        feature_element["type"] = "Feature"
        information = {"codigo": building.code_infra,
                       "nombre": building.name, "unidad": building.unity}
        information["bloque"] = building.code_infra  #CUÁL ES LA DIFERENCIA ENTRE LAS CLAVES bloque y código
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



def alternative_names(request):
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
    user.token= str(token)
    user.save()
    return HttpResponse(str(token))  

def add_user(request, data):
    usuario = Users()
    usuario.username = data
    usuario.password = data
    usuario.token = "None"
    usuario.save()
    return HttpResponse(str(True))
    

def show_photo(request, codigo,  token):
    """Return the photo of a block """
    usuario = Users.objects.filter(token = token)
    if len(usuario) > 0:
        building = Buildings.objects.filter(code_infra=codigo)
        if (len(building) != 1):
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
            return HttpResponseRedirect(url)
        full_path = finders.find("img/"+codigo+"/"+codigo+".JPG")
        if full_path == None :
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
        else:
            url = "http://www.espol-guide.espol.edu.ec/static/img/"+codigo+"/"+codigo+".JPG"
            #url = "192.168.0.7:8000/static/"+codigo+"/"+codigo+".JPG"
        return HttpResponseRedirect(url)
    return HttpResponse("Token Invalido")
=======
        feature_element["identificador"] = "Bloque"+str(bloque.id)
        informacion = {"codigo": bloque.codigo,
                       "nombre": bloque.nombre, "unidad": bloque.unidad}
        informacion["bloque"] = bloque.bloque
        informacion["tipo"] = bloque.tipo
        informacion["descripcio"] = bloque.descripcio
        feature_element["properties"] = informacion
        lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario, ensure_ascii=False).encode("latin1"),\
        content_type="application/json")


def info_bloque(request, primary_key):
    """Funcion que recibe un codigo y devuelve la informacion del bloque con ese codigo"""
    diccionario = {}
    lista = []
    bloque = Bloques.objects.get(pk=primary_key)
    feature_element = {}
    feature_element["type"] = "Feature"
    informacion = {"codigo": bloque.codigo,
                   "nombre": bloque.nombre, "unidad": bloque.unidad}
    informacion["bloque"] = bloque.bloque
    informacion["tipo"] = bloque.tipo
    informacion["descripcio"] = bloque.descripcio
    feature_element["properties"] = informacion
    geometry = {}
    geometry["type"] = "Polygon"
    coordenadas_externa = []
    coordenadas_media = []
    rango = len(bloque.geom[0][0])
    for i in range(rango):
        tupla = bloque.geom[0][0][i]
        coordenadas = []
        coordenadas.append(tupla[1])
        coordenadas.append(tupla[0])
        coordenadas_media.append(coordenadas)
        break
    # print("SE ACABO EL POLIGONO")
    coordenadas_externa.append(coordenadas_media)
    geometry["coordinates"] = coordenadas_externa
    feature_element["geometry"] = geometry
    lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario, ensure_ascii=False).encode("latin1"),\
        content_type="application/json")


def nombres_bloques(request):
    """Returns the official and alternative names of a block """
    feature_element = {}
    bloques = Bloques.objects.all()
    for bloque in bloques:
        diccionario = {}
        diccionario["NombreOficial"] = bloque.codigo
        lista = []
        if bloque.nombre != "":
            lista.append(bloque.nombre)
        lista.append(bloque.descripcio)
        diccionario["NombresAlternativos"] = lista
        diccionario["tipo"] = bloque.tipo
        feature_element["Bloque"+str(bloque.id)] = diccionario
    return HttpResponse(json.dumps(feature_element, ensure_ascii=False).encode("latin1"), \
        content_type="application/json")


def show_photo(request, codigo):
    """Return the photo of a block """
    building = Bloques.objects.filter(codigo=codigo)
    if (len(building) != 1):
        url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
        return HttpResponseRedirect(url)
    full_path = finders.find("img/"+codigo+"/"+codigo+".JPG")
    if full_path == None :
        url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
    else:
        url = "http://www.espol-guide.espol.edu.ec/static/img/"+codigo+"/"+codigo+".JPG"
    return HttpResponseRedirect(url)
>>>>>>> master
