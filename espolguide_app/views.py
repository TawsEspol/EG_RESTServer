#-*- encoding: latin-1 -*-
'''Views, archivo para el backend del servidor'''
import json
from osgeo import osr
from django.http import HttpResponse
from .models import Bloques

# Create your views here.

def obtener_bloques(request):
    '''Funcion para poder obtener la informacion de los bloques incluido los shapefiles o 
    poligonos para ubicarlos en la app'''
    diccionario = {}
    # d["type"]="FeatureCollection"
    lista = []
    bloques = Bloques.objects.all()
    numero = 1
    for b in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(numero)
        numero += 1
        geometry = {}
        geometry["type"] = "Polygon"
        coordenadas_externa = []
        coordenadas_media = []
        rango = len(b.geom[0][0])
        for i in range(rango):
            tupla = b.geom[0][0][i]
            wgs84 = osr.SpatialReference()
            wgs84.ImportFromEPSG(4326)
            inp = osr.SpatialReference()
            inp.ImportFromEPSG(32717)
            transformation = osr.CoordinateTransformation(inp, wgs84)
            tupla_transformada = transformation.TransformPoint(tupla[0], tupla[1])
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
    for b in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["identificador"] = "Bloque"+str(numero)
        numero += 1
        informacion = {"codigo": b.codigo, "nombre": b.nombre, "unidad": b.unidad}
        informacion["bloque"] = b.bloque
        informacion["tipo"] = b.tipo
        feature_element["properties"] = informacion
        lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario,ensure_ascii=False).encode("latin1"), content_type='application/json')


def info_bloque(request, pk):
    '''FUncion que recibe un codigo y devuelve la informacion del bloque con ese codigo'''
    diccionario = {}
    # d["type"]="FeatureCollection"
    lista = []
    b = Bloques.objects.get(pk=pk)
    feature_element = {}
    feature_element["type"] = "Feature"
    informacion = {"codigo": b.codigo, "nombre": b.nombre, "unidad": b.unidad}
    informacion["bloque"] = b.bloque
    informacion["tipo"] = b.tipo
    informacion["descripcio"] = b.descripcio
    feature_element["properties"] = informacion
    geometry = {}
    geometry["type"] = "Polygon"
    coordenadas_externa = []
    coordenadas_media = []
    rango = len(b.geom[0][0])
    for i in range(rango):
        tupla = b.geom[0][0][i]
        wgs84 = osr.SpatialReference()
        wgs84.ImportFromEPSG(4326)
        inp = osr.SpatialReference()
        inp.ImportFromEPSG(32717)
        transformation = osr.CoordinateTransformation(inp, wgs84)
        tupla_transformada = transformation.TransformPoint(tupla[0], tupla[1])
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
    for b in bloques:
        diccionario = {}
        diccionario["NombreOficial"] = b.codigo
        lista = []
        if b.nombre != "":
            lista.append(b.nombre)
        lista.append(b.descripcio)
        diccionario["NombresAlternativos"] = lista
        diccionario["tipo"] = b.tipo
        feature_element["Bloque"+str(numero)] = diccionario
        numero += 1
    return HttpResponse(json.dumps(feature_element,ensure_ascii=False).encode("latin1"), content_type='application/json')

def imagen_bloque(request,codigo):
    # resp = HttpResponse(content_type="text/html")
    # # imagen_file = file('img/'+str(codigo)+'.jpg')
    # # encoded_string = base64.b64encode(image_file.read())
    # resp.write("<img src='img/%s.jpg'>"%str(codigo))
    # return resp
    response = HttpResponse(content_type="image/jpeg")
    img = Image.open('espolguide_app/img/'+str(codigo)+'.jpg')
    img.save(response,'jpeg')
    return response


