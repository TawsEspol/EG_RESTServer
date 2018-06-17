#-*- encoding: latin1-*-
"""Views, archivo para el backend del servidor"""
import json
#from osgeo import osr
from PIL import Image
from django.http import HttpResponse, HttpResponseRedirect 
from .models import *
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
    return HttpResponse(json.dumps(diccionario, ensure_ascii=False).encode("latin1"), content_type="application/json")


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
    return HttpResponse(json.dumps(diccionario, ensure_ascii=False).encode("latin1"), content_type="application/json")


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
    return HttpResponse(json.dumps(feature_element, ensure_ascii=False).encode("latin1"), content_type="application/json")


def show_photo(request, codigo):
    """Return the photo of a block """
    try:
        block = Bloques.objects.get(bloque=codigo)
        full_path = finders.find("img/"+codigo+"/"+codigo+".JPG")
        print(full_path)
        if full_path == None :
            url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
        else:
            url = "http://www.espol-guide.espol.edu.ec/static/img/"+codigo+"/"+codigo+".JPG"
        return HttpResponseRedirect(url)
    
    except Bloques.DoesNotExist:
        url = "http://www.espol-guide.espol.edu.ec/static/img/espol/espol.png"
        return HttpResponseRedirect(url)
