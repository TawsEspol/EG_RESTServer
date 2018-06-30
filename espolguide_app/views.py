#-*- encoding: latin1-*-
"""Views, archivo para el backend del servidor"""
import json
from rest_framework.authtoken.models import Token
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from django.http import HttpResponse
from .models import Bloques, Users
from django.http import HttpResponse, HttpResponseRedirect 
from django.templatetags.static import static
from django.shortcuts import redirect
from django.contrib.staticfiles import finders



def obtener_bloques(request):
    """Funcion para poder obtener la informacion de los bloques incluido los shapefiles o
    poligonos para ubicarlos en la app"""
    diccionario = {}
    lista = []
    bloques = Bloques.objects.all()
    for bloque in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(bloque.id)
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
        # print("SE ACABO EL POLIGONO")
        coordenadas_externa.append(coordenadas_media)
        geometry["coordinates"] = coordenadas_externa
        feature_element["geometry"] = geometry
        lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario, ensure_ascii=False).encode("latin1"),
                        content_type="application/json")


def obtener_informacion_bloques(request):
    """Funcion para obtener solo informacion de cloques sin incluir shapefiles"""
    diccionario = {}
    lista = []
    bloques = Bloques.objects.all()
    for bloque in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
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
    return HttpResponse(json.dumps(diccionario, ensure_ascii=False).encode("latin1")\
        , content_type="application/json")



def info_bloque(request, primary_key, token):
    """Funcion que recibe un codigo y devuelve la informacion del bloque con ese codigo"""
    usuario = Users.objects.filter(token = token)
    if len(usuario) > 0:
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
        return HttpResponse(json.dumps(diccionario, ensure_ascii=False).encode("latin1")\
            , content_type="application/json")
    return HttpResponse("Token Invalido")



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

    return HttpResponse(json.dumps(feature_element, ensure_ascii=False).encode("latin1")\
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
        block = Bloques.objects.filter(bloque=codigo)
        if (len(block) == 0):
        	url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
        	return HttpResponseRedirect(url)
        full_path = finders.find("img/"+codigo+"/"+codigo+".JPG")
        if full_path == None :
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
        else:
            url = "http://www.espol-guide.espol.edu.ec/static/img/"+codigo+"/"+codigo+".JPG"
        return HttpResponseRedirect(url)
    return HttpResponse("Token Invalido")
