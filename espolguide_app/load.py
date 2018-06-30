'''Script para cargar shapefiles en la base de datos se debe ejecutar en el shell de django'''
import os
from django.contrib.gis.utils import LayerMapping
from .models import Buildings, Unities
# Auto-generated `LayerMapping` dictionary for Bloques model
BLOQUES_MAPPING = {
    'code_infra': 'code_infra',
    'code_gtsi': 'code_gtsi',
    'name': 'name',
    'name_infra': 'name_infra',
    'building_type': 'building_t',
    'description': 'descriptio',
    'geom': 'MULTIPOLYGON',
}
#BLOQUES_SHP = os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                           'data/Bloques/prueba', 'datos-de-prueba.shp'),)
BLOQUES_SHP =  "/home/belen/Downloads/Shapes/data/Bloques/bloques-faltantes.shp"

def run(verbose=True):
    '''Funcion para cargar los shapefiles'''
    layer_map = LayerMapping(
        Buildings, BLOQUES_SHP, BLOQUES_MAPPING,
        transform=False, encoding='utf-8',
    )
    layer_map.save(strict=True, verbose=verbose)

def load_unities():
    file = open("dumps/unidades.txt","r")
    for line in file:
        data = line.strip().split("\t")
        name = data[0]
        unidad = Unities(name = name)
        if len(data)==2:
            description = data[1]
            unidad.description = description
        unidad.save()

    file.close()

