#-*- encoding: latin1-*-
"""Views, archivo para el backend del servidor"""
import json
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import HttpResponse
from .models import Buildings, Users
from django.http import HttpResponse, HttpResponseRedirect 
from django.templatetags.static import static
from django.shortcuts import redirect
from django.contrib.staticfiles import finders



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
    usuario = Users.objects.filter(token = token)
    if len(usuario) > 0:
        dictionary = {}
	    info_list = []
	    building = Buildings.objects.filter(pk=primary_key)
	    #If there are no buildings or more than one with that pk
	    #Return empty dictionary
	    if (len(building) != 1 ):
	        return HttpResponse(json.dumps(dictionary, ensure_ascii=False).encode("utf-8")\
	        , content_type="application/json")
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



def nombres_bloques(request):
    """Returns the official and alternative names of a block """
    feature_element = {}
    buildings = Buildings.objects.all()
    for building in buildings:
        dictionary = {}
        dictionary["NombreOficial"] = building.code_infra
        info_list = []
        if building.name != "":
            info_list.append(building.name)
        info_list.append(building.descripcio)
        dictionary["NombresAlternativos"] = info_list
        dictionary["tipo"] = building.building_type
        feature_element["Bloque"+str(building.id)] = dictionary

    return HttpResponse(json.dumps(feature_element, ensure_ascii=False).encode("utf-8")\
        , content_type='application/json')


def token_user(request, name_user):
    '''Funcion para generar token para usuarios'''
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    user = Users.objects.get(username=name_user, password=name_user)
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    user.token= str(token)
    user.save()
    return HttpResponse(str(token))  

def add_user(request, datos):
    #try:
    usuario = Users()
    usuario.username = datos
    usuario.password = datos
    usuario.token = "None"
    usuario.save()
    return HttpResponse(str(True))
    #except:
     #   return HttpResponse(str(False))


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
	    return HttpResponseRedirect(url)
    return HttpResponse("Token Invalido")
