import json
from django.http import HttpResponse
from django.db import connection
from pyproj import Proj, transform
from .models import Bloques


# Create your views here.


'''Funcion para poder obtener la informacion de los bloques incluido los shapefiles o poligonos para ubicarlos en la app'''


def obtener_bloques(request):
    diccionario = {}
    # d["type"]="FeatureCollection"
    lista = []
    bloques = Bloques.objects.all()
    for b in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["properties"] = {"codigo": b.codigo, "nombre": b.nombre, "unidad": b.unidad,
                                         "bloque": b.bloque, "tipo": b.tipo, "descripcio": b.descripcio, "area_m2": b.area_m2}
        geometry = {}
        geometry["type"] = "Polygon"
        coordenadas_externa = []
        coordenadas_media = []
        rango = len(b.geom[0][0])
        for i in range(rango):
            tupla = b.geom[0][0][i]
            # print(tupla[0])
            coordenadas = []
            coordenadas.append(tupla[0])
            coordenadas.append(tupla[1])
            coordenadas_media.append(coordenadas)
        #print("SE ACABO EL POLIGONO")
        coordenadas_externa.append(coordenadas_media)
        geometry["coordinates"] = coordenadas_externa
        feature_element["geometry"] = geometry
        lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario), content_type='application/json')


'''Funcion para obtener solo informacion de cloques sin incluir shapefiles'''


def obtener_informacion_bloques(request):
    diccionario = {}
    # d["type"]="FeatureCollection"
    lista = []
    bloques = Bloques.objects.all()
    for b in bloques:
        feature_element = {}
        feature_element["type"] = "Feature"
        feature_element["properties"] = {"codigo": b.codigo, "nombre": b.nombre,
                                         "unidad": b.unidad, "bloque": b.bloque, "tipo": b.tipo, "descripcio": b.descripcio}
        lista.append(feature_element)
    diccionario["features"] = lista
    diccionario["type"] = "FeatureCollection"
    return HttpResponse(json.dumps(diccionario), content_type='application/json')


'''Funcion para trasformar un sistema de coordenadas a otro'''


def transformar_coordenadas(coord1, coord2):
    in_proj = Proj(init='epsg:3857')
    out_proj = Proj(init='epsg:4326')
    new_coord_x1, new_coord_y1 = coord1, coord2
    new_coord_x2, new_coord_y2 = transform(
        in_proj, out_proj, new_coord_x1, new_coord_y1)
    print(new_coord_x2, new_coord_y2)
