#-*- encoding: latin-1 -*-
'''Views, archivo para el backend del servidor'''
import json
from osgeo import osr
from PIL import Image
from django.http import HttpResponse
from .models import Bloques
<<<<<<< HEAD

=======
>>>>>>> ced7774f20a7b439fd455f5a862b5d1a57d9cf75

# Create your views here.

def transformar_coordenada(latitud, longitud):
    '''Funcion para transformar el sistema de coordenadas'''
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromEPSG(4326)
    inp = osr.SpatialReference()
    inp.ImportFromEPSG(32717)
    transformation = osr.CoordinateTransformation(inp, wgs84)
    return transformation.TransformPoint(latitud, longitud)


def obtener_bloques(request):
    '''Funcion para poder obtener la informacion de los bloques incluido los shapefiles o
    poligonos para ubicarlos en la app'''
    diccionario = {}
    lista = []
    bloques = Bloques.objects.all()
    numero = 1
    for bloque in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(numero)
        numero += 1
        geometry = {}
        geometry["type"] = "Polygon"
        coordenadas_externa = []
        coordenadas_media = []
        rango = len(bloque.geom[0][0])
        for i in range(rango):
            tupla = bloque.geom[0][0][i]
            tupla_transformada = transformar_coordenada(tupla[0], tupla[1])
            # print(tupla[0])
            coordenadas = []
            coordenadas.append(tupla_transformada[1])
            coordenadas.append(tupla_transformada[0])
            coordenadas_media.append(coordenadas)
        # print("SE ACABO EL POLIGONO")
        coordenadas_externa.append(coordenadas_media)
        geometry["coordinates"] = coordenadas_externa
        feature_element["geometry"] = geometry
        lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario,ensure_ascii=False).encode("latin1"), content_type='application/json')





def obtener_informacion_bloques(request):
    '''Funcion para obtener solo informacion de cloques sin incluir shapefiles'''
    diccionario = {}
    # d["type"]="FeatureCollection"
    lista = []
    bloques = Bloques.objects.all()
    numero = 1
    for bloque in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(numero)
        numero += 1
<<<<<<< HEAD
        informacion = {"codigo": bloque.codigo, "nombre": bloque.nombre, "unidad": bloque.unidad}
        informacion["bloque"] = bloque.bloque
        informacion["tipo"] = bloque.tipo
        informacion["descripcio"] = bloque.descripcio
=======
        informacion = {"codigo": b.codigo, "nombre": b.nombre, "unidad": b.unidad}
        informacion["bloque"] = b.bloque
        informacion["tipo"] = b.tipo
>>>>>>> ced7774f20a7b439fd455f5a862b5d1a57d9cf75
        feature_element["properties"] = informacion
        lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario,ensure_ascii=False).encode("latin1"), content_type='application/json')


def info_bloque(request, primary_key):
    '''FUncion que recibe un codigo y devuelve la informacion del bloque con ese codigo'''
    diccionario = {}
    # d["type"]="FeatureCollection"
    lista = []
    bloque = Bloques.objects.get(pk=primary_key)
    feature_element = {}
    feature_element["type"] = "Feature"
    informacion = {"codigo": bloque.codigo, "nombre": bloque.nombre, "unidad": bloque.unidad}
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
        tupla_transformada = transformar_coordenada(tupla[0], tupla[1])
        # print(tupla[0])
        coordenadas = []
        coordenadas.append(tupla_transformada[1])
        coordenadas.append(tupla_transformada[0])
        coordenadas_media.append(coordenadas)
        break
    # print("SE ACABO EL POLIGONO")
    coordenadas_externa.append(coordenadas_media)
    geometry["coordinates"] = coordenadas_externa
    feature_element["geometry"] = geometry
    lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario,ensure_ascii=False).encode("latin1"), content_type='application/json')


def nombres_bloques(request):
    '''Funcion que retorna los nombres oficiales y alternativos de los bloques '''
    feature_element = {}
    # d["type"]="FeatureCollection"
    bloques = Bloques.objects.all()
    numero = 1
    for bloque in bloques:
        diccionario = {}
        diccionario["NombreOficial"] = bloque.codigo
        lista = []
        if bloque.nombre != "":
            lista.append(bloque.nombre)
        lista.append(bloque.descripcio)
        diccionario["NombresAlternativos"] = lista
        diccionario["tipo"] = bloque.tipo
        feature_element["Bloque"+str(numero)] = diccionario
        numero += 1
    return HttpResponse(json.dumps(feature_element,ensure_ascii=False).encode("latin1"), content_type='application/json')

def imagen_bloque(request, codigo):
    '''Funcion que genera la ruta para la imagen de los bloques '''
    response = HttpResponse(content_type="image/jpeg")
    img = Image.open('espolguide_app/img/'+str(codigo)+'.jpg')
    img.save(response, 'jpeg')
    return response
